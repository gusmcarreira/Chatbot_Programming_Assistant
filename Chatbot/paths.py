# Location used --> actions/actions_error_guidance.py
guide_docs_dir = "./custom/Docs/ErrorGuidance/"
# Location used --> actions/actions_answer_questions.py
main_dir = "custom/Docs/MyDocuments/"
# Location used --> actions/actions_error_help.py
main_dir_error_messages_explanation = "custom/Docs/ErrorMessagesExamples/"

dic_answers = {
    # ===========================> CONDITIONS <============================
    "ask_question_testcases": [main_dir + "InfoTecnico/CasosTeste.txt", 0],
    "ask_question_average": [main_dir + "Calculos/Media.txt", 0],
    "ask_question_centimeters": [main_dir + "Calculos/MetrosParaCentimetros.txt", 0],
    "ask_question_circle_area": [main_dir + "Calculos/AreaCirculo.txt", 0],
    "ask_question_consonant": [main_dir + "Calculos/Vogais_Consoantes.txt", 0],
    "ask_question_hypotenuse": [main_dir + "Calculos/Hipotenusa.txt", 0],
    # =====================================================================

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
    "ask_loop_general": [main_dir + "Repeti????es/Loops.txt", 0],
    "ask_loop_while": [main_dir + "Repeti????es/Loops.txt", 1],
    "ask_loop_for": [main_dir + "Repeti????es/Loops.txt", 2],
    "ask_loop_indent": [main_dir + "Repeti????es/Loops.txt", 3],
    # =====================================================================

    # ===========================> MOTIVATION <============================
    "ask_motiv_programming": [main_dir + "Motiva????o/Aprender_a_Programar.txt", 0],
    "ask_motiv_python": [main_dir + "Motiva????o/Aprender_Python.txt", 1],
    "ask_motiv_python_applications": [main_dir + "Motiva????o/Aprender_Python.txt", 0],
    # =====================================================================

    # ============================> OPERATORS <============================
    "ask_op_arithmetic": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 0],
    "ask_op_arithmetic_add": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 1],
    "ask_op_arithmetic_sub": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 2],
    "ask_op_arithmetic_multi": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 3],
    "ask_op_arithmetic_div": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 4],
    "ask_op_arithmetic_rem": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 6],
    "ask_op_arithmetic_exp": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 7],
    "ask_op_square_root": [main_dir + "Operadores/Operadores_Aritm??ticos.txt", 8],
    "ask_op_logic": [main_dir + "Operadores/Operadores_L??gicos.txt", 0],
    "ask_op_logic_and": [main_dir + "Operadores/Operadores_L??gicos.txt", 1],
    "ask_op_logic_or": [main_dir + "Operadores/Operadores_L??gicos.txt", 2],
    "ask_op_logic_not": [main_dir + "Operadores/Operadores_L??gicos.txt", 3],
    "ask_op_comparison": [main_dir + "Operadores/Operadores_Compara????o.txt", 0],
    "ask_op_order": [main_dir + "Operadores/Operadores_Ordem.txt", 0],
    # =====================================================================

    # =============================> SYNTAX <==============================
    "ask_comments": [main_dir + "Sintaxe/Coment??rios.txt", 0],
    "ask_multi_comments": [main_dir + "Sintaxe/Coment??rios.txt", 1],
    # =====================================================================

    # ============================> VARIABLES <============================
    "ask_question_var": [main_dir + "Vari??veis/Vari??veis.txt", 0],
    "ask_question_var_name": [main_dir + "Vari??veis/Vari??veis.txt", 1],
    "ask_question_var_types": [main_dir + "Vari??veis/TiposDados.txt", 0],
    "ask_question_var_get_type": [main_dir + "Vari??veis/TiposDados.txt", 1],
    "ask_question_var_strings": [main_dir + "Vari??veis/Strings.txt", 0],
    "ask_question_var_strings_convert": [main_dir + "Vari??veis/Strings.txt", 1],
    "ask_question_var_strings_concat" :[main_dir + "Vari??veis/Strings.txt", 2] ,
    "ask_question_var_ints": [main_dir + "Vari??veis/Int.txt", 0],
    "ask_question_var_ints_convert": [main_dir + "Vari??veis/Int.txt", 1],
    "ask_question_var_floats": [main_dir + "Vari??veis/Float.txt", 0],
    "ask_question_var_floats_convert": [main_dir + "Vari??veis/Float.txt", 1],
    "ask_question_var_bools": [main_dir + "Vari??veis/Bool.txt", 0],
    "ask_question_var_arrays": [main_dir + "Vari??veis/Array.txt", 0],
    # =====================================================================
}

