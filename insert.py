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
        if author_collection.find(authors_dict):
            return "Error, an authors document the same as this already exists in this Database.  Please insert another unique document"
        else:
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

    def insertPaper(self, title):
        papers_dict = {}
        papers_dict["title"] = title
        papers_dict["authors"] = self.authors
        papers_dict["url"] = "www.google.com"
        papers_dict["page_number"] = "page#"
        papers_dict["publication"] = self.publications

        # get papers collection
        paper_collection = self.db.getPapersCollection()

        # insert created papers dict into papers collection
        if paper_collection.find(papers_dict):
            return "Error, a papers document the same as this already exists in this Database.  Please insert another unique document"
        else:
            x = paper_collection.insert_one(papers_dict)
            return x.acknowledged

    def insertPublication(self, name, iteration, location):
        publication_dict = {}
        publication_dict["name"] = name
        publication_dict["year"] = 2020
        publication_dict["iteration"] = iteration
        publication_dict["conference_details"] = {"location": location}
        publication_dict["Papers"] = self.papers

        # get publications collection
        publications_collection = self.db.getPublicationsCollection()

        # insert created publications dict into publications collection
        if publications_collection.find(publication_dict):
            return "Error, a Publications document the same as this already exists in this Database.  Please insert another unique document"
        else:
            x = publications_collection.insert_one(publication_dict)
            return x.acknowledged


if __name__=="__main__":
    from pymongo import MongoClient

    # initialize insert
    myInsert = Insert(Database("rcharnley", "ljfsRYJzLQJv0I0C"))

    # insert author
    myInsert._authorAffiliation("SMU", "2021-01-01")
    myInsert._authorPapers("Paper1")
    myInsert.insertAuthor("Mike", "Wisniewski")

    # insert paper
    myInsert._paperAuthors("Mike", "Wisniewski")
    myInsert._paperAuthors("Rosemary", "Charnley")
    myInsert._paperAuthors("George", "Sammit")
    myInsert._paperPublications("CS7330")
    myInsert._paperPublications("SMU")
    myInsert.insertPaper("CS7330 Project Paper")

    # insert publication
    myInsert._authorPapers("CS7330 Project Write Up")
    myInsert.insertPublication("CS DBMS Conference", 1, "Dallas, TX")
