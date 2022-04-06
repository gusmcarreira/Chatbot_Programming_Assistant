from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.custom.modelqa import answer_questions_model
from actions.custom.search_documents import search_in_documents
from actions.custom.get_whole_answer import get_wanted_whole_answer
from actions.paths import doc_idx_directory


# Action to answer general questions
class ActionAnswerQuestions(Action):

    def name(self) -> Text:
        return "action_answer_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get user's latest message
        question = tracker.latest_message["text"]
        # Get message's intent
        question_intent = tracker.latest_message['intent'].get('name')
        # Get message's entity
        wanted_concept = next(tracker.get_latest_entity_values("answer_concept_wanted"), None)

        # Get Whoosh text related to the entity
        context = search_in_documents(wanted_concept)
        # Get answer from the Whoosh document
        answer = answer_questions_model(context[0], question)[0]
        # Get the whole text of the answer
        wanted_answer = get_wanted_whole_answer(answer, doc_idx_directory + context[1])

        if question_intent == "ask_example":
            if len(wanted_answer.split("Exemplo:")) > 1:
                wanted_answer = "Um exemplo seria:\n" + wanted_answer.split("Exemplo:")[1]
            else:
                wanted_answer = "Desculpe, de momento não me lembro de nenhum exemplo!"

        dispatcher.utter_message(text=wanted_answer)

        return []