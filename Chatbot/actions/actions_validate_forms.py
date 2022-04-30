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
        student_answer = tracker.latest_message["text"]

        if student_answer.lower() == ("parar" or "para"):
            return {"slot_eh_answer": student_answer}

        elif wanted_situation == "Test Case":
            return {"slot_eh_answer": student_answer}

        elif (wanted_situation == "Concepts Included") or (wanted_situation == "Concepts Order"):
            regex = "(\s*\d\s*)+"
            check_answer = re.search(regex, student_answer)
            if check_answer == None:
                # Includes something that it is not a number/white space
                dispatcher.utter_message(
                    text="A sua resposta parece conter caracters sem ser números e/ou espaços, por favor volte a escrever a sua resposta contendo apenas o número da opção, e se for mais que uma opção separe-as com um espaço (eg, 1 2 5). Lembre-se que se quiser parar, basta dizer PARAR.")
                return {"slot_eh_answer": None}
            else:
                check_answer = check_answer.span()
                # Includes only numbers and white spaces
                if (check_answer[0] == 0) and (check_answer[1] == len(student_answer)):
                    num_options = tracker.get_slot("slot_eh_concepts_options")
                    for num in student_answer.split(" "):
                        if num:
                            if int(num) >= len(num_options):
                                dispatcher.utter_message(
                                    text="A sua resposta parece conter algum número que não está entre as opções, por favor volte a escrever a sua resposta, se for mais que uma opção separe-as com um espaço (eg, 1 2 5). Lembre-se que se quiser parar, basta dizer PARAR.")
                                # There is a number higher than the available options
                                return {"slot_eh_answer": None}
                    return {"slot_eh_answer": student_answer}
                else:
                    # Includes something that it is not a number/white space
                    dispatcher.utter_message(
                        text="A sua resposta parece conter caracters sem ser números e/ou espaços, por favor volte a escrever a sua resposta contendo apenas o número da opção, e se for mais que uma opção separe-as com um espaço (eg, 1 2 5). Lembre-se que se quiser parar, basta dizer PARAR.")
                    return {"slot_eh_answer": None}

        # Check that the numbers comprise only of the options given
        elif wanted_situation == "Questions":

            # Contains letters
            if re.findall("[a-zA-Z]", student_answer):
                dispatcher.utter_message(text="A sua resposta parece conter letras, por favor escreva apenas a 1 número a representar a quantidade.")
                return {"slot_eh_answer": None}
            # Contains more than one number
            elif re.search("\s*\d+\s+\d+", student_answer):
                dispatcher.utter_message(text="A sua resposta parece conter mais que um número, por favor escreva apenas a 1 número a representar a quantidade.")
                return {"slot_eh_answer": None}
            else:
                return {"slot_eh_answer": student_answer}

        elif wanted_situation == "Conclusion":
            wanted_intent = tracker.latest_message['intent'].get('name')

            if wanted_intent == "affirm":
                # validation succeeded, set the value of the "cuisine" slot to value
                return {"slot_eh_answer": "affirm"}
            elif wanted_intent == "deny":
                # validation succeeded, set the value of the "cuisine" slot to value
                return {"slot_eh_answer": "deny"}
            else:
                # validation failed, set this slot to None so that the
                # user will be asked for the slot again
                dispatcher.utter_message(text="Por favor responda apenas, sim ou não")
                return {"slot_eh_answer": None}
        return