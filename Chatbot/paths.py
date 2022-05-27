# Location used --> actions/actions_error_guidance.py
guide_docs_dir = "./custom/Docs/ErrorGuidance/"
# Location used --> actions/actions_answer_questions.py
main_dir = "custom/Docs/MyDocuments/"
# Location used --> actions/actions_error_help.py
main_dir_error_messages_explanation = "custom/Docs/ErrorMessagesExamples/"

dic_answers = {

    # ===========================> CONDITIONS <============================
    "ask_cond_general": [main_dir + "Condicoes/Condicionais.txt", 0],
    "ask_cond_if": [main_dir + "Condicoes/Condicionais.txt", 1],
    "ask_cond_else": [main_dir + "Condicoes/Condicionais.txt", 2],
    "ask_cond_elif": [main_dir + "Condicoes/Condicionais.txt", 3],
    "ask_cond_indent": [main_dir + "Condicoes/Condicionais.txt", 4],
    # =====================================================================

    # ==========================> INPUT/OUTPUT <===========================
    "ask_input": [main_dir + "Entrada_Saida/Entradas_Saidas.txt", 0],
    "ask_output": [main_dir + "Entrada_Saida/Entradas_Saidas.txt", 1],
    # =====================================================================

    # =============================> ERRORS <==============================
    "ask_name_error": [main_dir + "Erros/NameErrors.txt", 0],
    "ask_syntax_error": [main_dir + "Erros/SyntaxErrors.txt", 0],
    "ask_type_error": [main_dir + "Erros/TypeErrors.txt", 0],
    # =====================================================================

    # ============================> FUNCTIONS <============================
    "ask_func_general": [main_dir + "Funcoes/Funcoes.txt", 0],
    "ask_func_parameters": [main_dir + "Funcoes/Funcoes.txt", 1],
    "ask_func_return": [main_dir + "Funcoes/Funcoes.txt", 2],
    "ask_func_indent": [main_dir + "Funcoes/Funcoes.txt", 3],
    # =====================================================================

    # ==============================> LOOPS <==============================
    "ask_loop_general": [main_dir + "Repetições/Loops.txt", 0],
    "ask_loop_while": [main_dir + "Repetições/Loops.txt", 1],
    "ask_loop_for": [main_dir + "Repetições/Loops.txt", 2],
    "ask_loop_indent": [main_dir + "Repetições/Loops.txt", 3],
    # =====================================================================

    # ===========================> MOTIVATION <============================
    "ask_motiv_programming": [main_dir + "Motivação/Aprender_a_Programar.txt", 0],
    "ask_motiv_python": [main_dir + "Motivação/Aprender_Python.txt", 1],
    "ask_motiv_python_applications": [main_dir + "Motivação/Aprender_Python.txt", 0],
    # =====================================================================

    # ============================> OPERATORS <============================
    "ask_op_arithmetic": [main_dir + "Operadores/Operadores_Aritméticos.txt", 0],
    "ask_op_arithmetic_add": [main_dir + "Operadores/Operadores_Aritméticos.txt", 1],
    "ask_op_arithmetic_sub": [main_dir + "Operadores/Operadores_Aritméticos.txt", 2],
    "ask_op_arithmetic_multi": [main_dir + "Operadores/Operadores_Aritméticos.txt", 3],
    "ask_op_arithmetic_div": [main_dir + "Operadores/Operadores_Aritméticos.txt", 4],
    "ask_op_arithmetic_rem": [main_dir + "Operadores/Operadores_Aritméticos.txt", 6],
    "ask_op_arithmetic_exp": [main_dir + "Operadores/Operadores_Aritméticos.txt", 7],
    "ask_op_logic": [main_dir + "Operadores/Operadores_Lógicos.txt", 0],
    "ask_op_logic_and": [main_dir + "Operadores/Operadores_Lógicos.txt", 1],
    "ask_op_logic_or": [main_dir + "Operadores/Operadores_Lógicos.txt", 2],
    "ask_op_logic_not": [main_dir + "Operadores/Operadores_Lógicos.txt", 3],
    "ask_op_comparison": [main_dir + "Operadores/Operadores_Comparação.txt", 0],
    "ask_op_order": [main_dir + "Operadores/Operadores_Ordem.txt", 0],
    # =====================================================================

    # =============================> SYNTAX <==============================
    "ask_comments": [main_dir + "Sintaxe/Comentários.txt", 0],
    "ask_multi_comments": [main_dir + "Sintaxe/Comentários.txt", 1],
    # =====================================================================

    # ============================> VARIABLES <============================
    "ask_question_var": [main_dir + "Variáveis/Variáveis.txt", 0],
    "ask_question_var_name": [main_dir + "Variáveis/Variáveis.txt", 1],
    "ask_question_var_types": [main_dir + "Variáveis/TiposDados.txt", 0],
    "ask_question_var_get_type": [main_dir + "Variáveis/TiposDados.txt", 1],
    "ask_question_var_strings": [main_dir + "Variáveis/Strings.txt", 0],
    "ask_question_var_strings_convert": [main_dir + "Variáveis/Strings.txt", 1],
    "ask_question_var_strings_concat" :[main_dir + "Variáveis/Strings.txt", 2] ,
    "ask_question_var_ints": [main_dir + "Variáveis/Int.txt", 0],
    "ask_question_var_ints_convert": [main_dir + "Variáveis/Int.txt", 1],
    "ask_question_var_floats": [main_dir + "Variáveis/Float.txt", 0],
    "ask_question_var_floats_convert": [main_dir + "Variáveis/Float.txt", 1],
    "ask_question_var_bools": [main_dir + "Variáveis/Bool.txt", 0],
    "ask_question_var_arrays": [main_dir + "Variáveis/Array.txt", 0],
    # =====================================================================
}

