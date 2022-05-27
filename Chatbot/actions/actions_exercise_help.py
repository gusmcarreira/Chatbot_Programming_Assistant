from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop

import ast
import random

from paths import guide_docs_dir
from custom.CodeInformation.code_information import CodeInformation

import json
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

        test_case_information = tracker.get_slot(slot_eh_test_case).split("<sep>") # Separate inputs from outputs

        if test_case_information[0]:
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
                dispatcher.utter_message(text="Se a entrada dada ao algoritmo fosse: '" + test_case_inputs[0] + "'")
            else:
                entries = "'" + test_case_inputs[0] + "'"
                index = 1
                while index < len(test_case_inputs):
                    entries = entries + ", '" + test_case_inputs[index] + "'"
                    index += 1
                dispatcher.utter_message(text="Se as entradas dadas ao algoritmo fossem: " + entries)

            dispatcher.utter_message(text="Qual seria a sua saida? Se achar que é mais que uma separe-as com um ponto e vírgula (;)")

            # Save required information to use in later functions (SlotSet) and start form to ask for answer (FollowupAction)
            return [SlotSet(slot_eh_situation, "Test Case"), SlotSet(slot_eh_student_answer, None), SlotSet(slot_eh_test_case, [test_case_inputs, test_case_outputs]), FollowupAction("form_eh_answer")]
        else:
            return [FollowupAction("action_eh_concepts_order")]
# ================================================ ORDER CONCEPTS ======================================================
class ActionEhConceptsOrder(Action):
    def name(self) -> Text:
        return "action_eh_concepts_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # ------ Get all the concepts on the answer -------
        answer_code_concepts = codeInformation(tracker.get_slot(slot_eh_answer_code)).all_concepts_map
        answer_code_concepts = [concept for concept in answer_code_concepts if concept]

        dispatcher.utter_message(text="Vou-lhe agora propor um desafio! Vou lhe dar todas as peças de UMA possível solução!")
        dispatcher.utter_message(text="Analise as peças, selecione-as por ordem que acha que devem ser implementadas, e no final clique em enviar!")

        dispatcher.utter_message(text=conceptsOptionsButtons(answer_code_concepts))

        return [SlotSet(slot_eh_situation, "Concepts Order"), SlotSet(slot_eh_student_answer, None), SlotSet(slot_eh_concepts_options, answer_code_concepts), FollowupAction("form_eh_answer")]

