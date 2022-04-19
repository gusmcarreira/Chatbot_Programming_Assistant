from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from custom.modelqa import answer_questions_model
from custom.search_documents import search_in_documents
from custom.get_whole_answer import get_wanted_whole_answer
from paths import doc_idx_directory


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
        # context = search_in_documents(question)

        if context:
            # Get answer from the Whoosh document
            answer = answer_questions_model(context[0], question)[0]
            # Get the whole text of the answer
            wanted_answer = get_wanted_whole_answer(answer, doc_idx_directory + context[1])
            wanted_sugestions = ""
        else:
            wanted_answer = ""

        # Check for suggestions (of next questions to ask)
        suggestions = check_sugestions(wanted_answer)
        # If there were suggestions set the answer to the given answer
        # And suggestions to true suggestions
        if isinstance(suggestions, tuple):
            wanted_answer = suggestions[0]
            suggestions = suggestions[1].split("<sep>")

        # Check if the student ask for example, and send only the example
        if question_intent == "ask_example":
            if len(wanted_answer.split("Exemplo:")) > 1:
                wanted_answer = "Um exemplo seria:\n" + wanted_answer.split("Exemplo:")[1]
            else:
                wanted_answer = "Desculpe, de momento não me lembro de nenhum exemplo!"
        # If the student asked for example but there were none
        else:
            if not wanted_answer:
                wanted_answer = "Desculpe estou com dificuldades a responder 😥! Vou treinar para a próxima conseguir ajudar!"

        # SEND ANSWER TO STUDENT
        dispatcher.utter_message(text=wanted_answer)

        # SEND SUGGESTIONS IF ANY
        if isinstance(suggestions, list):
            dispatcher.utter_message(text="Algumas sugestões de temas relacionados:")
            buttons = []
            for option in suggestions:
                payload = ('"' + option + '"')
                buttons.append({"title": option, "payload": payload})
            dispatcher.utter_message(buttons=buttons)

        return []
    
def check_sugestions(wanted_answer):
    split_sugestions = wanted_answer.split("Sugestões:")

    if len(split_sugestions) == 2:
        return split_sugestions[0], split_sugestions[1]
    else:
        return wanted_answer