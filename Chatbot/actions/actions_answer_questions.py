from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from paths import *

slot_error_cause_information = "slot_error_cause_information"

# Action to answer general questions
class ActionAnswerQuestions(Action):

    def name(self) -> Text:
        return "action_answer_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get message's intent
        question_intent = tracker.latest_message['intent'].get('name')
        # Control if the student wants an example
        wants_example = False
        example = question_intent.split("_")
        
        if example[1] == "example":
            wants_example = True
    
        # Get base ask intent
        if wants_example:
            question_intent = ""
            for word in example:
                if word != "example":
                    question_intent = question_intent + word + "_"
            question_intent = question_intent[:-1]
    
        # Get text from file (dic_answers --> paths.py)
        path_to_file = dic_answers[question_intent][0]
        index_info_wanted = dic_answers[question_intent][1]
        whole_text_file = open(path_to_file, "r").read().split("-#-")

        answer = whole_text_file[index_info_wanted]

        # Check if the user asked for an example
        if wants_example:
            answer = get_example(answer)

        # Check for suggestions (of next questions to ask)
        answer, suggestions = check_sugestions(answer)

        # SEND ANSWER TO STUDENT
        dispatcher.utter_message(text=answer)

        # SEND SUGGESTIONS IF ANY
        if suggestions:
            dispatcher.utter_message(text="Algumas sugestões:")
            buttons = []
            for option in suggestions:
                payload = ('"' + option + '"')
                buttons.append({"title": option, "payload": payload})
            dispatcher.utter_message(buttons=buttons)

        return []

class ActionAnswerErrorQuestions(Action):
    def name(self) -> Text:
        return "action_answer_error_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get message's intent
        question_intent = tracker.latest_message['intent'].get('name')
        # Get text from file (dic_answers --> paths.py)
        path_to_file = dic_answers[question_intent][0]
        error_causes = open(path_to_file, "r").read().split("-#-")

        # Send first error cause
        answer = error_causes[0]

        # Display answer
        dispatcher.utter_message(text=answer)
        dispatcher.utter_message(text="Gostaria de saber outra possível razão deste tipo de erro?")

        return [SlotSet(slot_error_cause_information, [error_causes, 1])]


class ActionAnswerErrorQuestionsFollowup(Action):
    def name(self) -> Text:
        return "action_answer_error_questions_followup"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        error_causes_information = tracker.get_slot(slot_error_cause_information)
        errror_causes_arr = error_causes_information[0]
        error_cause_index = error_causes_information[1]

        answer = errror_causes_arr[error_cause_index]

        # Check for suggestions (of next questions to ask)
        answer, suggestions = check_sugestions(answer)

        dispatcher.utter_message(text=answer)

        # If there are suggestions, means that it is the last cause
        if suggestions:
            dispatcher.utter_message(text="Algumas sugestões:")
            buttons = []
            for option in suggestions:
                payload = ('"' + option + '"')
                buttons.append({"title": option, "payload": payload})

            dispatcher.utter_message(buttons=buttons)

            return [SlotSet(slot_error_cause_information, None)]

        dispatcher.utter_message(text="Gostaria de saber outra possível razão deste tipo de erro?")
        return [SlotSet(slot_error_cause_information, [errror_causes_arr, error_cause_index + 1])]

def check_sugestions(wanted_answer):
    split_sugestions = wanted_answer.split("Sugestões:")
    if len(split_sugestions) == 2:
        return split_sugestions[0], split_sugestions[1].split("<sep>")
    else:
        return wanted_answer, None

def get_example(wanted_answer):
    wanted_answer_example = wanted_answer.split("Exemplo:", 1)
    if len(wanted_answer_example) == 2:
        return  wanted_answer_example[1]
    else:
        return wanted_answer