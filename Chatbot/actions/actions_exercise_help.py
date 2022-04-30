from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop

import ast
import random

from paths import guide_docs_dir
from custom.CodeInformation.code_information import CodeInformation

# ---------------- Slots Used ----------------
slot_eh_answer_code = "slot_eh_code_answer"
slot_eh_student_answer = "slot_eh_answer"
slot_eh_situation = "slot_eh_situation"
slot_eh_test_case = "slot_eh_test_case"
slot_eh_concepts_options = "slot_eh_concepts_options"
slot_eh_question_ask = "slot_eh_question_ask"
slot_eh_second_try = "slot_eh_second_try"
# --------------------------------------------

# =================================================== TEST CASE ========================================================
# Given x, what input should it produce? 
class ActionEhTestCase(Action):
    def name(self) -> Text:
        return "action_eh_test_case"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # --- TEST CASE information sent by the application ---
        # It is in a form of a string, eg, <input>2<sep><output>3
        # Separate inputs from outputs
        test_case_information = tracker.get_slot(slot_eh_test_case).split("<sep>")
        # == INPUTS ==
        test_case_inputs = test_case_information[0].split("<input>")
        test_case_inputs = [i for i in test_case_inputs if i] # Removing empty strings
        # == OUTPUTS ==
        test_case_outputs = test_case_information[1].split("<output>")
        test_case_outputs = [i for i in test_case_outputs if i] # Removing empty strings

        dispatcher.utter_message(text="Lembre-se se a qualquer momento quiser parar, diga PARAR")
        dispatcher.utter_message(text="O primeiro passo é ver se compreende corretamente o que o seu algoritmo deve produzir!")

        # Text language according to amount of inputs fosse (1) / fossem (more than one)
        if len(test_case_inputs) == 1:
            dispatcher.utter_message(text="Se a entrada dada ao algoritmo fosse: " + test_case_inputs[0])
        else:
            entries = test_case_inputs[0]
            index = 1
            while index < len(test_case_inputs):
                entries = entries + ", " + test_case_inputs[index]
                index += 1
            dispatcher.utter_message(text="Se as entradas dadas ao algoritmo fossem: " + entries)

        dispatcher.utter_message(text="Diga qual seria a sua saida. Se achar que é mais que uma separe-as com um ponto e vírgula (;)")

        # Save required information to use in later functions (SlotSet) and start form to ask for answer (FollowupAction)
        return [SlotSet(slot_eh_situation, "Test Case"), SlotSet(slot_eh_student_answer, None), SlotSet(slot_eh_test_case, [test_case_inputs, test_case_outputs]), FollowupAction("form_eh_answer")]

# ============================================== CONCEPTS INCLUDED =====================================================
# What concepts would you say are included on this exercise?
class ActionEhConceptsIncluded(Action):
    def name(self) -> Text:
        return "action_eh_concepts_included"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # --- All Possible Concepts ---
        options_arr = ["Declararação de variável", "Declararação de função", "Declararação de condicional",
                        "Declararação de repetição FOR", "Declararação de repetição WHILE", "Impressão (print) de dado",
                        "Concatenação", "Leitura de dado do teclado", "Conversão de dado para texto (string)",
                        "Conversão de dado para inteiro (int)", "Conversão de dado para número decimal (float)",
                        "Cálculo - soma", "Cálculo - subtração", "Cálculo - divisão", "Cálculo - multiplicação",
                        "Cálculo - potência", "Cálculo - resto"]

        # --- Answer analysis to retrieve used concepts ---
        answer_code_concepts = codeInformation(tracker.get_slot(slot_eh_answer_code)).concepts_map

        # -- Produce options array ---
        # 1. Remove all the concepts included in the answer from the options_arr
        options_arr = [concept for concept in options_arr if concept not in answer_code_concepts]
        # 2. Then retrieve three random concepts from the remaining element of the options_arr
        options_arr = random.sample(options_arr, 3)
        # 3. Create a new array with the correct concepts and the three other random concepts
        options_arr = options_arr + answer_code_concepts
        # 4. Finally shuffle array so the concepts are in no specific order
        random.shuffle(options_arr)

        dispatcher.utter_message(text="Para o resto da conversa é preciso lembrar que por vezes existem várias formas de resolver um mesmo exercício e que esta conversa é com base EM UMA maneira de o resolver, o que NÃO quer dizer que seja a ÚNICA.")
        dispatcher.utter_message(text="Continuando...agora que vimos o que o algoritmo deve produzir como saida, da seguinte lista, diga quais os conceitos que diria serem úteis para este exercício:")
        dispatcher.utter_message(text=produceString(options_arr, True))
        dispatcher.utter_message(text="Responda apenas com o número da opção e se for mais que uma separe-as com um espaço (ex, 0 3 4)")

        return [SlotSet(slot_eh_situation, "Concepts Included"), SlotSet(slot_eh_student_answer, None), SlotSet(slot_eh_concepts_options, options_arr), FollowupAction("form_eh_answer")]


