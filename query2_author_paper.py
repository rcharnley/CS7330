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
def query_author(firstName, lastName):

    # query the title of the paper and return the base information
    author_filter = {"First Name": firstName, "Last Name": lastName}
    author_cursor = authors_collection.find(author_filter)

    # Store papers as list
    listOfPapersByAuthor = []
    for document in author_cursor:
        for paper in document['Papers']: 
            listOfPapersByAuthor.append(paper)
    
    return listOfPapersByAuthor
