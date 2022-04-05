from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


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