dict_error_message = {
    # ============================> VARIABLES <============================
    "Voc?? declarou uma string, mas esqueceu de incluir as duas aspas (abertura e fechamento)": main_dir_error_messages_explanation + "Vari??vel/stringSemAspas.txt",
    "Voc?? declarou uma vari??vel com n??mero decimal e utilizou , (v??rgula) quando deveria ter usado . (ponto)": main_dir_error_messages_explanation + "Vari??vel/numeroDecimalComVirgula.txt",
    "Voc?? declarou uma vari??vel com dois == (igualdades) quando deveria ter usado apenas um =": main_dir_error_messages_explanation + "Vari??vel/declaracaoVariavelComDoisIguais.txt",
    "Voc?? est?? atribuindo um valor ?? uma vari??vel com duas igualdades (==), quando deveria utilizar apenas uma igualdade. Por exemplo: x = 2": main_dir_error_messages_explanation + "Vari??vel/declaracaoVariavelComDoisIguais.txt",
    "Voc?? utilizou espa??o no nome de uma vari??vel e isso n??o ?? permitido": main_dir_error_messages_explanation + "Vari??vel/espacoNoNomeVariavel.txt",
    "Voc?? tentou utilizar uma vari??vel que n??o foi declarada": main_dir_error_messages_explanation + "Vari??vel/variavelNaoDeclarada.txt",
    "vari??vel que n??o foi declarada": main_dir_error_messages_explanation + "Vari??vel/variavelNaoDeclarada.txt",
    "Voc?? tentou utilizar uma fun????o ou vari??vel que n??o existe": main_dir_error_messages_explanation + "Vari??vel/variavelNaoDeclarada.txt",
    # =====================================================================
    # ===========================> CONDITIONS <============================
    "A instru????o else n??o pode ter uma compara????o": main_dir_error_messages_explanation + "Condi????o/comparacaoElse.txt",
    "Em uma condi????o ?? preciso comparar um par de informa????es, mas voc?? escreveu apenas um dado": main_dir_error_messages_explanation + "Condi????o/apenasUmParComparacao.txt",
    "Ao utilizar if ou elif voc?? precisa incluir uma compara????o. Por exemplo: if x == a, onde x == a ?? a compara????o": main_dir_error_messages_explanation + "Condi????o/semComparacao.txt",
    "Voc?? utilizou um operador and ou or, mas escreveu eles mai??sculo": main_dir_error_messages_explanation + "Condi????o/andOrMaiusculo.txt",
    "A compara????o de uma condi????o deve ser feita com dois sinais de == (igualdade), mas voc?? utilizou apenas um =": main_dir_error_messages_explanation + "Condi????o/comparacaoApenasUmaIgualdade.txt",
    "Em uma condi????o ?? preciso incluir : (dois pontos) ao t??rmino da instru????o. Por exemplo: if idade > 18": main_dir_error_messages_explanation + "Condi????o/faltaDoisPontosCondicao.txt",
    # =====================================================================
    # ============================> FUNCTIONS <============================
    "Voc?? esqueceu de um par??ntesis na declara????o/uso de uma fun????o": main_dir_error_messages_explanation + "Fun????o/faltaParentesis.txt",
    "Voc?? esqueceu de uma , (v??rgula) para separar os par??metros de uma fun????o": main_dir_error_messages_explanation + "Fun????o/faltaVirgula.txt",
    "Ao criar uma fun????o ?? preciso incluir : (dois pontos) ao t??rmino da instru????o. Por exemplo: def nome-funcao():": main_dir_error_messages_explanation + "Fun????o/faltaDoisPontosFuncao.txt",
    # =====================================================================
    # ==========================> REPETITIONS <============================
    "Repeti????es precisam ter um : no final da linha em que s??o criadas. Exemplo: for x in range(5):": main_dir_error_messages_explanation + "Repeti????o/faltaDoisPontos.txt",
    "Em um while ?? preciso comparar um par de informa????es, mas voc?? escreveu apenas um dado. Exemplo correto: while x <= 10:": main_dir_error_messages_explanation + "Repeti????o/apenasUmParComparacao.txt",
    "Ao utilizar while voc?? precisa incluir uma compara????o. Por exemplo: while x <= 10, onde x <= 10 ?? a compara????o": main_dir_error_messages_explanation + "Repeti????o/semComparacao.txt",
    "Voc?? utilizou um operador and ou or, mas escreveu eles em mai??sculo": main_dir_error_messages_explanation + "Repeti????o/andOrMaiusculo.txt",
    "A compara????o de um while deve ser feita com dois sinais de == (igualdade), mas voc?? utilizou apenas um =": main_dir_error_messages_explanation + "Repeti????o/comparacaoApenasUmaIgualdade.txt",
    "Em uma repeti????o ?? preciso incluir : (dois pontos) ao t??rmino da instru????o. Por exemplo: for x in range(10):": main_dir_error_messages_explanation + "Repeti????o/faltaDoisPontos.txt",
    "Voc?? n??o utilizou o operador in para iterar sobre uma lista, array, range ou string": main_dir_error_messages_explanation + "Repeti????o/faltaOperadorIn.txt",
    "Faltou um par de dados no uso do operador in. Por exemplo: for x in range(2). Onde, x e range s??o os dados necess??rios para itera????o": main_dir_error_messages_explanation + "Repeti????o/semParDadosIn.txt",
    "Voc?? escreveu a sintaxe do while sem uma compara????o": main_dir_error_messages_explanation + "Repeti????o/sintaxeWhileInvalida.txt",
    "Voc?? esqueceu de abrir ou fechar um par??ntesis": main_dir_error_messages_explanation + "Repeti????o/faltaParentesis.txt",
    # =====================================================================
    # =========================> EDITOR MESSAGES ==========================
    "Voc?? utilizou uma condi????o e est?? comparando as vari??veis/valores com apenas uma igualdade": main_dir_error_messages_explanation + "Condi????o/comparacaoApenasUmaIgualdade.txt",
    "Voc?? utilizou uma condi????o e n??o informou a vari??vel/valor em uma compara????o": main_dir_error_messages_explanation + "Condi????o/apenasUmParComparacao.txt",
    "Voc?? n??o incluiu o sinal de compara????o (>, <, >=, <=, == ou !=) na condi????o": main_dir_error_messages_explanation + "comparacaoSemOperador.txt",
    "Voc?? escreveu uma condi????o, repeti????o ou fun????o e n??o incluiu os : (dois pontos)": main_dir_error_messages_explanation + "Fun????o/faltaDoisPontosFuncao.txt",
    "Voc?? escreveu uma fun????o ou a chamada ?? uma fun????o e n??o colocou o par??ntesis de abertura e/ou fechamento ()": main_dir_error_messages_explanation + "Fun????o/faltaParentesis.txt",
    "Voc?? escreveu uma String e n??o incluiu as aspas corretamente": main_dir_error_messages_explanation + "Vari??vel/stringSemAspas.txt",
}

