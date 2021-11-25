from pymongo import MongoClient

# parameter setting
connection_string = "mongodb+srv://rcharnley:ljfsRYJzLQJv0I0C@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "ProjectCS7330"
papers_collection_name = "Papers"
publication_collection_name = "Publications"

# connection protocol
client = MongoClient(connection_string)
db = client.get_database(database_name)
papers_collection = db.get_collection(papers_collection_name)
publication_collection = db.get_collection(publication_collection_name)

# query a paper title
def query_paper(paper):

    # query the title of the paper and return the base information
    title_filter = {"Title": paper}
    paper_cursor = papers_collection.find(title_filter)

    # Store Paper Info as Dictionary
    paperInfo = {}

    for document in paper_cursor:
        paperInfo.update({"Title": document['Title']})
        paperInfo.update({"Author": [*document['Authors']]})
        paperInfo.update({"URL": document['URL']})
        paperInfo.update({"Page Number": document['Page Number']})
        paperInfo.update({"Publication": [*document['Publication']]})

    return paperInfo
