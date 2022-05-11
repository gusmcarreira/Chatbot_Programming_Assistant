import ast
import astor

class CodeInformation(ast.NodeVisitor):
    def __init__(self):
        # Keep track of variable's values
        self.var_map = {}
        # Control what concepts are being used in the algorithm
        self.all_concepts_map = []
        # Check if it comes from print
        self.isPrint = False
        self.ifControl = {}
    # ------------------------ VARIABLES --------------------
    def visit_Assign(self, node):
        self.all_concepts_map.append("Declaração de variável")
        # Var name
        var_name = self.visit(node.targets[0])[1]
        # Var value
        var_value = self.visit(node.value)

        if var_value:
            # Store var information
            self.var_map[var_name] = var_value
            if var_value[0] == "Constant":
                self.all_concepts_map.append(self.value_meaning(var_value[1]))
            elif var_value[0] == "Op":
                self.all_concepts_map.append(var_value[1])
        return
    # =============================== FUNCTIONS ===============================
    def visit_FunctionDef(self, node):
        self.all_concepts_map.append("Declaração de função")

        self.all_concepts_map.append("[INICIO ESCOPO FUNÇÃO]")

        for concept in node.body:
            self.visit(concept)

        self.all_concepts_map.append("[FINAL ESCOPO FUNÇÃO]")

        return

    # ============================== CONDITIONS ===============================
    def visit_If(self, node):
        if node.col_offset not in self.ifControl:
            wanted_ident_start = "[INICIO ESCOPO IF]"
            wanted_ident_end = "[FINAL ESCOPO IF]"
            self.all_concepts_map.append("Declaração de condicional (if)")
        else:
            if self.ifControl[node.col_offset] == "elif":
                wanted_ident_start = "[INICIO ESCOPO ELIF]"
                wanted_ident_end = "[FINAL ESCOPO ELIF]"
                self.all_concepts_map.append("Declaração de condicional (elif)")

        self.all_concepts_map.append(wanted_ident_start)

        for concept in node.body:
            self.visit(concept)

        self.all_concepts_map.append(wanted_ident_end)

        if node.orelse:
            for arg in node.orelse:
                if isinstance(arg, ast.If):
                    self.ifControl[node.col_offset] = "elif"
                    self.visit(arg)
                else:
                    self.all_concepts_map.append("Declaração de condicional (else)")

                    self.all_concepts_map.append("[INICIO ESCOPO ELSE]")

                    for concept in node.body:
                        self.visit(concept)

                    self.all_concepts_map.append("[FINAL ESCOPO ELSE]")

        return

    # ============================= REPETITIONS ===============================
    def visit_For(self, node):
        self.all_concepts_map.append("Declaração de repetição FOR")

        self.all_concepts_map.append("[INICIO ESCOPO FOR]")

        for concept in node.body:
            self.visit(concept)

        self.all_concepts_map.append("[FINAL ESCOPO FOR]")

        return

    def visit_While(self, node):
        self.all_concepts_map.append("Declaração de repetição WHILE")

        self.all_concepts_map.append("[INICIO ESCOPO WHILE]")

        for concept in node.body:
            self.visit(concept)

        self.all_concepts_map.append("[FINAL ESCOPO WHILE]")

        return
    # ------------------ FUNCTION CALLS -----------------
    def visit_Call(self, node):
        func_name_info = self.visit(node.func)
        func_name = func_name_info[1]
        func_args = node.args

        if self.func_natural_meaning(func_name):
            self.all_concepts_map.append(self.func_natural_meaning(func_name))
            # ---------------- INPUT --------------
            if func_name == "input":
                return ["Call", "str"]
            # ---------------- PRINT --------------
            elif func_name == "print":
                if len(func_args) > 1:
                    self.all_concepts_map.append("Concatenação")
                else:
                    func_arg_print = self.visit(func_args[0])

                    if func_arg_print[0] == "Name":
                        self.all_concepts_map.append("variável (já declarada)")
                    elif func_arg_print[0] == "Constant":
                        self.all_concepts_map.append(self.value_meaning(func_arg_print[1]))
                    elif func_arg_print[0] == "Op":
                        self.all_concepts_map.append(func_arg_print[1])
            # ---------------- CONVERSIONS --------------
            elif func_name == "int" or func_name == "str" or func_name == "float":
                self.all_concepts_map.append("Leitura de dado do teclado")
                return ["Call", func_name]
        return

    # ------------------ OPERATIONS -----------------
    def visit_BinOp(self, node):
        var_left = self.visit(node.left)

        if isinstance(node.left, ast.BinOp) or isinstance(node.right, ast.BinOp):
            return ["Op", astor.to_source(node)[1:-2]]
            #return ["Op", "equação matemática"]

        var_right = self.visit(node.right)
        op = ast.dump(node.op)

        if var_left[0] == "Name":
            var_left = self.var_map[var_left[1]][1]
        elif var_left[0] == "Constant":
            if len(var_right) == 3:
                var_left = [var_left[1], var_left[2]]
            else:
                var_left = var_left[1]
        if var_right[0] == "Name":
            var_right = self.var_map[var_right[1]][1]
        elif var_right[0] == "Constant":
            if len(var_right) == 3:
                var_right = [var_right[1], var_right[2]]
            else:
                var_right = var_right[1]

        if (var_left == "str" or var_left[1] == "str") and (var_right == "str" or var_right[1] == "str"):
            return ["Op", "Concatenação"]

        else:
            if isinstance(var_left, list) and isinstance(var_right, list):
                return ["Op", self.operation_meaning(op) + " de numeros"]
            elif isinstance(var_left, list):
                return ["Op", self.operation_meaning(op) + " de var por " + str(var_left[1])]
            elif isinstance(var_right, list):
                return ["Op", self.operation_meaning(op) + " de var por " + str(var_right[1])]
            else:
                return ["Op", self.operation_meaning(op) + " de variáveis"]

        return
    # ------------------- NAMES ------------------
    def visit_Name(self, node):
        return ["Name", node.id]

    # ----------------- CONSTANTS ----------------
    def visit_Constant(self, node):
        return ["Constant", type(node.value).__name__, node.value]

    def func_natural_meaning(self, func_name):
        try:
            func_map = {
                        "input": "Leitura de dado do teclado",
                        "print": "Impressão (print) de ...",
                        "str": "Conversão de dado para texto (string)",
                        "int": "Conversão de dado para inteiro (int)",
                        "float": "Conversão de dado para número decimal (float)",
                        }
            return func_map[func_name]
        except:
            return

    def value_meaning(self, func_name):
        value_map = {
                    "str": "texto (string)",
                    "int": "inteiro (int)",
                    "float": "número decimal (float)",
                    }
        return value_map[func_name]

    def operation_meaning(self, operation):
        operations_map = {"Add()": "soma",
                          "Sub()": "subtração",
                          "Div()": "divisão",
                          "Mult()": "multiplicação",
                          "Pow()": "potência",
                          "Mod()": "resto"}
        return operations_map[operation]