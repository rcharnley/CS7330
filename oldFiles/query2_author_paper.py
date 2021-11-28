import re

#import certifi
from pymongo import MongoClient

# parameter setting
connection_string = "mongodb+srv://rcharnley:ljfsRYJzLQJv0I0C@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "ProjectCS7330"
authors_collection_name = "Authors"

# connection protocol
client = MongoClient(connection_string)
db = client.get_database(database_name)
authors_collection = db.get_collection(authors_collection_name)

# query a author name
def query_author(first_name=None, last_name=None):

    # query the title of the paper and return the base information
    filter = []
    if first_name is not None and len(first_name):
        filter.append({"first_name": re.compile(first_name, re.IGNORECASE)})
    if last_name is not None and len(last_name):
        filter.append({"last_name": re.compile(last_name, re.IGNORECASE)})

    if len(filter):
        author_filter = {"$and": filter}
    else:
        author_filter = {}
    author_cursor = authors_collection.find(author_filter)

    # Store papers as list
    listOfPapersByAuthor = []
    for document in author_cursor:
        for paper in document['papers']:
            listOfPapersByAuthor.append(paper)
    
    return listOfPapersByAuthor


def print_result(papers):
    for paper in papers:
        print(paper)
    print('------------------')


if __name__ == "__main__":

    print_result(query_author('Siddhant', 'Arora'))
    print_result(query_author(first_name='Siddhant'))
    print_result(query_author(last_name='Arora'))
    print_result(query_author(first_name='Sidd.*'))
    print_result(query_author(last_name='Aro.*'))