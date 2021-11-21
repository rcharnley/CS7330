from pymongo import MongoClient

# parameter setting
connection_string = "mongodb+srv://mwisniewski:nzMIpgjB96hUS2vO@cluster0.817yp.mongodb.net/Cluster0?retryWrites=true&w=majority"
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

    for document in paper_cursor:
        print(document['Title'])
        print(*document['Authors'], sep=", ")
        print(document['URL'])
        print(document['Page Number'])
        print(*document['Publication'], sep=", ")
    print()

    # query the title of the paper and return the publication information
    publication_filter = {"Papers": paper}
    publication_cursor = publication_collection.find(publication_filter)

    for document in publication_cursor:
        for info in document["conference_info"]:
            print(document["Name"])
            print(info["Iteration"])
            print(info["Year"])
            print(info["Location"])
            print()

query_paper("Paper1")
