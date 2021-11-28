from pymongo import MongoClient

# parameter setting
#connection_string = "mongodb+srv://rcharnley:ljfsRYJzLQJv0I0C@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE"
#database_name = "ProjectCS7330"
#authors_collection_name = "Authors"

# connection protocol
#client = MongoClient(connection_string)
#db = client.get_database(database_name)
#authors_collection = db.get_collection(authors_collection_name)


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


def insertAuthor(firstName, lastName, affiliation, papers):
    authors_dict = {}
    authors_dict["first_name"] = firstName
    authors_dict["last_name"] = lastName
    authors_dict["affiliation"] = []

    for employer in affiliation:
        employer_dict = {}
        employer_dict["name"] = employer[0]
        employer_dict["start_date"] = employer[1]
        employer_dict["end_date"] = employer[2]
        authors_dict["affiliation"].append(employer_dict)

    authors_dict["papers"] = papers

    return authors_dict

if __name__=="__main__":
    # connection protocol
    myclient = MongoClient("mongodb+srv://rcharnley:ljfsRYJzLQJv0I0C@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE")
    mydb = myclient["ProjectCS7330"]
    mycol = mydb["Authors"]

    # call this function for multiple affiliation inserts
    _authorAffiliation("Raytheon", "2021-11-01")
    _authorAffiliation("Southern Methodist", "2020-11-01", "2021-11-01")

    # call this function for multiple paper inserts
    _authorPapers("paper1")
    _authorPapers("paper2")
    _authorPapers("paper3")

    # this is the final author list to be inserted into mongodb
    a = insertAuthor("Rosemary", "Charnley", affiliation, papers)
    print(a)

    x = mycol.insert_one(a)
    print(x.acknowledged)
    