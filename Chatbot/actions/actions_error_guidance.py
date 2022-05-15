from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, ActiveLoop
#AllSlotsReset

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

        return [SlotSet("slot_eg_start", None), SlotSet("slot_eg_answer", None), SlotSet("slot_eg_question_index", 0),
                SlotSet("slot_eh_start", None)]


# Function to START asking the questions
class ActionEgStart(Action):
    def name(self) -> Text:
        return "action_eg_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # -- Error information from slots --
        error_concept = tracker.get_slot(slot_eg_concept)
        error_message = tracker.get_slot(slot_eg_message)

        # -- Path_to_file (using the error information) --
        path_to_error_guidance_file = returnFilePath(error_concept, error_message)
        # File text list (divided by questions/checkpoint --> -#-)
        text_doc = open(path_to_error_guidance_file, "r").read().split("-###-")

        # Send the first question to the user
        dispatcher.utter_message(text="Lembre-se se a qualquer momento quiser parar, diga PARAR")
        dispatcher.utter_message(text=returnParameter("Pergunta:", text_doc[0]))

        # Check for initial options
        if returnParameter("Opções_Iniciais", text_doc[0]):
            # Display initial options in a form of buttons
            dispatcher.utter_message(buttons=returnButtons("Opções_Iniciais:", text_doc[0]))

        # Store all the questions information in slot
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
        # Current question information
        current_question = tracker.get_slot(slot_eg_question_list)[question_index]
        # Real answer from the file (previously stored in the clarifying_concept_text slot)
        true_answer = returnParameter("Resposta:", current_question)
        # Answer given by the user
        student_answer = tracker.get_slot(slot_eg_student_answer)

        # Check if user asked to stop
        if student_answer.lower() == "parar" or student_answer.lower() == "para":
            dispatcher.utter_message(response="ERRO AJUDA PARADA")
            return [FollowupAction("utter_anything_else")]

        # ------------- ANSWER WAS CORRECT MOVE ONTO NEXT ONE -------------
        if findWholeWord(true_answer, student_answer):
            # Congratulate student
            dispatcher.utter_message(response="utter_congratulate")
            # Send student further explanation
            concise_answer = returnParameter("Explicação", true_answer)
            dispatcher.utter_message(text=concise_answer)

            # Reset answer slot and Return next question
            return [SlotSet(slot_eg_student_answer, None), FollowupAction(action_eg_followup_concept), SlotSet(slot_eg_answer_from_option, False)]

        # --- ANSWER WAS NOT CORRECT, DISPLAY OPTIONS IF THERE ARE ANY, ELSE GIVE THE ANSWER ----
        else:
            # --> There are options
            if returnParameter("Opções:", current_question) and (not tracker.get_slot(slot_eg_answer_from_option)):
                # Display options
                dispatcher.utter_message(response="utter_refresh_memory", buttons=returnButtons("Opções:", current_question))
                # Reset answer slot and Set the from_options slot to True and Activate answer loop
                return [SlotSet(slot_eg_student_answer, None), SlotSet(slot_eg_answer_from_option, True), ActiveLoop("form_eg_answer")]
            # --> There are no options
            else:
                # Not correct message -> "Almost"
                dispatcher.utter_message(text="Quase!")
                # Send student answer/explanation
                concise_answer = returnParameter("Explicação:", current_question)
                dispatcher.utter_message(text=concise_answer)

                # Reset answer slot and Set from_options slot to False and Return next question
                return [SlotSet(slot_eg_student_answer, None), SlotSet(slot_eg_answer_from_option, False), FollowupAction(action_eg_followup_concept)]


# Followup Questions
class ActionEgFollowUpConcept(Action):
    def name(self) -> Text:
        return "action_eg_followup_concept"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Index of the next question (increment)
        question_index = tracker.get_slot(slot_eg_question_index) + 1
        # Next question
        wanted_question = tracker.get_slot(slot_eg_question_list)[question_index]

        # THERE ARE MORE QUESTIONS
        if returnParameter("Pergunta:", wanted_question):
            # Ask question
            dispatcher.utter_message(text=returnParameter("Pergunta:", wanted_question))
            # Check for initial options
            if returnParameter("Opções_Iniciais:", wanted_question):
                # Send options as buttons
                dispatcher.utter_message(buttons=returnButtons("Opções_Iniciais:", wanted_question))

                return [SlotSet(slot_eg_question_index, question_index), SlotSet(slot_eg_answer_from_option, True)]
            return [SlotSet(slot_eg_question_index, question_index)]
        # LAST QUESTION --> CHECKPOINT
        else:
            wanted_question = returnParameter("Checkpoint:", wanted_question)
            dispatcher.utter_message(text=wanted_question)
            return [FollowupAction("action_restart")]


# Function to check if the answer is in the user's message
def findWholeWord(real_answer, user_answer):
    # Remove white spaces
    real_answer = real_answer.replace(" ", "").replace("\n", "")
    user_answer = user_answer.replace(" ", "")
    for i in real_answer.split("<sep>"):
        if i in user_answer:
            return True
    return False


# Get wanted parameter from string (Pergunta, Opções_Iniciais, Opções, Resposta, Explicação, Checkpoint)
def returnParameter(parameter, wanted_string):
    wanted_info = parameter
    # Each parameter ends with |end|
    for x in wanted_string.split("<end>"):
        if wanted_info in x:
            return x.replace(wanted_info, '')


def returnButtons(parameter, wanted_list):
    buttons = []
    for option in returnParameter(parameter, wanted_list).split("<sep>"):
        payload = ('"' + option + '"')
        buttons.append({"title": option, "payload": payload})
    return buttons


def returnFilePath(error_concept, error_string):
    mainPath = guide_docs_dir
    # Each path on txt file is divided by -#-
    text_doc = open(mainPath + error_concept + ".txt", "r").read().split("-###-")

    for j, item in enumerate(text_doc):
        text_doc[j] = item.replace('\n', '')
        # The file has the following organization: Condição sem comparação-->Condição/semComparacao.txt
        # Meaning: Error message-->path_to_file
        line = text_doc[j].split("-->")
        if line[0] == error_string:
            # Return the path to the wanted file according to the error message
            return mainPath + line[1]

