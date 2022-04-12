from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from paths import index_directory, doc_idx_directory


def search_in_documents(search_string):
    # ---------------- OPENING INDEX ---------------
    ix = open_dir(doc_idx_directory + index_directory)
    # -------------- SEARCH DOCUMENTS ---------------
    # Create a search object
    searcher = ix.searcher()

    # Parse a query string
    with ix.searcher() as searcher:

        query = QueryParser("content", ix.schema).parse(search_string)
        # Get only the top document
        results = searcher.search(query, limit=1)

        # By default Whoosh only pulls fragments from the first 32k characters
        results.fragmenter.charlimit = None
        return [results[0]["content"], results[0]["path"]]


search_in_documents('um nome e o dado que armazena')
'''
def search_relevant_terms(search_string):
    # ---------------- OPENING INDEX ---------------
    ix = open_dir(doc_idx_directory + index_directory)
    # -------------- SEARCH DOCUMENTS ---------------
    # Create a search object
    searcher = ix.searcher()

    """qp = QueryParser('content', ix.schema)
q = qp.parse(unicode('id:1'))
with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
    scoring.TFIDF().scorer(searcher_tfidf, 'body', 'algebra').score(q.matcher(searcher_tfidf))
with ix.searcher(weighting=scoring.BM25F()) as searcher_bm25f:
    scoring.BM25F().scorer(searcher_bm25f, 'body', 'algebra').score(q.matcher(searcher_bm25f))"""

    # Parse a query string
    q = QueryParser("content", ix.schema).parse(search_string)

    with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
        x = scoring.TFIDF().scorer(searcher_tfidf, 'body', 'algebra').score(q.matcher(searcher_tfidf))
        print(x)
    with ix.searcher(weighting=scoring.BM25F()) as searcher_bm25f:
        y = scoring.BM25F().scorer(searcher_bm25f, 'body', 'algebra').score(q.matcher(searcher_bm25f))

search_relevant_terms("variáveis")'''