# =============================================== CONCEPTS AMOUNT ======================================================
class ActionEhQuestions(Action):
    def name(self) -> Text:
        return "action_eh_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        checkpoint = tracker.get_slot(slot_eh_question_ask)

        # Ask for amount of variables
        if not checkpoint:
            checkpoint = "variables"
            dispatcher.utter_message(text="Agora que discutimos um pouco sobre os conceitos involvidos, vamos passar um pouco a quantidadde. Não lhe vou perguntar de todos os elementos, mas dos mais comus, ou seja, variaveis, entradas e saidas.")
            dispatcher.utter_message(text="Primeiro, quantas variáveis acha que são necessárias usar?")
        # Ask for amount of inputs
        elif checkpoint == "variables":
            checkpoint = "inputs"
            dispatcher.utter_message(text="Agora, analisando melhor o enunciado, quantos dados do teclado acha que se têm de ler?")
        # Ask for amount of prints
        elif checkpoint == "inputs":
            checkpoint = "prints"
            dispatcher.utter_message(text="Finalmente, quantas saidas diria serem necessárias?")

        return [SlotSet(slot_eh_situation, "Questions"), SlotSet("slot_eh_answer", None), SlotSet(slot_eh_question_ask, checkpoint), FollowupAction("form_eh_answer")]


# ================================================ ORDER CONCEPTS ======================================================
class ActionEhConceptsOrder(Action):
    def name(self) -> Text:
        return "action_eh_concepts_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # ------ Get all the concepts on the answer -------
        answer_code_concepts = codeInformation(tracker.get_slot(slot_eh_answer_code)).all_concepts_map
        random.shuffle(answer_code_concepts)

        dispatcher.utter_message(text="Ok, por fim proponho um desafio! Vou lhe dar todas as peças do meu algoritmo, tente juntá-las, mas tenha atenção a alguns aspetos:")
        dispatcher.utter_message(text="A resposta deve conter apenas o número das opções pela ordem correta e cada uma separada por um espaço (ex, 0 3 2)")
        dispatcher.utter_message(text="E se por exemplo, quiser indicar que um dado do teclado é para ser guardado numa variavel basta por o numero da opção do dado do teclado logo a seguir da opção da declaração da variavel!")

        dispatcher.utter_message(text=produceString(answer_code_concepts, True))

        return [SlotSet(slot_eh_situation, "Concepts Order"), SlotSet(slot_eh_student_answer, None), SlotSet(slot_eh_concepts_options, answer_code_concepts), FollowupAction("form_eh_answer")]

# =================================================== CONCLUSION =======================================================
class ActionEhFurtherHelp(Action):
    def name(self) -> Text:
        return "action_eh_further_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        dispatcher.utter_message(text="<code>Por vezes o nosso algoritmo corre mas não produz o que queriamos, aqui vão algumas dicas:</code>\n\n" +
                                 "<code_print>1 - Veja se em vez de ter usado o nome da variável, não a envolveu em aspas tornando-a uma string\n\n" +
                                 "<code_print>2 - Verifique as suas variáveis, poderá estar por exemplo a fazer a subtração de a - a, em vez de a - b,  ou até a trocar a sua ordem fazendo b - a\n\n" +
                                 "<code_print>3 - Quando o exercício involve produzir um text exato, veja se escreveu corretamente (incluindo acentos, sinais de pontuação e espaços)\n\n" +
                                 "<code_print>4 - Quando faz uma concatenação lembre-se que se for preciso, tem de ser você a colocar espaço entre as palavras, ex, x = 'Olá' + 'Chabot', vai gerar 'OláChatbot', pois não inseri um espaço no inicio/final de nenhuma das strings \n\n" +
                                 "<code_print>5 - Ao usar a função range, lembre-se que esta começa no 0 acabando 1 número ANTES do que o escolhido, ex: range(3), irá ser do 0 ao 2")

        dispatcher.utter_message(text="Se tiver dificuldade em algum conceito em especifico, clique no seu botão:")

        correct_order = codeInformation(tracker.get_slot(slot_eh_answer_code)).all_concepts_map
        dispatcher.utter_message(buttons=returnButtons(correct_order))
        return []

