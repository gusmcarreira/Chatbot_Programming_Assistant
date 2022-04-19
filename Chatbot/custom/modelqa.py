import transformers
from transformers import pipeline
from paths import question_answering_model
import re
#from get_whole_answer import get_wanted_whole_answer
#from paths import doc_idx_directory
#from search_documents import search_in_documents


def answer_questions_model(context, question):
    context = re.sub('Sugestões\:.+[\-\#\-]*', '', context)
    nlp = pipeline("question-answering", model=question_answering_model)
    result = nlp(question=question, context=context)
    
    return [result['answer'], round(result['score'], 4)]


"""print(f"Answer: '{result['answer']}', "
f"score: {round(result['score'], 4)}, "
f"start: {result['start']}, "
f"end: {result['end']}")"""


