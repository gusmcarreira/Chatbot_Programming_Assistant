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
            dispatcher.utter_message(text='Gostaria de um diálogo sobre a possivel causa do seu erro (sim/não)')
        else:
            dispatcher.utter_message(text='Se quiser falar de outra coisa responda "não", se quiser ajuda com o seu erro diga "sim"')
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"slot_eg_start": None}


class ValidateFormEgAnswer(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_eg_answer"

    async def extract_slot_eg_answer(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        wanted_intent = tracker.latest_message['intent'].get('name')
        student_answer = tracker.latest_message["text"]

        if wanted_intent == "EXTERNAL_CODE_MESSAGE":
            dispatcher.utter_message(response="utter_remember_help")
            dispatcher.utter_message(response="utter_back_to_error")
            dispatcher.utter_message(text='Qual seria então a sua resposta? Se quiser parar este diálogo diga "parar"')
            return {"slot_eg_answer": None}
        else:
            return {"slot_eg_answer": student_answer}

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
        student_answer = tracker.latest_message["text"]
        wanted_intent = tracker.latest_message['intent'].get('name')

        if wanted_situation == "Conclusion":
            if wanted_intent != "affirm" and wanted_intent != "deny" and wanted_intent != "EXTERNAL_ERROR_MESSAGE":
                dispatcher.utter_message(text="Responda apenas sim ou não")
                return {"slot_eh_answer": None}

        return {"slot_eh_answer": student_answer}

class ValidateFormTeacherHelp(FormValidationAction):
    def name(self) -> Text:
        return "validate_form_teacher_help"

    async def extract_slot_teacher_help(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:

        student_answer = tracker.latest_message["text"]
        question_parameter = "pergunta:"
        wanted_intent = tracker.latest_message['intent'].get('name')

        if question_parameter in student_answer.lower():
            dispatcher.utter_message(text="Anotado! Passerei a dúvida ao profressor logo que possível!")
            return {"slot_teacher_help": student_answer}

        elif wanted_intent != "deny":
            dispatcher.utter_message(text='Para enviar a dúvida começe a sua frase com "Pergunta:" se já não quiser diga "não"')
            return {"slot_teacher_help": None}

        else:
            return {"slot_teacher_help": student_answer}