# ================================================= CHECK ANSWERS ======================================================
class ActionEhCheckAnswer(Action):
    def name(self) -> Text:
        return "action_eh_check_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get code answer
        code_answer = tracker.get_slot(slot_eh_answer_code)
        # Check what is being evaluated (Test Case, Concepts Included, Questions, Concepts Order)
        answer_situation = tracker.get_slot(slot_eh_situation)
        # Get student's answer
        student_answer = tracker.get_slot(slot_eh_student_answer)

        # Check if user asked to stop
        if student_answer.lower() == ("parar" or "para"):
            return [FollowupAction("utter_anything_else")]

        # """""""""""""""""""""""""""" TEST CASES """"""""""""""""""""""""""""
        if answer_situation == "Test Case":
            student_answer = student_answer.split(";")
            student_answer = [output.strip() for output in student_answer if output] # Remove start/end spaces
            test_case_slot = tracker.get_slot(slot_eh_test_case) # Inputs and Outputs
            # Check each output answer given by the user against correct answer
            tmp_wrong = []
            tmp_right = []

            for output in student_answer:
                if output in test_case_slot[1]:
                    tmp_right.append(output)
                else:
                    tmp_wrong.append(output)

            # Exact correct answer
            if (not tmp_wrong) and (len(tmp_right) == len(test_case_slot[1])):
                dispatcher.utter_message(text="Isso mesmo 🤌!")
            # Incorrect answer - Show correct answer
            else:
                dispatcher.utter_message(text="Não é bem isso, a resposta correta seria:")
                dispatcher.utter_message(text=produceString(test_case_slot[1], False))
                dispatcher.utter_message(text="Dica: Ao resolver o exercício tenha atenção se o enunciado especifica algum texto que o algoritmo deve imprimir, pois a falta de um pormenor como um acento ou dois pontos vai produzir a saida errada!")

            return [FollowupAction("action_eh_concepts_included")]
        # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # """"""""""""""""""""" CONCEPTS ON EXERCISE """""""""""""""""""""""""
        elif answer_situation == "Concepts Included":
            correct_concepts = codeInformation(code_answer).concepts_map # Correct Concepts
            concept_choices = tracker.get_slot(slot_eh_concepts_options) # Options displayed to the student
            student_choices = student_answer.split(" ") # Options chosen by the student
            
            wrong_concepts = []
            right_concepts = []

            for index, concept in enumerate(concept_choices):
                # Concepts chosen by the student that are one of the correct ones
                if (str(index) in student_choices) and (concept in correct_concepts):
                    right_concepts.append(concept)
                # Concepts chosen by the student but not one of the correct ones
                elif (str(index) in student_choices) and not (concept in correct_concepts):
                    wrong_concepts.append(concept)

            # Correct concepts that the student has not chosen
            missing_concepts = [concept for concept in correct_concepts if concept not in right_concepts]

            # Tried to choose every option
            if (len(right_concepts) + len(wrong_concepts)) == len(concept_choices):
                dispatcher.utter_message(text="Parece ter escolhido todas as opções, no entanto existem aqui alguns conceitos que não são propriamente úteis para este exercício, tente outra vez!")
                return [SlotSet(slot_eh_student_answer, None), FollowupAction("form_eh_answer")]

            # Student answer [EXACTLY] == Correct Answer
            if right_concepts and not wrong_concepts and not missing_concepts:
                dispatcher.utter_message(text="Acertou em todos os conceitos 😎!")

            # Student answer does not contain any right answer
            elif not right_concepts:
                dispatcher.utter_message(text="Hmm 🤔 parece que estar com algumas dificuldades em perceber que conceitos podem ser úteis ao exercício, na verdade seria mais algo como:")
                dispatcher.utter_message(text=produceString(missing_concepts, False)) # Send correct options to the student

            # Contains right options (and) wrong options
            else:
                # Student answer contains all the correct options + some wrong
                if (len(right_concepts) == len(correct_concepts)) and wrong_concepts:
                    if len(wrong_concepts) > 1:
                        dispatcher.utter_message(text="Hmm 🤔 parece ter escolhido alguns conceitos que não achámos tão relevantes para este exercício, mas escolheu todos aqueles que achámos úteis, que no caso são os seguintes:")
                    else:
                        dispatcher.utter_message(text="Hmm 🤔 escolheu um conceito que não achámos tão relevante para este exercício, mas escolheu todos aqueles que achámos mais úteis, que no caso são os seguintes:")
                    dispatcher.utter_message(text=produceString(right_concepts, False)) # Display right concepts
                # Student answer contains some correct options (meaning some missing) + some wrong
                elif wrong_concepts:
                    if len(wrong_concepts) > 1:
                        dispatcher.utter_message(text="Hmm 🤔 escolheu alguns conceitos que não achámos tão relevantes para este exercício, mas escolheu também alguns que achamos mais úteis, que no caso são os seguintes:")
                    else:
                        dispatcher.utter_message(text="Hmm 🤔 escolheu um conceito que não achámos tão relevante para este exercício, mas escolheu também alguns que achámos mais úteis, que no caso são os seguintes:")
                    dispatcher.utter_message(text=produceString(right_concepts, False)) # Display right concepts
                    dispatcher.utter_message(text="Sendo que achámos que os seguintes também seriam úteis:")
                    dispatcher.utter_message(text=produceString(missing_concepts, False)) # Display missing concepts (missing options)
                # Student answer contains some correct options (meaning some missing) but no wrong options
                else:
                    dispatcher.utter_message(text="Diriamos que todos os que escolheu são úteis, ou seja estão corretos:")
                    dispatcher.utter_message(text=produceString(right_concepts, False)) # Display right concepts
                    dispatcher.utter_message(text="Mas acicionariamos ainda os seguintes:")
                    dispatcher.utter_message(text=produceString(missing_concepts, False))  # Display missing concepts (missing options)

            return  [FollowupAction("action_eh_questions")]
        # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # == QUESTIONS ON AMOUNT OF NEEDED CONCEPT =
        elif answer_situation == "Questions":
            student_answer = int(student_answer.strip())
            checkpoint = tracker.get_slot(slot_eh_question_ask)
        
            num_wanted = 0
            text_wanted = ""
            action_wanted = "action_eh_questions"

            if checkpoint == "variables":
                num_wanted = codeInformation(code_answer).number_of_variables
                text_wanted = " variáveis"

            elif checkpoint == "inputs":
                num_wanted = codeInformation(code_answer).number_of_inputs
                text_wanted = " dados do teclado (inputs)"

            elif checkpoint == "prints":
                num_wanted = codeInformation(code_answer).number_of_prints
                if num_wanted == 1:
                    text_wanted = " print"
                else:
                    text_wanted = " prints"
                action_wanted = "action_eh_concepts_order"

            # Muitos ou poucos
            if (student_answer > (num_wanted + 4)) or (student_answer < (num_wanted - 4)):
                dispatcher.utter_message(text="A sua quantidade afasta-se um pouco daquela que usei! No meu caso foram " + str(num_wanted) + text_wanted)
            elif student_answer == num_wanted:
                dispatcher.utter_message(text="Pensámos no mesmo número de" + text_wanted + "👌!")
            else:
                dispatcher.utter_message(text="Lembrando que não há respostas erradas, por vezes você pode fazer num passo aquilo que eu faço em dois! Eu pensei mais em " + str(num_wanted) + text_wanted)

            return [FollowupAction(action_wanted)]

        # """"""""""""""""""""""" ORDER CONCEPTS """""""""""""""""""""""""""""
        elif answer_situation == "Concepts Order":
            second_try = tracker.get_slot(slot_eh_second_try) # Check if it is the second try
            # ----------- CORRECT ANSWER ---------
            correct_order = codeInformation(code_answer).all_concepts_map
            # ------------------------------------
            # ----------- STUDENT ANSWER ---------
            student_answer = student_answer.split(" ") # Get each option
            student_answer = [concept for concept in student_answer if concept] #Remove empty strings
            # ------------------------------------

            order_options = tracker.get_slot(slot_eh_concepts_options) # Options shuffled

            right_choices = []
            wrong_choices = []
            decision_arr = []

            for index, concept in enumerate(correct_order):
                if index >= len(student_answer):
                    wrong_choices.append(concept)
                    decision_arr.append("wrong")
                else:
                    if concept == order_options[int(student_answer[index])]:
                        right_choices.append(concept)
                        decision_arr.append("right")
                    else:
                        wrong_choices.append(concept)
                        decision_arr.append("wrong")
            show_answer = False
            if wrong_choices:
                # First try
                if not second_try:
                    if right_choices:
                        wanted_num_clues = round(len(wrong_choices) / 3) # To add a third of the wrong answers as a clue
                        if wanted_num_clues != 0:
                            dispatcher.utter_message(text="Não é bem isso, tente outra vez mas agora com uma ajudinha:")
                            dispatcher.utter_message(text=returnOptions(decision_arr, wanted_num_clues, correct_order))
                            if wanted_num_clues == 1:
                                dispatcher.utter_message(text="Adicionei 1 peça aquelas que já tinha juntado, tente agora!")
                            else:
                                dispatcher.utter_message(text="Adicionei " + str(wanted_num_clues) + " peças aquelas que já tinha, tente agora!")
                        else:
                            dispatcher.utter_message(text="Quase! A resposta correta seria: ")
                            show_answer = True
                    else:
                        wanted_num_clues = round(len(wrong_choices) / 3)
                        if wanted_num_clues != 0:
                            dispatcher.utter_message(text="Está com algumas dificuldade, vá outra vez mas agora com uma ajudinha:")
                            dispatcher.utter_message(text=returnOptions(decision_arr, wanted_num_clues, correct_order))
                            if wanted_num_clues == 1:
                                dispatcher.utter_message(text="Adicionei 1 peça, tente agora!")
                            else:
                                dispatcher.utter_message(text="Adicionei " + str(wanted_num_clues) + " peças, tente agora!")
                        else:
                            dispatcher.utter_message(text="Não é bem isso, a resposta correta seria:")
                            show_answer = True
                # Second try
                else:
                    dispatcher.utter_message(text="Hmm ainda não é bem isso, a resposta correta seria:")
                    show_answer = True
            else:
                dispatcher.utter_message(text="Muito bem, é isso mesmo 👏👏, a resposta correta é portanto:")
                show_answer = True

            if show_answer:
                dispatcher.utter_message(text=produceString(correct_order, True))

            if (not second_try) and (not show_answer):
                return [SlotSet(slot_eh_student_answer, None), FollowupAction("form_eh_answer"), SlotSet(slot_eh_second_try, "True")]

            dispatcher.utter_message(text="Agora tente passar para código o que discutimos!")
            dispatcher.utter_message(text="A nossa conversa ajudou-o a saber como proceder? (sim, não)")

            return [SlotSet(slot_eh_student_answer, None), FollowupAction("form_eh_answer"), SlotSet(slot_eh_situation, "Conclusion")]
        # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        # """""""""""""""""""""""""""" CONCLUSION """"""""""""""""""""""""""""
        elif answer_situation == "Conclusion":
            if student_answer == "affirm":
                return [FollowupAction("utter_anything_else")]
            else:
                return [FollowupAction("action_eh_further_help")]
        # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        return []

