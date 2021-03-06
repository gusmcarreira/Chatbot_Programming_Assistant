from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop

import ast
import random

from paths import arr_dicas
from custom.CodeInformation.code_information import CodeInformation

import json
# ---------------- Slots Used ----------------
slot_eh_answer_code = "slot_eh_code_answer"
slot_eh_question_id = "slot_eh_question_id"
slot_tip_given = "slot_tip_given"
# --------------------------------------------

class ActionQuestionSuggestionsOrTip(Action):
    def name(self) -> Text:
        return "action_question_suggestions_or_tip"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tip_given = tracker.get_slot(slot_tip_given)

        question_id = tracker.get_slot(slot_eh_question_id)


        code_answer = tracker.get_slot(slot_eh_answer_code)
        concepts_involved = codeInformation(code_answer).concepts_questions_arr
        concepts_involved_str = "<code_print>"

        if concepts_involved:
            for index, concept in enumerate(concepts_involved):
                if index != len(concepts_involved) - 1:
                    concepts_involved_str = concepts_involved_str + concept + "\n\n"
                else:
                    concepts_involved_str = concepts_involved_str + concept + "</code_print>"

        dispatcher.utter_message(text="Aqui vão algumas sugestões de perguntas que possam ajudar:")
        dispatcher.utter_message(text=concepts_involved_str)

        if question_id in arr_dicas:
            if not tip_given:
                utter_string = "utter_" + question_id
                dispatcher.utter_message(response=utter_string)
                return [SlotSet(slot_tip_given, True)]

class ActionQuestionSuggestions(Action):
    def name(self) -> Text:
        return "action_question_suggestions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        code_answer = tracker.get_slot(slot_eh_answer_code)
        tip_given = tracker.get_slot(slot_tip_given)

        concepts_involved = codeInformation(code_answer).concepts_questions_arr

        concepts_involved_str = "<code_print>"
        
        if concepts_involved:
            for index, concept in enumerate(concepts_involved):
                if index != len(concepts_involved) - 1:
                    concepts_involved_str = concepts_involved_str + concept + "\n\n"
                else:
                    concepts_involved_str = concepts_involved_str + concept + "</code_print>"

        dispatcher.utter_message(text="Aqui vão algumas sugestões de perguntas que possam ajudar:")
        dispatcher.utter_message(text=concepts_involved_str)
    
        question_id = tracker.get_slot(slot_eh_question_id)

        if question_id in arr_dicas:
            if not tip_given:
                dispatcher.utter_message(text="Talvez também dê jeito uma dica:")
                buttons = [{"title": "Dica", "payload": "Dica"}]
                dispatcher.utter_message(buttons=buttons)
            
            # dispatcher.utter_message(text="Lembre-se que pode pedir a dica e as sugestões desde o inicio da questão!")

class ActionQuestionTip(Action):
    def name(self) -> Text:
        return "action_question_tip"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        question_id = tracker.get_slot(slot_eh_question_id)

        if question_id in arr_dicas:
            utter_string = "utter_" + question_id
            dispatcher.utter_message(response = utter_string)
        else:
            dispatcher.utter_message(text="Desculpe não tenho nenhuma dica para este exercício 😓")

def codeInformation(code_slot):
    answer_code = code_slot.replace("<new_line><br>", "\n").replace("<tab>", "\t")
    vis_answer = CodeInformation()
    vis_answer.visit(ast.parse(answer_code))
    return vis_answer