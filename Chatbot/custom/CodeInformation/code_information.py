import ast

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
        var_meaning = "Declaração de variável COM "
        var_name = self.visit(node.targets[0])[1]
        var_value = self.visit(node.value)

        if var_value[0] == "Call":
            self.all_concepts_map.append(var_meaning + var_value[1])
            var_value = var_value[2]
        elif var_value[0] == "Constant":
            self.all_concepts_map.append(var_meaning + self.value_meaning(var_value[2]))
            var_value = var_value[2]
        elif var_value[0] == "Op":
            self.all_concepts_map.append(var_meaning + var_value[1])
            var_value = var_value[2]

        self.var_map[var_name] = var_value
    # =============================== FUNCTIONS ===============================
    def visit_FunctionDef(self, node):
        func_name = node.name
        func_args = node.args.args

        if len(func_args) == 0:
            self.all_concepts_map.append("Declaração de função")
        else:
            self.all_concepts_map.append("Declaração de função com argumento/s")
        for concept in node.body:
            self.visit(concept)
        return

    def visit_Return(self, node):
        self.all_concepts_map.append("Retorno de função")
    # ============================== CONDITIONS ===============================
    def visit_If(self, node):
        if node.col_offset not in self.ifControl:
            self.all_concepts_map.append("Declaração de condicional (if)")
        else:
            if self.ifControl[node.col_offset] == "elif":
                self.all_concepts_map.append("Declaração de condicional (elif)")

        for concept in node.body:
            self.visit(concept)

        if node.orelse:
            for arg in node.orelse:
                if isinstance(arg, ast.If):
                    self.ifControl[node.col_offset] = "elif"
                    self.visit(arg)
                else:
                    self.all_concepts_map.append("Declaração de condicional (else)")
                    for concept in node.body:
                        self.visit(concept)

        return

    # ============================= REPETITIONS ===============================
    def visit_For(self, node):
        self.all_concepts_map.append("Declaração de repetição FOR")
        for concept in node.body:
            self.visit(concept)
        return

    def visit_While(self, node):
        self.all_concepts_map.append("Declaração de repetição WHILE")
        for concept in node.body:
            self.visit(concept)

    # ------------------ FUNCTION CALLS -----------------
    def visit_Call(self, node):
        func_name_info = self.visit(node.func)
        func_name = func_name_info[1]
        func_args = node.args
        if func_name == "input":
            return ["Call", self.func_natural_meaning(func_name), "str"]
        elif func_name == "print":
            print_meaning = "Impressão DE "
            if len(func_args) > 1:
                print_meaning = print_meaning + "concatenação DE "
                for index, arg in enumerate(func_args):
                    arg = self.visit(arg)
                    if arg[0] == "Name":
                        print_meaning = print_meaning + "valor de variável"
                    elif arg[0] == "Constant":
                        print_meaning = print_meaning + self.value_meaning(arg[2])
                    if index + 1 != len(func_args):
                        print_meaning = print_meaning + " COM "
            else:
                arg = self.visit(func_args[0])
                if arg[0] == "Name":
                    print_meaning = print_meaning + "valor de variável"
                else:
                    print_meaning = print_meaning + self.value_meaning(arg[2])
            self.all_concepts_map.append(print_meaning)
        elif self.func_natural_meaning(func_name):
            return ["Call", self.func_natural_meaning(func_name), func_name]
        else:
            if func_args:
                self.all_concepts_map.append("Chamada de função com argumento/s")
            else:
                self.all_concepts_map.append("Chamada de função")
        return

    # ------------------ OPERATIONS -----------------
    def visit_BinOp(self, node):
        # --> Operação mais complexa <--
        if isinstance(node.left, ast.BinOp) or isinstance(node.right, ast.BinOp):
            return ["Op", "equação matemática", "float"]
        # ------------------------------
        var_left = self.visit(node.left)
        var_right = self.visit(node.right)
        op = ast.dump(node.op)
        op_meaning = ""
        op_type = ""
        # ---> OPERAÇÃO COM VARIÁVEIS <---
        if var_left[0] == "Name" and var_right[0] == "Name":
            var_left_value = self.var_map[var_left[1]]
            var_right_value = self.var_map[var_right[1]]
            # --> CONCATENAÇÃO <--
            if var_left_value == "str" and var_right_value == "str":
                op_meaning = "concatenação de variáveis"
                op_type = "string"
            # --> OPERAÇÃO <--
            else:
                op_meaning = self.operation_meaning(op)
                if var_left_value == "float" or var_right_value == "float":
                    op_type = "float"
                else:
                    op_type = "int"
        # ---> OPERAÇÃO COM VARIÁVEL E CONSTANTE <---
        elif var_left[0] == "Name" and var_right[0] == "Constant":
            if var_right[2] == "str":
                op_meaning = "concatenação de variável COM texto"
                op_type = "string"
            else:
                op_meaning = self.operation_meaning(op)
        # ---> OPERAÇÃO COM CONSTANT E VARIÁVEL <---
        elif var_left[0] == "Constant" and var_right[0] == "Name":
            if var_right[2] == "str":
                op_meaning = "concatenação de texto COM variável"
                op_type = "string"
            else:
                op_meaning = self.operation_meaning(op)
                if var_left[2] == "float" or var_left[2] == "float":
                    op_type = "float"
                else:
                    op_type = "int"
        # ---> OPERAÇÃO COM CONSTANTES <---
        else:
            op_meaning = self.operation_meaning(op)
        return ["Op", op_meaning, op_type]
    # ------------------- NAMES ------------------
    def visit_Name(self, node):
        return ["Name", node.id]

    # ----------------- CONSTANTS ----------------
    def visit_Constant(self, node):
        return ["Constant", node.value, type(node.value).__name__]

    def func_natural_meaning(self, func_name):
        try:
            func_map = {
                        "input": "dado do teclado",
                        "print": "Impressão (print) de ...",
                        "str": "conversão de dado para texto (string)",
                        "int": "conversão de dado para inteiro (int)",
                        "float": "conversão de dado para número decimal (float)",
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