# =================================================== CONCLUSION =======================================================
class ActionEhFurtherHelp(Action):
    def name(self) -> Text:
        return "action_eh_further_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="<code>Por vezes o nosso algoritmo corre mas não produz o que queriamos, aqui vão algumas dicas:\n\n" +
        #                          "1 - Veja se em vez de ter usado o nome da variável, não a envolveu em aspas tornando-a uma string\n\n" +
        #                          "2 - Verifique as suas variáveis, poderá estar por exemplo a fazer a subtração de (a - a), em vez de (a - b),  ou até a trocar a sua ordem fazendo (b - a)\n\n" +
        #                          "3 - Quando o exercício involve produzir um texto exato, veja se escreveu corretamente (incluindo acentos, sinais de pontuação e espaços)\n\n" +
        #                          "4 - Quando faz uma concatenação lembre-se que, se for preciso, tem de ser você a colocar espaço entre as palavras, ex, (x = 'Olá' + 'Chabot'), vai gerar 'OláChatbot', pois não inseri um espaço no inicio/final de nenhuma das strings \n\n" +
        #                          "5 - Ao usar a função range, lembre-se que esta começa no 0 acabando 1 número ANTES do que o escolhido, ex: range(3), irá ser do 0 ao 2</code>")

        dispatcher.utter_message(text="Aqui vão algumas sugestões de perguntas que possam ajudar:")
        concepts_involved = codeInformation(tracker.get_slot(slot_eh_answer_code)).concepts_questions_arr
        concepts_involved_str = "<code>"

        if concepts_involved:
            for index, concept in enumerate(concepts_involved):
                if index != len(concepts_involved) - 1:
                    concepts_involved_str = concepts_involved_str + concept + "\n\n"
                else:
                    concepts_involved_str = concepts_involved_str + concept + "</code>"

        dispatcher.utter_message(text=concepts_involved_str)
        # correct_concepts = [concept for concept in correct_concepts if concept]
        # dispatcher.utter_message(buttons=returnButtons(correct_concepts))
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
        if (student_answer.lower() == "parar") or (student_answer.lower() == "para"):
            return [FollowupAction("utter_anything_else")]
        elif tracker.latest_message['intent'].get('name') == "EXTERNAL_ERROR_MESSAGE":
            student_answer = student_answer.split("/EXTERNAL_ERROR_MESSAGE")[1]
            student_answer = json.loads(student_answer)
            return [ActiveLoop(None), SlotSet(slot_eh_student_answer, None), SlotSet("slot_eg_concept", student_answer["error_type"]), SlotSet("slot_eg_message", student_answer["error_message"]),FollowupAction("utter_start_error_guidance")]
        # """""""""""""""""""""""""""" TEST CASES """"""""""""""""""""""""""""
        if answer_situation == "Test Case":
            student_answer = student_answer.split(";")
            student_answer = [output.strip() for output in student_answer if output]  # Remove start/end spaces
            test_case_slot = tracker.get_slot(slot_eh_test_case)  # Inputs and Outputs
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
                if produceString(test_case_slot[1], False).isnumeric():
                    dispatcher.utter_message(text = "Dica: Quando se trata de um valor númerico, atente no enunciado, pois este ou especifica o valor, ou o cálculo para chegar a este.")
                else:
                    dispatcher.utter_message(text = "Dica: Ao resolver o exercício tenha atenção se o enunciado especifica algum texto que o algoritmo deve imprimir, pois a falta de um pormenor, como um acento ou dois pontos, vai produzir a saida errada!")
            return [FollowupAction("action_eh_concepts_order")]
        # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        # """"""""""""""""""""""" ORDER CONCEPTS """""""""""""""""""""""""""""
        elif answer_situation == "Concepts Order":
            second_try = tracker.get_slot(slot_eh_second_try) # Check if it is the second try
            # ----------- CORRECT ANSWER ---------
            correct_order = codeInformation(code_answer).all_concepts_map
            correct_order = [concept for concept in correct_order if concept]
            # ------------------------------------
            # ----------- STUDENT ANSWER ---------
            student_answer = student_answer.split("<sep>") # Get each option
            student_answer = [concept for concept in student_answer if concept] #Remove empty strings
            # ------------------------------------
            right_choices = []
            wrong_choices = []
            decision_arr = []


            for index, concept in enumerate(correct_order):
                if index >= len(student_answer):
                    wrong_choices.append(concept)
                    decision_arr.append("wrong")
                else:
                    if concept == student_answer[index]:
                        right_choices.append(concept)
                        decision_arr.append("right")
                    else:
                        wrong_choices.append(concept)
                        decision_arr.append("wrong")

            if wrong_choices:
                dispatcher.utter_message(text="Hmm não é bem isso, a resposta correta seria:")
                #show_answer = True
            else:
                dispatcher.utter_message(text="Muito bem, é isso mesmo 👏👏, a resposta correta é portanto:")
                #show_answer = True

            #if show_answer:
            dispatcher.utter_message(text=produceString(correct_order, True))

            #if (not second_try) and (not show_answer):
            #    return [SlotSet(slot_eh_student_answer, None), FollowupAction("form_eh_answer"), SlotSet(slot_eh_second_try, "True")]

            dispatcher.utter_message(text="O seu último desafio é transformar isto em código!")
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
            newArrOptions.append("")

    for i in arrIndexes:
        newArrOptions[i] = arrAnswer[i]

    newStrArrOptions = "<buttons_order_second>"

    for index, concept in enumerate(newArrOptions):
        if index == len(newArrOptions) - 1:
            newStrArrOptions = newStrArrOptions + str(index) + "<num>" + concept
        else:
            newStrArrOptions = newStrArrOptions + str(index) + "<num>" + concept + "<sep>"

    return newStrArrOptions

def conceptsOptionsButtons(answer_code_concepts):
    shuffled_answer_code_concepts = []
    for index, concept in enumerate(answer_code_concepts):
        shuffled_answer_code_concepts.append([index, concept])
    random.shuffle(shuffled_answer_code_concepts)
    order_string = "<buttons_order>"
    for index, concept in enumerate(shuffled_answer_code_concepts):
        if index == 0:
            order_string = order_string + str(concept[0]) + "<num>" + concept[1]
        else:
            order_string = order_string + "<sep>" + str(concept[0]) + "<num>" + concept[1]

    return order_string

def codeInformation(code_slot):
    answer_code = code_slot.replace("<new_line><br>", "\n").replace("<tab>", "\t")
    vis_answer = CodeInformation()
    vis_answer.visit(ast.parse(answer_code))
    return vis_answer

def produceString(arr_wanted, wants_order=False):

    str_arr_wanted = "<code_print>"

    for index, concept in enumerate(arr_wanted):
        if wants_order:
            str_arr_wanted = str_arr_wanted + str(index) + " - " + concept + "\n"
        else:
            str_arr_wanted = str_arr_wanted + concept + "\n"

    return str_arr_wanted