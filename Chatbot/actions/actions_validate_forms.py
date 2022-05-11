from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

import re

class ValidateFormEgStart(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_eg_start"

    async def extract_slot_eg_start(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        wanted_intent = tracker.latest_message['intent'].get('name')

        if wanted_intent == "affirm":
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_eg_start": True}
        elif wanted_intent == "deny":
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_eg_start": False}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"slot_eg_start": None}


class ValidateFormEhStart(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_eh_start"

    async def extract_slot_eh_start(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        wanted_intent = tracker.latest_message['intent'].get('name')

        if wanted_intent == "affirm":
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_eh_start": True}
        elif wanted_intent == "deny":
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_eh_start": False}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"slot_eh_start": None}

class ValidateFormEhAnswer(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_eh_answer"

    async def extract_slot_eh_answer(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        wanted_situation = tracker.get_slot("slot_eh_situation")
        if wanted_situation == "Conclusion":
            wanted_intent = tracker.latest_message['intent'].get('name')
            if wanted_intent != "affirm" or wanted_intent != "deny":
                dispatcher.utter_message(text="Responda apenas sim ou não")
                return {"slot_eg_start": None}
        else:
            student_answer = tracker.latest_message["text"]

        return {"slot_eh_answer": student_answer}