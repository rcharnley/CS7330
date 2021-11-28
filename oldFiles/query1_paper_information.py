import re

#import certifi
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
def query_paper(title=None, authors=None, publication=None):

    # query the title of the paper and return the base information
    filter = []
    if title is not None and len(title):
        filter.append({"title": re.compile(title, re.IGNORECASE)})
    if publication is not None and len(publication):
        filter.append({"publication": re.compile(publication, re.IGNORECASE)})
    if authors is not None and len(authors):
        authors_regex = []
        for author in authors:
            authors_regex.append(re.compile(author, re.IGNORECASE))
        filter.append({'authors': {"$all": authors_regex}})

    if len(filter):
        filter = {"$and": filter}
    else:
        filter = {}

    paper_cursor = papers_collection.find(filter)

    # Store Paper Info as Dictionary
    # paperInfo = {}
    #
    # for document in paper_cursor:
    #     paperInfo.update({"Title": document['Title']})
    #     paperInfo.update({"Author": [*document['Authors']]})
    #     paperInfo.update({"URL": document['URL']})
    #     paperInfo.update({"Page Number": document['Page Number']})
    #     paperInfo.update({"Publication": [*document['Publication']]})
    #
    # return paperInfo
    return paper_cursor


def print_result(papers):
    for paper in papers:
        print(paper)
    print('------------------')


if __name__ == "__main__":
    print_result(query_paper("The Meaning of Null in Databases and Programming Languages"))
    print_result(query_paper(".*database.*"))
    print_result(query_paper(authors=["Kenneth Baclawski"]))
    print_result(query_paper(authors=[".*Baclawski"]))
    print_result(query_paper("The Meaning of Null in Databases and Programming Languages", publication=".*"))
