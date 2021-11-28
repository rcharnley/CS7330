from pymongo import MongoClient

class Database:
    def __init__(self, username, password): 
        self.username = username
        self.password = password
        self.connection_string = "mongodb+srv://"+username+":"+password+"@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE"
        self.database_name = "ProjectCS7330"
        self.client = MongoClient(self.connection_string)
        self.db = self.client.get_database(self.database_name)

    # Get Papers Collections
    def getPapersCollection(self):
        collection = "Papers"
        this_collection = self.db.get_collection(collection)
        return this_collection
    
    # Test Get Papers Collections
    def testPapersCollection(self):
        papers_collection = self.getPapersCollection()
        for document in papers_collection.find():
            print(document)
    
    # Get Authors Collection
    def getAuthorsCollection(self):
        collection = "Authors"
        this_collection = self.db.get_collection(collection)
        return this_collection
    
     # Test Get Authors Collections
    def testAuthorsCollection(self):
        authors_collection = self.getAuthorsCollection()
        for document in authors_collection.find():
            print(document)

    # Get Publications Collection
    def getPublicationsCollection(self):
        collection = "Publications"
        this_collection = self.db.get_collection(collection)
        return this_collection

    # Test Get Publications Collections
    def testPublicationsCollection(self):
        publications_collection = self.getPublicationCollection()
        for document in publications_collection.find():
            print(document)

# [Test Database Class] returns and prints collections for database class
'''
myDB = Database("rcharnley", "ljfsRYJzLQJv0I0C")
myDB.testPapersCollection()
myDB.testAuthorsCollection()
myDB.testPublicationsCollection()
'''

