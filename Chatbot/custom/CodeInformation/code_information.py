import ast
# import astor

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

        # Keep track of variable's values
        self.var_map = {}
        # Control what concepts are being used in the algorithm
        self.concepts_map = []
        self.all_concepts_map = []

    # ========================== VARIABLES ==========================
    def visit_Assign(self, node):
        self.all_concepts_map.append("Declararação de variável")
        if "Declararação de variável" not in self.concepts_map:
            self.concepts_map.append("Declararação de variável")

        # ------ VAR VALUE -----
        new_var_value = self.visit(node.value)

        self.number_of_variables += 1
        # Keep track of the variable's values
        self.var_map[node.targets[0].id] = new_var_value
        return

    # ========================== FUNCTIONS ==========================
    def visit_FunctionDef(self, node):
        self.all_concepts_map.append("Declararação de função")
        if "Declararação de função" not in self.concepts_map:
            self.concepts_map.append("Declararação de função")
        self.number_of_functions += 1
        return

    # ========================= CONDITIONS ==========================
    def visit_If(self, node):
        self.all_concepts_map.append("Declararação de condicional")
        if "Declararação de condicional" not in self.concepts_map:
            self.concepts_map.append("Declararação de condicional")
        self.number_of_conditions += 1
        return

    # ======================== REPETITIONS ==========================
    def visit_For(self, node):
        self.all_concepts_map.append("Declararação de repetição FOR")
        if "Declararação de repetição FOR" not in self.concepts_map:
            self.concepts_map.append("Declararação de repetição FOR")
        self.number_of_repetitions_for += 1
        return

    def visit_While(self, node):
        self.all_concepts_map.append("Declararação de repetição WHILE")
        if "Declararação de repetição WHILE" not in self.concepts_map:
            self.concepts_map.append("Declararação de repetição WHILE")
        self.number_of_repetitions_while += 1
        return

    # ======================== FUNCTION CALL ========================
    def visit_Call(self, node):
        # --- Get name of function ---
        func_name = getattr(node.func, "id", None)
        func_args = node.args
        if func_args:
            for arg in func_args:
                self.visit(arg)
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
            self.all_concepts_map.append("Conversão de dado para " + conversion_meaning(func_name))
            if "Conversão de dado para " + conversion_meaning(func_name) not in self.concepts_map:
                self.concepts_map.append("Conversão de dado para " + conversion_meaning(func_name))
            self.number_of_conversions += 1
        # ----------------------------
        else:
            # self.all_concepts_map.append("Chamada de função")
            # if "Chamada de função" not in self.concepts_map:
            #     self.concepts_map.append("Chamada de função")
            pass
        # ----------------------------
        return func_name

    # ========================= OPERATIONS ==========================
    def visit_BinOp(self, node):
        # --------- LEFT VALUE ---------
        value_left_name = self.visit(node.left)
        # -------- RIGHT VALUE ---------
        value_right_name = self.visit(node.right)

        # Check what operation is being conducted
        left_value = self.var_map[value_left_name][0]
        right_value = self.var_map[value_right_name][0]

        # Check the type of the result (string or number) --> to check for concatenation
        type_result = type(left_value + right_value).__name__

        operation_meaning = self.operation_meaning(ast.dump(node.op))

        true_meaning = "Cálculo - " + operation_meaning

        if type_result == "str" and ast.dump(node.op) == "Add()":
            true_meaning = "Concatenação"
            self.number_of_concatenations += 1
        else:
            self.number_of_computations += 1

        self.all_concepts_map.append(true_meaning)
        if true_meaning not in self.concepts_map:
            self.concepts_map.append(true_meaning)

        return

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        self.all_concepts_map.append(self.conversion_meaning(type(node.value).__name__))
        return node.value

    ################ AUXILIAR FUNCTIONS ################
    # Get operators natural language (pt) meaning
    def operation_meaning(self, operation):
        operations_map = {"Add()": "soma",
                          "Sub()": "subtração",
                          "div()": "divisão",
                          "Mult()": "multiplicação",
                          "Pow()": "potência",
                          "Mod()": "resto"}
        return operations_map[operation]

    def conversion_meaning(self, func_name):
        conversion_map = {"str": "texto (string)",
                          "int": "inteiro (int)",
                          "float": "número decimal (float)"}
        return conversion_map[func_name]