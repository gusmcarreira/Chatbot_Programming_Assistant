import os.path
#import docx
import os
import shutil
# For the schema fields
from whoosh.fields import Schema, TEXT
# For the Index (creating, opening)
from whoosh.index import create_in, open_dir
# Stemming
from whoosh.lang.snowball.portugese import PortugueseStemmer
from whoosh.analysis import StemmingAnalyzer, LowercaseFilter, CharsetFilter
from whoosh.support.charset import accent_map
# from paths import doc_directory, index_directory
doc_directory = "MyDocuments"
index_directory = "index"

########## 1st Create the schema ##############
def create_schema_index(index_directory):
    # -------------- CREATING SCHEMA ----------------
    stemmer_pt = PortugueseStemmer()
    stem_ana = StemmingAnalyzer(stemfn=stemmer_pt.stem) | CharsetFilter(accent_map)

    # This schema has two fields, “path” and “content”
    schema = Schema(
        path=TEXT(analyzer=stem_ana, stored=True),
        content=TEXT(analyzer=stem_ana, stored=True)
    )

    # ---------------- CREATING INDEX ---------------
    if os.path.isdir(index_directory):
        shutil.rmtree(index_directory)
    os.mkdir(index_directory)
    create_in(index_directory, schema)
    print("Index Schema Created")

############# 2nd add the documents ###############
def add_docs(index_directory):
    # ---------------- OPENING INDEX ---------------
    ix = open_dir(index_directory)

    # -------------- ADDING DOCUMENTS ---------------
    writer = ix.writer()

    # Directories where the documents are stored
    subdirectories = os.listdir(doc_directory)
    for subdirectory in subdirectories:
        if subdirectory != ".DS_Store":
            docs = os.listdir(doc_directory + "/" + subdirectory)
            for doc in docs:
                if doc != ".DS_Store":
                    path_doc = doc_directory + "/" + subdirectory + "/" + doc
                    text_doc = open(doc_directory + "/" + subdirectory + "/" + doc, "r").read()
                    writer.add_document(path=path_doc, content=text_doc)

    # Saves the added documents to the index
    writer.commit()
    print("Documents Added")


if __name__ == '__main__':
    # Create schema and index
    create_schema_index(index_directory)
    # Add documents
    add_docs(index_directory)
