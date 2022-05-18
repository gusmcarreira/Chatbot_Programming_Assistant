import ast


class CodeInformation(ast.NodeVisitor):
    def __init__(self):
        # Keep track of variable's values
        self.var_map = {}
        # Control what concepts are being used in the algorithm
        self.all_concepts_map = []
        self.concepts_questions_arr = []
        # Check if it comes from print
        self.isPrint = False
        self.ifControl = {}

    # ------------------------ VARIABLES --------------------
    def visit_Assign(self, node):
        var_meaning = "Declaração de variável COM "
        # Append concept question to array
        self.append_questions("var")

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
            # Append concept question to array
            self.append_questions("func")

        else:
            self.all_concepts_map.append("Declaração de função com argumento/s")
            # Append concept question to array
            self.append_questions("func_args")

        for concept in node.body:
            self.visit(concept)
        return

    def visit_Return(self, node):
        self.all_concepts_map.append("Retorno de função")
        # Append concept question to array
        self.append_questions("func_return")

    # ============================== CONDITIONS ===============================
    def visit_If(self, node):
        if node.col_offset not in self.ifControl:
            self.all_concepts_map.append("Declaração de condicional (if)")
            # Append concept question to array
            self.append_questions("if")

        else:
            if self.ifControl[node.col_offset] == "elif":
                self.all_concepts_map.append("Declaração de condicional (elif)")
                # Append concept question to array
                self.append_questions("elif")

        for concept in node.body:
            self.visit(concept)

        if node.orelse:
            for arg in node.orelse:
                if isinstance(arg, ast.If):
                    self.ifControl[node.col_offset] = "elif"
                    self.visit(arg)
                else:
                    self.all_concepts_map.append("Declaração de condicional (else)")
                    # Append concept question to array
                    self.append_questions("else")

                    for concept in node.body:
                        self.visit(concept)
        return

    # ============================= REPETITIONS ===============================
    def visit_For(self, node):
        self.all_concepts_map.append("Declaração de repetição FOR")
        # Append concept question to array
        self.append_questions("for")

        for concept in node.body:
            self.visit(concept)
        return

    def visit_While(self, node):
        self.all_concepts_map.append("Declaração de repetição WHILE")
        # Append concept question to array
        self.append_questions("while")
        # Append concept question to array - condition information
        self.visit(node.test)

        for concept in node.body:
            self.visit(concept)

    def visit_AugAssign(self, node):
        op_meaning = self.operation_meaning(ast.dump(node.op))
        value = self.visit(node.value)
        self.all_concepts_map.append(op_meaning + " de " + str(value[1]) + " a variável")
        return

    def visit_Compare(self, node):
        self.append_questions("op_rel")

    def visit_BoolOp(self, node):
        for value in node.values:
            self.visit(value)

        self.append_questions("op_log")

    # ------------------ FUNCTION CALLS -----------------
    def visit_Call(self, node):
        func_name_info = self.visit(node.func)
        func_name = func_name_info[1]
        func_args = node.args
        if func_name == "input":
            # Append concept question to array
            self.append_questions("input")

            return ["Call", self.func_natural_meaning(func_name), "str"]
        elif func_name == "print":
            print_meaning = "Impressão DE "
            # Append concept question to array
            self.append_questions("print")

            if len(func_args) > 1:
                print_meaning = print_meaning + "concatenação DE "
                # Append concept question to array
                self.append_questions("concatenação")

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
            # Append concept question to array
            self.append_questions("func_name")
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
            # Append concept question to array
            self.append_questions("ordem_operações")
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
                # Append concept question to array
                self.append_questions("concatenação")

                op_meaning = "concatenação de variáveis"
                op_type = "string"
            # --> OPERAÇÃO <--
            else:
                op_meaning = self.operation_meaning(op)
                # Append concept question to array
                self.append_questions(op_meaning)
                if var_left_value == "float" or var_right_value == "float":
                    op_type = "float"
                else:
                    op_type = "int"
        # ---> OPERAÇÃO COM VARIÁVEL E CONSTANTE <---
        elif var_left[0] == "Name" and var_right[0] == "Constant":
            if var_right[2] == "str":
                # Append concept question to array
                self.append_questions("concatenação")

                op_meaning = "concatenação de variável COM texto"
                op_type = "string"
            else:
                op_meaning = self.operation_meaning(op)
        # ---> OPERAÇÃO COM CONSTANT E VARIÁVEL <---
        elif var_left[0] == "Constant" and var_right[0] == "Name":
            if var_right[2] == "str":
                # Append concept question to array
                self.append_questions("concatenação")
                op_meaning = "concatenação de texto COM variável"
                op_type = "string"
            else:
                op_meaning = self.operation_meaning(op)
                # Append concept question to array
                self.append_questions(op_meaning)
                if var_left[2] == "float" or var_left[2] == "float":
                    op_type = "float"
                else:
                    op_type = "int"
        # ---> OPERAÇÃO COM UMA VARIÁVEL <---
        elif var_left[0] == "Name" and var_right[0] == "Name":
            isvar_left = var_left[0] == "Name"
            isvar_right = var_right[0] == "Name"
            if not isvar_left:
                if isvar_left[2] == "str":
                    # Append concept question to array
                    self.append_questions("concatenação")
                    op_meaning = "concatenação de texto COM variável"
                    op_type = "string"
            else:
                if isvar_right[2] == "str":
                    # Append concept question to array
                    self.append_questions("concatenação")
                    op_meaning = "concatenação de texto COM variável"
                    op_type = "string"
            op_meaning = self.operation_meaning(op)
            # Append concept question to array
            self.append_questions(op_meaning)
        # ---> OPERAÇÃO COM CONSTANTES <---
        else:
            if var_left[2] == "str" and var_right[2] == "str":
                # Append concept question to array
                self.append_questions("concatenação")
                op_meaning = "concatenação de texto COM variável"
                op_type = "string"
            else:
                op_meaning = self.operation_meaning(op)
                # Append concept question to array
                self.append_questions(op_meaning)

        return ["Op", op_meaning, op_type]

    # ------------------- NAMES ------------------
    def visit_Name(self, node):
        return ["Name", node.id]

    # ----------------- CONSTANTS ----------------
    def visit_Constant(self, node):
        type_node = type(node.value).__name__
        # Append concept question to array
        self.append_questions(self.value_meaning(type_node))
        return ["Constant", node.value, type_node]

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

    def append_questions(self, concept):
        concept_map = {
            "texto (string)": "O que é uma string?",
            "inteiro (int)": "O que é um número inteiro?",
            "número decimal": "O que é um número decima (float)?",
            "str": "Como se converte um dado em texto (string)?",
            "int": "Como se converte um dado em inteiro?",
            "float": "Como se converte um dado em número decimal (float)?",
            "soma": "Como se faz uma soma em Python?",
            "subtração": "Como se faz uma subtração em Python?",
            "multiplicação": "Como se faz uma multiplicação em Python?",
            "divisão": "Como se faz a divisão em Python?",
            "potência": "Como se faz a exponenciação em Python?",
            "resto": "Como se obtém o resto em Python?",
            "concatenação": "Como se faz uma concatenação?",
            "input": "Como se lê um dado do teclado?",
            "print": "Como se imprime um dado na tela?",
            "var": "Como se se declara uma variável?",
            "func": "Como se declara uma função?",
            "func_args": "Como se declara uma função com parâmetros?",
            "func_return": "O que é o retorno de uma função?",
            "if": "Como se declara uma condicional if?",
            "elif": "Como se declara uma condicional elif?",
            "else": "Como se declara uma condicional else?",
            "for": "Como se declara uma repetição for?",
            "while": "Como se declara uma repetição while?",
            "ordem_operações": "Qual a ordem em que os operdares matemáticos são avaliados?",
            "op_rel": "Quais são os operadores usados nas comparações (relacionais)?",
            "op_log": "Quais são os operadores lógicos?",
        }

        if concept_map[concept] not in self.concepts_questions_arr:
            self.concepts_questions_arr.append(concept_map[concept])