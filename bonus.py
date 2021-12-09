import re
from database import Database
from query import Query
class Bonus: 

    def __init__(self, database, query):
        self.db = database
        self.query = query
        self.level0 = []
        self.level1 = []
        self.level2 = []
        self.level3 = []
    
    @staticmethod
    def print_result(collection):
        for document in collection:
            print(document)
        print('------------------')

    # [BONUS 1] The program should get the name of an author, and return the list of papers that he/she authored. 
    # However, if there is reason to believe that there are multiple authors that have the same name 
    # (e.g. they serve at different places in the same year, one should separate them. 
    # (Notice that sometime you may have to guess which paper belong to which author. It is ok, but specify how you make the guess).
    def query_same_name_authors(self, firstName, lastName):
        authors_collection = self.db.getAuthorsCollection()
        # query the title of the paper and return the base information
        author_filter = {"first_name": firstName, "last_name": lastName}
        author_cursor = authors_collection.find(author_filter)

        # Store papers as list and separate by latest affiliation
        listOfPapersBySameAuthor = []
        for document in author_cursor:
            listOfAuthors = []
            listOfPapers = []
            listOfAuthors.append(firstName)
            listOfAuthors.append(lastName)
            listOfAuthors.append(document["affiliation"][-1]["name"])

            for paper in document['papers']: 
                listOfPapers.append(paper)
            
            listOfAuthors.append(listOfPapers)
            listOfPapersBySameAuthor.append(listOfAuthors)

        return listOfPapersBySameAuthor

    # [BONUS 2] The program should get the name of an author, and then return all authors that have a co-auther number of at most 3. 
    # A co-author number is defined in the following number (let the input author be A)
    #       + If an author co-authored with A, then the cu-author number = 0
    #       + If an author did not co-authered with A, but co-authored with someone that has a co-author number of 0, then his/her co-author number is 1
    #       + In general, if an author did not co-authered with A or anyone with a co-author number < k, 
    #         but he co-authored a paper with someone with co-author number k, then his/her co-author number is k+1
    @staticmethod
    def buildCoAuthorsList(coAuthorsMap):
        coAuthorsSet = set(())
        for values in coAuthorsMap.values():
            coAuthorsSet.update(values)
        return list(coAuthorsSet)

    @staticmethod
    def onlyCoAuthors(authors, firstName, lastName):
        name = firstName + " " + lastName
        authors = [i for i in authors if i != name]
        return authors  

    def findCoAuthors(self, listOfPapers, firstName, lastName): 
        coAuthorsMap = {}
        for paper in listOfPapers: 
            paperInfo = self.query.query_paper(title = paper)
            coAuthors = self.onlyCoAuthors(paperInfo.get("author"), firstName, lastName)
            coAuthorsMap.update({paperInfo.get("title"): coAuthors})
        return coAuthorsMap

    # helper function
    @staticmethod
    def Merge(dict1, dict2):
        res = {**dict1, **dict2}
        return res

    # helper function
    @staticmethod
    def printDictionary(dict): 
        for key in dict:
            print(key, '->', dict[key])
    
    def query_co_author(self, firstName, lastName):
        # BUILD LEVEL 0
        # query papers by author 
        level0ListOfPapers = self.query.query_author(firstName, lastName)
        # map of papers with co-authors 
        level0CoAuthorsMap = self.findCoAuthors(level0ListOfPapers, firstName, lastName)
        level0CoAuthorsList = self.buildCoAuthorsList(level0CoAuthorsMap)
        #print(level0CoAuthorsMap)
        #print(level0CoAuthorsList)

        # BUILD LEVEL 1
        level1CoAuthorsMap = {}
        for author in level0CoAuthorsList: 
            name = author.split(' ', 1)
            tempListOfPapers = self.query.query_author(name[0], name[1])
            tempMap = self.findCoAuthors(tempListOfPapers, name[0], name[1])
            level1CoAuthorsMap = self.Merge(level1CoAuthorsMap, tempMap)
        level1CoAuthorsList = self.buildCoAuthorsList(level1CoAuthorsMap)
        level0CoAuthorsSet = set((level0CoAuthorsList))
        level1CoAuthorsSet = set((level1CoAuthorsList))
        level1CoAuthorsList = list(level1CoAuthorsSet.difference(level0CoAuthorsSet))
        # print(level0CoAuthorsList)
        # print(level1CoAuthorsList)

        # BUILD LEVEL 2
        level2CoAuthorsMap = {}
        for author in level1CoAuthorsList:
            name = author.split(' ', 1)
            tempListOfPapers = self.query.query_author(name[0], name[1])
            tempMap = self.findCoAuthors(tempListOfPapers, name[0], name[1])
            level2CoAuthorsMap = self.Merge(level2CoAuthorsMap, tempMap)
        level2CoAuthorsList = self.buildCoAuthorsList(level1CoAuthorsMap)
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
            tempListOfPapers = self.query.query_author(name[0], name[1])
            tempMap = self.findCoAuthors(tempListOfPapers, name[0], name[1])
            level3CoAuthorsMap = self.Merge(level3CoAuthorsMap, tempMap)
        level3CoAuthorsList = self.buildCoAuthorsList(level2CoAuthorsMap)
        level2CoAuthorsSet = set((level2CoAuthorsList))
        level3CoAuthorsSet = set((level3CoAuthorsList))
        level3CoAuthorsList = list(level3CoAuthorsSet.difference(level2CoAuthorsSet))
        
        self.level0 = level0CoAuthorsList
        self.level1 = level1CoAuthorsList
        self.level2 = level2CoAuthorsList
        self.level3  = level3CoAuthorsList
    
    def buildLevelListString(self):
        buildString = "Level 0 Co-Authors\n" +"-------------------------------------------\n" + str(self.level0) + "\n" + "Level 1 Co-Authors\n" + "-------------------------------------------\n" +str(self.level1)+"\n"+"Level 2 Co-Authors\n"+"-------------------------------------------\n" + str(self.level2)+"\n"+"Level 3 Co-Authors\n" + "-------------------------------------------\n" + str(self.level3)
        return buildString

if __name__=="__main__":

    # [Test Bonus Class] returns and prints bonus results for Bonus class
    '''
    myDB = Database("rcharnley", "ljfsRYJzLQJv0I0C")
    myQuery = Query(myDB)
    myBonus = Bonus(myDB, myQuery)
    myBonus.query_same_name_authors("Martin", "Grohe")
    myBonus.query_co_author("Peter", "Lindner")
    print(myBonus.buildLevelListString())
    '''

    myDB = Database("rcharnley", "ljfsRYJzLQJv0I0C")
    myQuery = Query(myDB)
    myBonus = Bonus(myDB, myQuery)
    print(myBonus.query_same_name_authors("Mike", "Wisniewski")[1])