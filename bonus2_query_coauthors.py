from pymongo import MongoClient
import query2_author_paper as queryByAuthor
import query1_paper_information as queryByTitle

# parameter setting
connection_string = "mongodb+srv://rcharnley:ljfsRYJzLQJv0I0C@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "ProjectCS7330"
authors_collection_name = "Authors"
papers_collection_name = "Papers"

# connection protocol
client = MongoClient(connection_string)
db = client.get_database(database_name)
authors_collection = db.get_collection(authors_collection_name)
papers_collection = db.get_collection(papers_collection_name) 

def buildCoAuthorsList(coAuthorsMap):
    coAuthorsSet = set(())
    for values in coAuthorsMap.values():
        coAuthorsSet.update(values)
    return list(coAuthorsSet)
    
def onlyCoAuthors(authors, firstName, lastName):
    name = firstName + " " + lastName
    authors.remove(name)
    return authors

def findCoAuthors(listOfPapers, firstName, lastName): 
    coAuthorsMap = {}
    for paper in listOfPapers: 
        paperInfo = queryByTitle.query_paper(paper)
        if paperInfo:
            coAuthors = onlyCoAuthors(paperInfo.get("Author"), firstName, lastName)
        if coAuthors:
            coAuthorsMap.update({paperInfo.get("Title"): coAuthors})
    return coAuthorsMap

# helper function
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

# helper function
def printDictionary(dict): 
    for key in dict:
        print(key, '->', dict[key])

def query_co_author(firstName, lastName):
    # BUILD LEVEL 0
    # query papers by author 
    level0ListOfPapers = queryByAuthor.query_author(firstName, lastName)
    # map of papers with co-authors 
    level0CoAuthorsMap = findCoAuthors(level0ListOfPapers, firstName, lastName)
    level0CoAuthorsList = buildCoAuthorsList(level0CoAuthorsMap)
    # print(level0CoAuthorsMap)
    # print(level0CoAuthorsList)

    # BUILD LEVEL 1
    level1CoAuthorsMap = {}
    for author in level0CoAuthorsList: 
        name = author.split(' ', 1)
        tempListOfPapers = queryByAuthor.query_author(name[0], name[1])
        tempMap = findCoAuthors(tempListOfPapers, name[0], name[1])
        level1CoAuthorsMap = Merge(level1CoAuthorsMap, tempMap)
    level1CoAuthorsList = buildCoAuthorsList(level1CoAuthorsMap)
    level0CoAuthorsSet = set((level0CoAuthorsList))
    level1CoAuthorsSet = set((level1CoAuthorsList))
    level1CoAuthorsList = list(level1CoAuthorsSet.difference(level0CoAuthorsSet))
    # print(level0CoAuthorsList)
    # print(level1CoAuthorsList)

    # BUILD LEVEL 2
    level2CoAuthorsMap = {}
    for author in level1CoAuthorsList:
        name = author.split(' ', 1)
        tempListOfPapers = queryByAuthor.query_author(name[0], name[1])
        tempMap = findCoAuthors(tempListOfPapers, name[0], name[1])
        level2CoAuthorsMap = Merge(level2CoAuthorsMap, tempMap)
    level2CoAuthorsList = buildCoAuthorsList(level1CoAuthorsMap)
    level1CoAuthorsSet = set((level1CoAuthorsList))
    level2CoAuthorsSet = set((level2CoAuthorsList))
    level2CoAuthorsList = list(level2CoAuthorsSet.difference(level1CoAuthorsSet))
    # print(level0CoAuthorsList)
    # print(level1CoAuthorsList)
    # print(level2CoAuthorsList)

    # BUILD LEVEL 3
    level3CoAuthorsMap = {}
    for author in level2CoAuthorsList: 
        name = author.split(' ', 1)
        tempListOfPapers = queryByAuthor.query_author(name[0], name[1])
        tempMap = findCoAuthors(tempListOfPapers, name[0], name[1])
        level3CoAuthorsMap = Merge(level3CoAuthorsMap, tempMap)
    level3CoAuthorsList = buildCoAuthorsList(level2CoAuthorsMap)
    level2CoAuthorsSet = set((level2CoAuthorsList))
    level3CoAuthorsSet = set((level3CoAuthorsList))
    level3CoAuthorsList = list(level3CoAuthorsSet.difference(level2CoAuthorsSet))
    print()
    print(level0CoAuthorsList)
    print()
    print(level1CoAuthorsList)
    print()
    print(level2CoAuthorsList)
    print()
    print(level3CoAuthorsList)

query_co_author("Martin", "Grohe")