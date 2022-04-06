import transformers
from transformers import pipeline
from ..paths import question_answering_model
#from get_whole_answer import get_wanted_whole_answer
#from paths import doc_idx_directory
#from search_documents import search_in_documents


def answer_questions_model(context, question):

    nlp = pipeline("question-answering", model=question_answering_model)
    result = nlp(question=question, context=context)

    """print(f"Answer: '{result['answer']}', "
          f"score: {round(result['score'], 4)}, "
          f"start: {result['start']}, "
          f"end: {result['end']}")"""

    return [result['answer'], round(result['score'], 4)]


"""wanted_concept = "Python"
question = "Para que serve Python?"
# Get Whoosh text related to the entity
context = search_in_documents(wanted_concept)
# Get answer from the Whoosh document
answer = answer_questions_model(context[0], question)
# Get the whole text of the answer
wanted_answer = get_wanted_whole_answer(answer, doc_idx_directory + context[1])

print(wanted_answer)"""
