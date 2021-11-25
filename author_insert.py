from pymongo import MongoClient

# parameter setting
connection_string = "mongodb://localhost:27017/mydatabase"
database_name = "mydatabase"
authors_collection_name = "Authors"

# connection protocol
client = MongoClient(connection_string)
db = client.get_database(database_name)
authors_collection = db.get_collection(authors_collection_name)


affiliation = []
def _authorAffiliation(companyName, startDate, endDate=""):
    global affiliation
    affiliation.append([companyName, startDate, endDate])

    # sort list by start date
    affiliation.sort(key=lambda affiliation:affiliation[1])

    return affiliation


papers = []
def _authorPapers(paper):
    global papers
    papers.append(paper)

    # sort list by paper title
    papers.sort()

    return papers


def insertAuthor(lastName, firstName, affiliation, papers):
    authors_dict = {}
    authors_dict["First Name"] = firstName
    authors_dict["Last Name"] = lastName
    authors_dict["Affiliation"] = []

    for employer in affiliation:
        employer_dict = {}
        employer_dict["Name"] = employer[0]
        employer_dict["Start Date"] = employer[1]
        employer_dict["End Date"] = employer[2]
        authors_dict["Affiliation"].append(employer_dict)

    authors_dict["Papers"] = papers

    return authors_dict

if __name__=="__main__":
    # parameter setting
    connection_string = "mongodb://localhost:27017/mydatabase"
    database_name = "mydatabase"
    authors_collection_name = "Authors"

    # connection protocol
    myclient = MongoClient(connection_string)
    mydb = myclient[database_name]
    mycol = mydb[authors_collection_name]

    # call this function for multiple affiliation inserts
    _authorAffiliation("Raytheon", "2021-11-01")
    _authorAffiliation("Southern Methodist", "2020-11-01", "2021-11-01")

    # call this function for multiple paper inserts
    _authorPapers("paper1")
    _authorPapers("paper2")
    _authorPapers("paper3")

    # this is the final author list to be inserted into mongodb
    a = insertAuthor("Wisniewski", "Mike", affiliation, papers)

    print(a)
    