# ================================================ AUX FUNCTIONS ======================================================
def returnButtons(options):
    buttons = []

    for option in options:
        payload = ('"' + option + '"')
        buttons.append({"title": option, "payload": payload})
    return buttons

def returnOptions(rightArr, numAdd, arrAnswer):
    arrIndexes = []
    if numAdd > 0:
        for index, decision in enumerate(rightArr):
            if decision != "right":
                arrIndexes.append(index)
        arrIndexes = random.sample(arrIndexes, numAdd)

    newArrOptions = []
    for index, decision in enumerate(rightArr):
        if decision == "right":
            newArrOptions.append(arrAnswer[index])
        else:
            newArrOptions.append("????")

    for i in arrIndexes:
        newArrOptions[i] = arrAnswer[i]

    newStrArrOptions = "<code_print>"

    for i in newArrOptions:
        newStrArrOptions = newStrArrOptions + i + "\n"

    return newStrArrOptions

def codeInformation(code_slot):
    answer_code = code_slot.replace("<new_line><br>", "\n").replace("<tab>", "\t")
    vis_answer = CodeInformation()
    vis_answer.visit(ast.parse(answer_code))
    return vis_answer

def produceString(arr_wanted, wants_order):
    str_arr_wanted = "<code_print>"

    for index, concept in enumerate(arr_wanted):
        if wants_order:
            str_arr_wanted = str_arr_wanted + str(index) + " - " + concept + "\n"
        else:
            str_arr_wanted = str_arr_wanted + concept + "\n"

    return str_arr_wanted