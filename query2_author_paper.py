from pymongo import MongoClient

# parameter setting
connection_string = "mongodb://localhost:27017/mydatabase"
database_name = "mydatabase"
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

    for document in author_cursor:
        print(document['First Name'], document['Last Name'])
        print(*document['Papers'], sep=", ")
    print()

query_author("Bob", "Jones")