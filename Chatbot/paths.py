# Location used --> actions/actions_error_guidance.py
guide_docs_dir = "./custom/Docs/ErrorGuidance/"

# Location used --> actions/actions_answer_questions.py
main_dir = "custom/Docs/MyDocuments/"

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