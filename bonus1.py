from pymongo import MongoClient

# parameter setting
connection_string = "mongodb://localhost:27017/mydatabase"
database_name = "mydatabase"
authors_collection_name = "Authors"

# connection protocol
client = MongoClient(connection_string)
db = client.get_database(database_name)
authors_collection = db.get_collection(authors_collection_name)

def query_same_name_authors(firstName, lastName):

    # query the title of the paper and return the base information
    author_filter = {"First Name": firstName, "Last Name": lastName}
    author_cursor = authors_collection.find(author_filter)

    # Store papers as list and separate by latest affiliation
    listOfPapersBySameAuthor = []
    for document in author_cursor:
        listOfAuthors = []
        listOfPapers = []
        listOfAuthors.append(firstName)
        listOfAuthors.append(lastName)
        listOfAuthors.append(document["Affiliation"][-1]["Name"])

        for paper in document['Papers']: 
            listOfPapers.append(paper)
        
        listOfAuthors.append(listOfPapers)
        listOfPapersBySameAuthor.append(listOfAuthors)

    return listOfPapersBySameAuthor

# printing out the data
l = query_same_name_authors("Martin", "Grohe")

for author in l:
    print("Author:", author[0], author[1])
    print("Latest Employer:", author[2])
    print("Papers: ", end="")
    print(*author[3], sep=", ")
    print()
