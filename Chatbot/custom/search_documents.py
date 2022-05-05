from whoosh.index import open_dir
from whoosh.qparser import QueryParser
# import spacy
from paths import index_directory, doc_idx_directory
# doc_idx_directory = "Docs/Whoosh/"
# index_directory = "index"

def search_in_documents(search_string):
    if "condicionais" in search_string:
        search_string.replace("condicionais", "condicional")

    if (("for" or "while") in search_string) and not (("repetição" or "instrução") in search_string):
        search_string = "repetição"

    elif (("if" or "elif" or "else") in search_string) and not (("condição" or "instrução" or "condicional") in search_string):
        search_string = "condicional"

    # ------------- LEMMATIZATION OF SEARCH STRING -----------
    # new_search_string = ""
    # # Portuguese pipeline
    # nlp = spacy.load("pt_core_news_md")
    # doc = nlp(search_string)
    # for token in doc:
    #     if token.pos_ == 'NOUN' or "ADJ":
    #         new_search_string = new_search_string + " " + token.lemma_
    # ---------------- OPENING INDEX ---------------
    ix = open_dir(doc_idx_directory + index_directory)
    # -------------- SEARCH DOCUMENTS ---------------
    # Parse a query string
    try:
        with ix.searcher() as searcher:

            query = QueryParser("content", ix.schema).parse(search_string)
            # Get only the top document
            results = searcher.search(query, limit=1)

            # By default Whoosh only pulls fragments from the first 32k characters
            results.fragmenter.charlimit = None

            return [results[0]["content"], results[0]["path"]]
    except:
        try:
            with ix.searcher() as searcher:
                query = QueryParser("content", ix.schema).parse(search_string)
                # Get only the top document
                results = searcher.search(query, limit=1)

                # By default Whoosh only pulls fragments from the first 32k characters
                results.fragmenter.charlimit = None

                return [results[0]["content"], results[0]["path"]]
        except:
            return

# print(search_in_documents("escopo de uma função"))