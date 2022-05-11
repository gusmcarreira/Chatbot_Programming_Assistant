import transformers
from transformers import pipeline
from paths import question_answering_model
import re
#from get_whole_answer import get_wanted_whole_answer
# from paths import doc_idx_directory
#from search_documents import search_in_documents
import spacy
# from nltk.corpus import stopwords

def answer_questions_model(context, question):
    context = re.sub('Sugestões\:.+[\-\#\-]*', '', context)
    final_result = [0, "", 0]
    # threshold = 0.8
    # For each segment in the file
    for index, text in enumerate(context.split("-#-")):
        # ----------------- LEMMATIZATION -----------------
        # Portuguese pipeline
        nlp = spacy.load("pt_core_news_md")
        doc = nlp(question)
        new_search_string = ""
        for token in doc:
            if (token.pos_ == 'NOUN') or (token.pos_ == "ADJ"):
                new_search_string = new_search_string + " " + token.lemma_
            else:
                new_search_string = new_search_string + " " + token.text
        # --------------------------------------------------
        nlp = pipeline("question-answering", model=question_answering_model)
        result = nlp(question=new_search_string, context=text)
        score = result['score']
        # If score is better than the previous segment's score
        if score > final_result[2]:
            final_result = [index, result["answer"], score]
        # if score > threshold:
        #     break
    return final_result


"""print(f"Answer: '{result['answer']}', "
f"score: {round(result['score'], 4)}, "
f"start: {result['start']}, "
f"end: {result['end']}")"""


