import ast

class CodeInformation(ast.NodeVisitor):
    def __init__(self):
        # Control the number of each concept
        # The order also controls the order of the questions
        self.number_of_variables = 0
        self.number_of_inputs = 0
        self.number_of_conversions = 0
        self.number_of_computations = 0
        self.number_of_concatenations = 0
        self.number_of_functions = 0
        self.number_of_conditions = 0
        self.number_of_repetitions_for = 0
        self.number_of_repetitions_while = 0
        self.number_of_prints = 0
        self.ifControl = {}
        # Keep track of variable's values
        self.var_map = {}
        # Control what concepts are being used in the algorithm
        self.concepts_map = []
        self.all_concepts_map = []

    # ============================= EXPRESSION ===============================
    def visit_Expr(self, node):
        self.visit(node.value)
        return

    # =============================== VARIABLES ===============================
    def visit_Assign(self, node):
        var_name = node.targets[0].id
        self.all_concepts_map.append("Declaração de variável")
        if "Declaração de variável" not in self.concepts_map:
            self.concepts_map.append("Declaração de variável")

        if isinstance(node.value, ast.BinOp):
            new_var_value = self.visit(node.value)
            left = new_var_value[0]
            op = new_var_value[1]
            right = new_var_value[2]
            meaning_str = ""

            if (isinstance(left, str)) and (isinstance(right, str)) and (op == "Add()"):
                meaning_str = "Concatenação"
            elif (isinstance(left, int)) and (isinstance(right, str)):
                meaning_str = self.operation_meaning1(op) + " por " + str(wanted_var) + " a variável existente"
            elif (isinstance(left, str)) and (isinstance(right, int)):
                meaning_str = self.operation_meaning1(op) + " por " + str(wanted_var) + " a variável existente"

            self.all_concepts_map.append(meaning_str)
        else:
            new_var_value = self.visit(node.value)

        self.number_of_variables += 1
        # Keep track of the variable's values
        self.var_map[var_name] = new_var_value

        return

    # =============================== FUNCTIONS ===============================
    def visit_FunctionDef(self, node):
        self.all_concepts_map.append("Declaração de função")
        if "Declaração de função" not in self.concepts_map:
            self.concepts_map.append("Declaração de função")

        self.all_concepts_map.append("[INICIO ESCOPO FUNÇÃO]")

        for concept in node.body:
            self.visit(concept)

        self.number_of_functions += 1
        self.all_concepts_map.append("[FINAL ESCOPO FUNÇÃO]")

        return

    # ============================== CONDITIONS ===============================
    def visit_If(self, node):
        if node.col_offset not in self.ifControl:
            wanted_ident_start = "[INICIO ESCOPO IF]"
            wanted_ident_end = "[FINAL ESCOPO IF]"
            self.all_concepts_map.append("Declaração de condicional (if)")
            if "Declaração de condicional (if)" not in self.concepts_map:
                self.concepts_map.append("Declaração de condicional (if)")
        else:
            if self.ifControl[node.col_offset] == "elif":
                wanted_ident_start = "[INICIO ESCOPO ELIF]"
                wanted_ident_end = "[INICIO ESCOPO IF]"
                self.all_concepts_map.append("Declaração de condicional (elif)")
                if "Declaração de condicional (elif)" not in self.concepts_map:
                    self.concepts_map.append("Declaração de condicional (elif)")

        self.all_concepts_map.append(wanted_ident_start)

        for concept in node.body:
            self.visit(concept)

        self.number_of_conditions += 1
        self.all_concepts_map.append(wanted_ident_end)

        if node.orelse:
            for arg in node.orelse:
                if isinstance(arg, ast.If):
                    self.ifControl[node.col_offset] = "elif"
                    self.visit(arg)
                else:
                    self.all_concepts_map.append("Declaração de condicional (else)")
                    if "Declaração de condicional (else)" not in self.concepts_map:
                        self.concepts_map.append("Declaração de condicional (else)")

                    self.all_concepts_map.append("[INICIO ESCOPO ELSE]")

                    for concept in node.body:
                        self.visit(concept)

                    self.number_of_conditions += 1
                    self.all_concepts_map.append("[FINAL ESCOPO ELSE]")

        return

    # ============================= REPETITIONS ===============================
    def visit_For(self, node):
        self.all_concepts_map.append("Declaração de repetição FOR")
        if "Declaração de repetição FOR" not in self.concepts_map:
            self.concepts_map.append("Declaração de repetição FOR")

        self.all_concepts_map.append("[INICIO ESCOPO FOR]")

        for concept in node.body:
            self.visit(concept)

        self.number_of_repetitions_for += 1
        self.all_concepts_map.append("[FINAL ESCOPO FOR]")

        return

    def visit_While(self, node):
        self.all_concepts_map.append("Declaração de repetição WHILE")
        if "Declaração de repetição WHILE" not in self.concepts_map:
            self.concepts_map.append("Declaração de repetição WHILE")

        self.all_concepts_map.append("[INICIO ESCOPO WHILE]")

        for concept in node.body:
            self.visit(concept)

        self.number_of_repetitions_while += 1
        self.all_concepts_map.append("[FINAL ESCOPO WHILE]")

        return

    # ============================= FUNCTION CALL =============================
    def visit_Call(self, node):
        # --- Get name of function ---
        func_name = getattr(node.func, "id", None)
        func_args = node.args
        # if func_args:
        #     for arg in func_args:
        #         self.visit(arg)
        # ----------------------------
        if func_name == "print":
            self.all_concepts_map.append("Impressão (print) de dado")
            if "Impressão (print) de dado" not in self.concepts_map:
                self.concepts_map.append("Impressão (print) de dado")
            self.number_of_prints += 1
            if len(func_args) > 1:
                self.all_concepts_map.append("Concatenação")
                self.concepts_map.append("Concatenação")
                self.number_of_concatenations += 1
        # ----------------------------
        elif func_name == "input":
            self.all_concepts_map.append("Leitura de dado do teclado")
            if "Leitura de dado do teclado" not in self.concepts_map:
                self.concepts_map.append("Leitura de dado do teclado")
            self.number_of_inputs += 1
        # ----------------------------
        elif func_name == ("str" or "int" or "float"):
            self.all_concepts_map.append("Conversão de dado para " + self.conversion_meaning(func_name))
            if "Conversão de dado para " + self.conversion_meaning(func_name) not in self.concepts_map:
                self.concepts_map.append("Conversão de dado para " + self.conversion_meaning(func_name))
            self.number_of_conversions += 1
        # ----------------------------
        else:
            self.all_concepts_map.append("Chamada de função criada")
            if "Chamada de função criada" not in self.concepts_map:
                self.concepts_map.append("Chamada de função criada")
        # ----------------------------
        return

    # ============================== OPERATIONS ===============================
    def visit_BinOp(self, node):
        # --------- LEFT VALUE ---------
        value_left_name = self.visit(node.left)
        # -------- RIGHT VALUE ---------
        value_right_name = self.visit(node.right)

        # Check what operation is being conducted
        try:
            left_value = self.var_map[value_left_name]
        except:
            left_value = value_left_name
        try:
            right_value = self.var_map[value_right_name]
        except:
            right_value = value_right_name

        return [left_value, ast.dump(node.op), right_value]

    # Names
    def visit_Name(self, node):
        return node.id

    # Arrays
    def visit_List(self, node):
        self.all_concepts_map.append("Dado - Lista")
        self.concepts_map.append("Dado - Lista")
        return

    def visit_Constant(self, node):
        self.all_concepts_map.append("Dado - " + self.conversion_meaning(type(node.value).__name__))
        return node.value

    # i += 1
    def visit_AugAssign(self, node):
        meaning_str = self.operation_meaning1(ast.dump(node.op)) + " por " + str(self.visit(node.value)) + " a variável existente"
        self.all_concepts_map.append(meaning_str)
        if meaning_str not in self.concepts_map:
            self.concepts_map.append(meaning_str)
        return

    ############################ AUXILIAR FUNCTIONS ############################
    # Get operators natural language (pt) meaning
    def operation_meaning(self, operation):
        operations_map = {"Add()": "soma",
                          "Sub()": "subtração",
                          "div()": "divisão",
                          "Mult()": "multiplicação",
                          "Pow()": "potência",
                          "Mod()": "resto"}
        return operations_map[operation]

    def operation_meaning1(self, operation):
        operations_map = {"Add()": "Aumento (adição)",
                          "Sub()": "Redução (subtração)",
                          "div()": "Redução (divisão)",
                          "Mult()": "Aumento (multiplicação)"}

        return operations_map[operation]

    def conversion_meaning(self, func_name):
        conversion_map = {"str": "texto (string)",
                          "int": "inteiro (int)",
                          "float": "número decimal (float)"}
        return conversion_map[func_name]
