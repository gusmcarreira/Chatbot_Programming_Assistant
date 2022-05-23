from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import FollowupAction, ActiveLoop

class ValidateFormEgStart(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_eg_start"

    async def extract_slot_eg_start(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        wanted_intent = tracker.latest_message['intent'].get('name')

        if wanted_intent == "affirm":
            return {"slot_eg_start": True}
        elif wanted_intent == "deny":
            #ERRO AJUDA PARADA
            dispatcher.utter_message(response="ERRO AJUDA PARADA")
            return {"slot_eg_start": False}
        elif wanted_intent == "EXTERNAL_CODE_MESSAGE":
            #print(tracker.latest_message['intent'].get('name'))
            return [FollowupAction("form_eh_start")]
            #return {"slot_eg_start": tracker.latest_message["text"]}
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
        elif wanted_intent == "EXTERNAL_ERROR_MESSAGE":
            # print(tracker.latest_message['intent'].get('name'))
            return [FollowupAction("form_eg_start")]
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
        student_answer = tracker.latest_message["text"]
        wanted_intent = tracker.latest_message['intent'].get('name')
        if wanted_situation == "Conclusion":
            if wanted_intent != "affirm" and wanted_intent != "deny" and wanted_intent != "EXTERNAL_ERROR_MESSAGE":
                dispatcher.utter_message(text="Responda apenas sim ou não")
                return {"slot_eh_answer": None}
            else:
                student_answer = wanted_intent
        return {"slot_eh_answer": student_answer}