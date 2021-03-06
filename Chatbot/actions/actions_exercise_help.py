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
slot_eh_question_id = "slot_eh_question_id"
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
        test_case_information = tracker.get_slot(slot_eh_test_case)

        # It is in a form of a string, eg, <input>2<sep><output>3
        if isinstance(test_case_information, str):
            test_case_information = tracker.get_slot(slot_eh_test_case).split("<sep>") # Separate inputs from outputs

        if test_case_information and test_case_information[0]:
            # == INPUTS ==
            if isinstance(test_case_information[0], str):
                test_case_inputs = test_case_information[0].split("<input>")
                test_case_inputs = [i for i in test_case_inputs if i] # Removing empty strings
            else:
                test_case_inputs = test_case_information[0]
            # == OUTPUTS ==
            if isinstance(test_case_information[1], str):
                test_case_outputs = test_case_information[1].split("<output>")
                test_case_outputs = [i for i in test_case_outputs if i] # Removing empty strings
            else:
                test_case_outputs = test_case_information[1]

            dispatcher.utter_message(text="Lembre-se se a qualquer momento quiser parar, diga PARAR")

            #dispatcher.utter_message(text="O primeiro passo ?? ver se compreende corretamente o que o seu algoritmo deve produzir!")
            dispatcher.utter_message(text='<text>Primeiro vamos aos Test Cases (tabela ?? direita com "entradas" - input() - e "saidas" - print()). \n\nPor vezes se houver um pormenor ou outro que n??o entenda apenas pelo enunciado, ?? bom olhar para eles.\n\nA minha sugest??o seria MENTALMENTE substituir os input() pelas entradas, e tentar perceber se acha que o seu c??digo iria gerar a saida correta')

            test_case_string = "<text>"

            if len(test_case_inputs) == 1:
                test_case_string = test_case_string + "\nUm exemplo, se a entrada fosse:\n\n" + test_case_inputs[0]

            else:
                entries = "'" + test_case_inputs[0] + "'"
                index = 1
                while index < len(test_case_inputs):
                    entries = entries + ", '" + test_case_inputs[index] + "'"
                    index += 1

                test_case_string = test_case_string + "Um exemplo, se as entradas fossem:\n\n" + entries


            if len(test_case_outputs) == 1:
                test_case_string = test_case_string + "\n\nQual diria ser as sua saida?"
            else:
                test_case_string = test_case_string + "\n\nQual diria serem as suas saidas? Separe-as com um ponto e v??rgula (;)"

            test_case_string = test_case_string + "</text>"
            dispatcher.utter_message(text=test_case_string)

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

        dispatcher.utter_message(text="Vou-lhe ent??o propor um desafio! Vou lhe dar todas as pe??as do equeleto de UMA poss??vel solu????o!")
        dispatcher.utter_message(text="N??o lhe dar?? a exata resposta (principalmente o que pertence aos escopos das func??es, condi????es, ...) mas lhe dar?? o esqueleto de uma!")
        dispatcher.utter_message(text="Analise as pe??as, selecione-as por ordem que acha que devem ser implementadas, e no final clique em enviar!")

        dispatcher.utter_message(text=conceptsOptionsButtons(answer_code_concepts))

        return [SlotSet(slot_eh_situation, "Concepts Order"), SlotSet(slot_eh_student_answer, None), SlotSet(slot_eh_concepts_options, answer_code_concepts), FollowupAction("form_eh_answer")]

# =================================================== CONCLUSION =======================================================
class ActionEhFurtherHelp(Action):
    def name(self) -> Text:
        return "action_eh_further_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="<code>Por vezes o nosso algoritmo corre mas n??o produz o que queriamos, aqui v??o algumas dicas:\n\n" +
        #                          "1 - Veja se em vez de ter usado o nome da vari??vel, n??o a envolveu em aspas tornando-a uma string\n\n" +
        #                          "2 - Verifique as suas vari??veis, poder?? estar por exemplo a fazer a subtra????o de (a - a), em vez de (a - b),  ou at?? a trocar a sua ordem fazendo (b - a)\n\n" +
        #                          "3 - Quando o exerc??cio involve produzir um texto exato, veja se escreveu corretamente (incluindo acentos, sinais de pontua????o e espa??os)\n\n" +
        #                          "4 - Quando faz uma concatena????o lembre-se que, se for preciso, tem de ser voc?? a colocar espa??o entre as palavras, ex, (x = 'Ol??' + 'Chabot'), vai gerar 'Ol??Chatbot', pois n??o inseri um espa??o no inicio/final de nenhuma das strings \n\n" +
        #                          "5 - Ao usar a fun????o range, lembre-se que esta come??a no 0 acabando 1 n??mero ANTES do que o escolhido, ex: range(3), ir?? ser do 0 ao 2</code>")

        dispatcher.utter_message(text="Aqui v??o algumas sugest??es de perguntas que possam ajudar:")
        concepts_involved = codeInformation(tracker.get_slot(slot_eh_answer_code)).concepts_questions_arr
        concepts_involved_str = "<code_print>"

        if concepts_involved:
            for index, concept in enumerate(concepts_involved):
                if index != len(concepts_involved) - 1:
                    concepts_involved_str = concepts_involved_str + concept + "\n\n\n"
                else:
                    concepts_involved_str = concepts_involved_str + concept
        concepts_involved_str = concepts_involved_str + "</code_print>"
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
        question_id = tracker.get_slot(slot_eh_question_id)

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
                dispatcher.utter_message(text="Isso mesmo ????!")
            # Incorrect answer - Show correct answer
            else:
                dispatcher.utter_message(text="N??o ?? bem isso, a resposta correta seria:")
                dispatcher.utter_message(text=produceString(test_case_slot[1], False))

                # if question_id:
                #     utter_string = "utter_" + question_id
                #     dispatcher.utter_message(response=utter_string)
                # else:
                if produceString(test_case_slot[1], False).replace("<code_print>", "").replace("</code_print>", "").replace("\n", "").isdigit():
                    dispatcher.utter_message(text = "Dica: Quando se trata de um valor n??merico, atente no enunciado, pois este ou especifica o valor, ou o c??lculo para chegar a este.")
                else:
                        dispatcher.utter_message(text = "Dica: Ao resolver o exerc??cio tenha aten????o se o enunciado especifica algum texto que o algoritmo deve imprimir, pois a falta de um pormenor, como um acento ou dois pontos, vai produzir a saida errada!")
            return [FollowupAction("action_eh_concepts_order")]
        # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        # """"""""""""""""""""""" ORDER CONCEPTS """""""""""""""""""""""""""""
        elif answer_situation == "Concepts Order":
            # second_try = tracker.get_slot(slot_eh_second_try) # Check if it is the second try
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
                dispatcher.utter_message(text="Hmm n??o ?? bem isso, a resposta correta seria:")
                #show_answer = True
            else:
                dispatcher.utter_message(text="Muito bem, ?? isso mesmo ????????, a resposta correta ?? portanto:")
                #show_answer = True

            #if show_answer:
            dispatcher.utter_message(text=produceString(correct_order, True))

            #if (not second_try) and (not show_answer):
            #    return [SlotSet(slot_eh_student_answer, None), FollowupAction("form_eh_answer"), SlotSet(slot_eh_second_try, "True")]

            dispatcher.utter_message(text="O seu ??ltimo desafio ?? transformar isto em c??digo!")

            return [SlotSet(slot_eh_student_answer, None), FollowupAction("utter_did_that_help"), SlotSet(slot_eh_situation, "Conclusion")]
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
    str_arr_wanted = str_arr_wanted + "</code_print>"
    return str_arr_wanted