dict_error_message = {
    # ============================> VARIABLES <============================
    "Você declarou uma string, mas esqueceu de incluir as duas aspas (abertura e fechamento)": main_dir_error_messages_explanation + "Variável/stringSemAspas.txt",
    "Você declarou uma variável com número decimal e utilizou , (vírgula) quando deveria ter usado . (ponto)": main_dir_error_messages_explanation + "Variável/numeroDecimalComVirgula.txt",
    "Você declarou uma variável com dois == (igualdades) quando deveria ter usado apenas um =": main_dir_error_messages_explanation + "Variável/declaracaoVariavelComDoisIguais.txt",
    "Você utilizou espaço no nome de uma variável e isso não é permitido": main_dir_error_messages_explanation + "Variável/espacoNoNomeVariavel.txt",
    "Você tentou utilizar uma variável que não foi declarada": main_dir_error_messages_explanation + "Variável/variavelNaoDeclarada.txt",
    # =====================================================================
    # ===========================> CONDITIONS <============================
    "A instrução else não pode ter uma comparação": main_dir_error_messages_explanation + "Condição/comparacaoElse.txt",
    "Em uma condição é preciso comparar um par de informações, mas você escreveu apenas um dado": main_dir_error_messages_explanation + "Condição/apenasUmParComparacao.txt",
    "Ao utilizar if ou elif você precisa incluir uma comparação. Por exemplo: if x == a, onde x == a é a comparação": main_dir_error_messages_explanation + "Condição/semComparacao.txt",
    "Você utilizou um operador and ou or, mas escreveu eles maiúsculo": main_dir_error_messages_explanation + "Condição/andOrMaiusculo.txt",
    "A comparação de uma condição deve ser feita com dois sinais de == (igualdade), mas você utilizou apenas um =": main_dir_error_messages_explanation + "Condição/comparacaoApenasUmaIgualdade.txt",
    "Em uma condição é preciso incluir : (dois pontos) ao término da instrução. Por exemplo: if idade > 18": main_dir_error_messages_explanation + "Condição/faltaDoisPontosCondicao.txt",
    # =====================================================================
    # ============================> FUNCTIONS <============================
    "Você esqueceu de um parêntesis na declaração/uso de uma função": main_dir_error_messages_explanation + "Função/faltaParentesis.txt",
    "Você esqueceu de uma , (vírgula) para separar os parâmetros de uma função": main_dir_error_messages_explanation + "Função/faltaVirgula.txt",
    "Ao criar uma função é preciso incluir : (dois pontos) ao término da instrução. Por exemplo: def nome-funcao():": main_dir_error_messages_explanation + "Função/faltaDoisPontosFuncao.txt",
    # =====================================================================
    # ==========================> REPETITIONS <============================
    "Repetições precisam ter um : no final da linha em que são criadas. Exemplo: for x in range(5):": main_dir_error_messages_explanation + "Repetição/faltaDoisPontos.txt",
    "Em um while é preciso comparar um par de informações, mas você escreveu apenas um dado. Exemplo correto: while x <= 10:": main_dir_error_messages_explanation + "Repetição/apenasUmParComparacao.txt",
    "Ao utilizar while você precisa incluir uma comparação. Por exemplo: while x <= 10, onde x <= 10 é a comparação": main_dir_error_messages_explanation + "Repetição/semComparacao.txt",
    "Você utilizou um operador and ou or, mas escreveu eles em maiúsculo": main_dir_error_messages_explanation + "Repetição/andOrMaiusculo.txt",
    "A comparação de um while deve ser feita com dois sinais de == (igualdade), mas você utilizou apenas um =": main_dir_error_messages_explanation + "Repetição/comparacaoApenasUmaIgualdade.txt",
    "Em uma repetição é preciso incluir : (dois pontos) ao término da instrução. Por exemplo: for x in range(10):": main_dir_error_messages_explanation + "Repetição/faltaDoisPontos.txt",
    "Você não utilizou o operador in para iterar sobre uma lista, array, range ou string": main_dir_error_messages_explanation + "Repetição/faltaOperadorIn.txt",
    "Faltou um par de dados no uso do operador in. Por exemplo: for x in range(2). Onde, x e range são os dados necessários para iteração": main_dir_error_messages_explanation + "Repetição/semParDadosIn.txt",
    "Você escreveu a sintaxe do while sem uma comparação": main_dir_error_messages_explanation + "Repetição/sintaxeWhileInvalida.txt",
    "Você esqueceu de abrir ou fechar um parêntesis": main_dir_error_messages_explanation + "Repetição/faltaParentesis.txt",
    # =====================================================================
    # =========================> EDITOR MESSAGES ==========================
    "Você utilizou uma condição e está comparando as variáveis/valores com apenas uma igualdade": main_dir_error_messages_explanation + "Condição/comparacaoApenasUmaIgualdade.txt",
    "Você utilizou uma condição e não informou a variável/valor em uma comparação": main_dir_error_messages_explanation + "Condição/apenasUmParComparacao.txt",
    "Você não incluiu o sinal de comparação (>, <, >=, <=, == ou !=) na condição": main_dir_error_messages_explanation + "comparacaoSemOperador.txt",
    "Você escreveu uma condição, repetição ou função e não incluiu os : (dois pontos)": main_dir_error_messages_explanation + "Função/faltaDoisPontosFuncao.txt",
    "Você escreveu uma função ou a chamada à uma função e não colocou o parêntesis de abertura e/ou fechamento ()": main_dir_error_messages_explanation + "Função/faltaParentesis.txt",
    "Você escreveu uma String e não incluiu as aspas corretamente": main_dir_error_messages_explanation + "Variável/stringSemAspas.txt",
}