from database import Database

class Insert:
    def __init__(self, database):
        self.db = database
        self.affiliation = []
        self.papers = []
        self.authors = []
        self.publications = []
    
    def _authorAffiliation(self, companyName, startDate, endDate=""):
        # clear list
        self.affiliation.clear()

        # append values
        self.affiliation.append([companyName, startDate, endDate])

        # sort list by start date
        self.affiliation.sort(key=lambda affiliation:affiliation[1])

        return self.affiliation

    def _authorPapers(self, paper):
        # clear list
        self.papers.clear()

        # append values
        self.papers.append(paper)

        # sort list by paper title
        self.papers.sort()

        return self.papers

    def insertAuthor(self, firstName, lastName):
        authors_dict = {}
        authors_dict["first_name"] = firstName
        authors_dict["last_name"] = lastName
        authors_dict["affiliation"] = []

        for employer in self.affiliation:
            employer_dict = {}
            employer_dict["name"] = employer[0]
            employer_dict["start_date"] = employer[1]
            employer_dict["end_date"] = employer[2]
            authors_dict["affiliation"].append(employer_dict)

        authors_dict["papers"] = self.papers

        # get authors collection
        author_collection = self.db.getAuthorsCollection()
        
        # insert created authors dict into authors collection
        for x in author_collection.find({}):
            x.pop("_id")
            if x == authors_dict:
                return "Error, an authors document the same as this already exists in this Database.  Please insert another unique document"

        x = author_collection.insert_one(authors_dict)
        return x.acknowledged

    def _paperAuthors(self, firstName, lastName):
        # clear list 
        self.authors.clear()

        # append values
        name = firstName + " " + lastName
        self.authors.append(name)

        # sort list so authors are in order
        self.authors.sort()

        return self.authors

    def _paperPublications(self, publication):
        # clear list
        self.publications.clear()

        # append values
        self.publications.append(publication)

        # sort list of publications
        self.publications.sort()
        return self.publications

    def insertPaper(self, title, url, pageNum):
        papers_dict = {}
        papers_dict["title"] = title
        papers_dict["authors"] = self.authors
        papers_dict["url"] = url
        papers_dict["page_number"] = pageNum
        papers_dict["publication"] = self.publications

        # get papers collection
        paper_collection = self.db.getPapersCollection()

        # insert created papers dict into papers collection
        for x in paper_collection.find({}):
            x.pop("_id")
            if x == papers_dict:
                return "Error, a papers document the same as this already exists in this Database.  Please insert another unique document"

        x = paper_collection.insert_one(papers_dict)
        return x.acknowledged

    def insertPublication(self, name, iteration, location, year):
        publication_dict = {}
        publication_dict["name"] = name
        publication_dict["year"] = year
        publication_dict["conference_details"] = {"iteration": iteration, "location": location}
        publication_dict["Papers"] = self.papers

        # get publications collection
        publications_collection = self.db.getPublicationsCollection()

        # insert created publications dict into publications collection
        for x in publications_collection.find({}):
            x.pop("_id")
            if x == publication_dict:
                return "Error, a Publications document the same as this already exists in this Database.  Please insert another unique document"

        x = publications_collection.insert_one(publication_dict)
        return x.acknowledged


if __name__=="__main__":
    from pymongo import MongoClient

    # initialize insert
    myInsert = Insert(Database("mwisniewski", "nzMIpgjB96hUS2vO"))

    # insert author
    # myInsert._authorAffiliation("Raytheon", "1999")
    # myInsert._authorPapers("Paper2")
    # print(myInsert.insertAuthor("UNIQUE2", "Wisniewski"))

    # insert paper
    # myInsert._paperAuthors("Mike", "Wisniewski")
    # myInsert._paperAuthors("Rosemary", "Charnley")
    # myInsert._paperAuthors("George", "Sammit")
    # myInsert._paperPublications("CS7330")
    # myInsert._paperPublications("SMU")
    # myInsert.insertPaper("CS7330 Project Paper", "Google", 4)

    # insert publication
    # myInsert._authorPapers("Paper 1, Paper 2")
    # print(myInsert.insertPublication("Some Journal", 20, "Dallas, TX", 2019))