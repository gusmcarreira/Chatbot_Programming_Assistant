from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset

from paths import guide_docs_dir

# VARIABLES
action_eg_start = "action_eg_start"
slot_eg_message = "slot_eg_message"
slot_eg_concept = "slot_eg_concept"
slot_eg_question_index = "slot_eg_question_index"
slot_eg_question_list = "slot_eg_questions_list"
slot_eg_student_answer = "slot_eg_answer"
slot_eg_answer_from_option = "slot_eg_answer_from_option"
action_eg_followup_concept = "action_eg_followup_concept"
action_eg_check_option = "action_eg_check_options"
slot_eg_more_questions = "slot_eg_more_questions"
entity_eg_answer_option_chosen = "entity_eg_answer_option_chosen"


# Purely to reset the slot
class ActionEgResetSlotStart(Action):
    def name(self) -> Text:
        return "action_eg_reset_slot_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("slot_eg_start", None), SlotSet("slot_eg_answer", None), SlotSet("slot_eg_question_index", 0)]


class ActionEgStart(Action):
    def name(self) -> Text:
        return "action_eg_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # -- Error information --
        error_concept = tracker.get_slot(slot_eg_concept)
        error_message = tracker.get_slot(slot_eg_message).replace(" ", "_") + ".txt"
        # -----------------------
        # Path_to_file
        path_to_error_guidance_file = guide_docs_dir + error_concept + "/" + error_message
        # File text list (divided by questions/checkpoint --> -#-)
        text_doc = open(path_to_error_guidance_file, "r").read().split("-#-")
        # Get current index (which is 0, since it is the first)
        question_index = tracker.get_slot(slot_eg_question_index)
        # Send the first question to the user
        dispatcher.utter_message(text="Lembre-se se a qualquer momento quiser parar, diga PARAR")
        dispatcher.utter_message(text=returnParameter("Pergunta:", text_doc[question_index]))
        # Store the text from the file (clarifying_concept_text) and increment the index (clarifying_concept_index)
        return [SlotSet(slot_eg_question_list, text_doc)]


# Check if the answer given was correct
class ActionEgCheckAnswer(Action):
    def name(self) -> Text:
        return "action_eg_check_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Index of the current answer
        question_index = tracker.get_slot(slot_eg_question_index)
        # Real answer from the file (stored in the clarifying_concept_text slot)
        true_answer = returnParameter("Resposta:", tracker.get_slot(slot_eg_question_list)[question_index])

        # Answer given by the user
        if tracker.get_slot(slot_eg_student_answer):
            student_answer = tracker.get_slot(slot_eg_student_answer)
            if student_answer.lower() == ("parar" or "para"):
                #dispatcher.utter_message(response="utter_anything_else")
                return [FollowupAction("utter_anything_else")]
        # Answer chosen by the user (if it was not in text then it was clicked (button))
        else:
            student_answer = next(tracker.get_latest_entity_values(entity_eg_answer_option_chosen), None)

        # ------------- ANSWER WAS CORRECT MOVE ONTO NEXT ONE -------------
        if findWholeWord(true_answer, student_answer):
            dispatcher.utter_message(response="utter_congratulate")

            return [SlotSet(slot_eg_student_answer, None), SlotSet(slot_eg_answer_from_option, False), FollowupAction(action_eg_followup_concept)]

        # --- ANSWER WAS NOT CORRECT, DISPLAY OPTIONS IF THERE ARE ANY, ELSE GIVE THE ANSWER ----
        else:
            if returnParameter("Opções:", tracker.get_slot(slot_eg_question_list)[question_index]) and (not tracker.get_slot(slot_eg_answer_from_option)):
                # Reset answer slot // Send options of answers
                return [SlotSet(slot_eg_student_answer, None), FollowupAction(action_eg_check_option)]
            else:
                concise_answer = returnParameter("Explicação", true_answer)
                if concise_answer:
                    dispatcher.utter_message(text=concise_answer)
                else:
                    dispatcher.utter_message(text="A resposta é: " + true_answer)

                return [SlotSet(slot_eg_student_answer, None), SlotSet(slot_eg_answer_from_option, False), FollowupAction(action_eg_followup_concept)]


# Check if there are options
class ActionEgCheckOptions(Action):

    def name(self) -> Text:
        return "action_eg_check_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get question number
        question_index = tracker.get_slot(slot_eg_question_index)
        # Real answer from the file (stored in the clarifying_concept_text slot)
        true_answer = returnParameter("Resposta:", tracker.get_slot(slot_eg_question_list)[question_index])

        # -------------------- THERE ARE OPTIONS ----------------
        if returnParameter("Opções:", tracker.get_slot(slot_eg_question_list)[question_index]):
            buttons = []
            # Display options
            for option in returnParameter("Opções:", tracker.get_slot(slot_eg_question_list)[question_index]).split("//"):
                payload = ('"' + option + '"')
                buttons.append({"title": option, "payload": payload})
            dispatcher.utter_message(response="utter_refresh_memory", buttons=buttons)

            return [SlotSet(slot_eg_answer_from_option, True), FollowupAction(action_eg_followup_concept)]

        # ------- THERE ARE NO OPTIONS THEREFORE GIVE ANSWER -------
        else:
            # Check for concise answer
            concise_answer = returnParameter("Explicação", true_answer)
            if concise_answer:
                dispatcher.utter_message(text=concise_answer)
            else:
                dispatcher.utter_message(text="A resposta é: " + true_answer)

            return[FollowupAction(action_eg_followup_concept)]



# Check if there are anymore questions
# Check if it is a checkpoint
# If not, send next
class ActionEgFollowUpConcept(Action):
    def name(self) -> Text:
        return "action_eg_followup_concept"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Index of the next answer
        question_index = tracker.get_slot(slot_eg_question_index) + 1
        wanted_question = tracker.get_slot(slot_eg_question_list)[question_index]
        # THERE ARE MORE QUESTIONS
        if returnParameter("Pergunta:", wanted_question):
            dispatcher.utter_message(text=returnParameter("Pergunta:", tracker.get_slot(slot_eg_question_list)[question_index]))
            return [SlotSet(slot_eg_question_index, question_index)]

        # LAST QUESTION --> CHECKPOINT
        else:
            wanted_question = returnParameter("Checkpoint:", wanted_question)
            dispatcher.utter_message(text=wanted_question)
            return [FollowupAction("action_restart")]
            #return [SlotSet(slot_eg_more_questions, None)]


# Function to check if the answer is in the user's message
def findWholeWord(real_answer, user_answer):
    for i in real_answer.split(" "):
        if i not in user_answer.split(" "):
            return False
    return True


# Get wanted parameter from string (i.e, Pergunta, Opções, Resposta, Explicação)
def returnParameter(parameter, wanted_string):
    wanted_info = parameter
    for x in wanted_string.split("\n"):
        if wanted_info in x:
            return x.replace(wanted_info, '')