arr_dicas = [
    # Ol?? mundo!
    "947713cc-17bf-11eb-adc1-0242ac120002",
    # Pequeno problema
    "76e4017f-6006-476f-8b47-88b0e33dbf84",
    # Concatenando strings - l
    "73e1e529-5972-4ab0-bc80-bf2859d45f2b",
    # Concatenando strings - ll
    "f369a1f7-c333-4c23-81ac-89639608eb35",
    # Bingo
    "c8c40972-17c0-11eb-adc1-0242ac120002",
    # Soma
    "71b67722-4639-4fcf-be03-574356d5b70a",
    # Convertendo de metros para cent??metros
    "4ad830c8-9c86-481a-93d7-8d91a08e36ce",
    # Soma - II
    "c61d439b-5131-4377-b08a-5704d554e7ea",
    # Qual o antecessor e o sucessor
    "43789fa2-b614-4e03-a8c8-1494b3e3d9e0",
    # ??rea do c??rculo
    "38bd2aec-f62f-475e-b010-20af623db20e",
    # Diferen??a do produto
    "c7cd8e92-da1a-412a-a0b3-4498d031545a",
    # Alugando um ve??culo
    "fc14f42a-fbfd-4503-b688-1f2102cc4ac9",
    # C??lculo da hipotenusa
    "33e2bda7-f130-4320-bb85-78b76a2db5cc",
    # Digitou a letra a?
    "88bd1120-54da-4e5f-837a-c92adf5b5ea8",
    # R??pido demais
    "047fe3c5-f517-4f50-8e42-42d1f633aeba",
    # Digitou o n??mero 5?
    "d213e854-5ccf-4f2e-a9bd-60320f79330c",
    # Pequeno problema
    "d3f96e29-b446-4706-af49-e9abd0febcd2",
    # Qual ?? o sexo - Parte 1
    "25024c58-e46c-4d43-a089-d9c24e96d4ed",
    # Fui aprovado?
    "da8487c1-a381-438e-963a-6f5a8b3a152e",
    # Quantos estudantes foram aprovados
    "ecd37459-f7bb-49a2-80d0-c2b26ca332ef",
    # Fui aprovado? - Parte II
    "7dc16a56-7e81-4fc7-9ba8-90c913fb8108",
    # Menor de 2 - Parte I
    "2916d33e-6045-40f2-88da-6742231e4cf4",
    # Fui aprovado - parte III
    "26d8deb3-3e65-4129-8927-6173aaec54a7",
    # N??meros em ordem crescente
    "116a15b2-5e51-41bc-9cc2-3504b4c8f49e",
    # M??ltiplo de 5
    "f2fce5f8-6e9a-4807-bec5-901e821c1318",
    # Menor de tr??s
    "d850c341-937f-4436-902e-0bbb5d0f7eb3",
    # Qual ?? o sexo - Parte II
    "8425f9da-bf08-4a91-8f57-82158eaf1acb",
    # Digitou a letra a? - Parte II
    "271061cf-9e0b-4206-9382-2b55138bcb91",
    # R??pido demais? - Parte II
    "fed3aea4-c17a-4800-98ff-73943cd62247",
    # C??digo secreto
    "e7cd1250-dcaa-464e-9b07-cbcbf658226f",
    # C??digo secreto - Parte II
    "91e0c9e7-69c7-4a8f-b84d-00b52be3f1d3",
    # ?? vogal?
    "560a0bc3-0d5d-42a7-a6c1-0dba987bfc6a",
    # Aumento no sal??rio
    "73d29cd6-e65e-461a-b08b-02afc519b784",
    #
    "",]