import re
from database import Database

class Query: 
    def __init__(self, database):
        self.db = database

    def print_result(self, collection):
        for document in collection:
            print(document)
        print('------------------')

    # [QUERY 1] The program should get the name of a paper and return all relevant info for each paper.
    def query_paper(self,title=None, authors=None, publication=None):
        papers_collection = self.db.getPapersCollection()
        # query the title of the paper and return the base information
        title_filter = {"title": title}
        paper_cursor = papers_collection.find(title_filter)

        # Store Paper Info as Dictionary
        paperInfo = {}

        for document in paper_cursor:
            paperInfo.update({"Title": document['title']})
            paperInfo.update({"Author": [*document['authors']]})
            if document.__contains__('url'):
                paperInfo.update({"URL": document['url']})
            if document.__contains__('page_number'):
                paperInfo.update({"Page Number": document['page_number']})
            paperInfo.update({"Publication": [*document['publication']]})

        return paperInfo

    # [QUERY 2] The program should get the name of an author (just the name), and list of the papers for that author.
    def query_author(self, first_name=None, last_name=None):
        authors_collection = self.db.getAuthorsCollection()
        # query the title of the paper and return the base information
        filter = []
        if first_name is not None and len(first_name):
            filter.append({"first_name": re.compile(first_name, re.IGNORECASE)})
        if last_name is not None and len(last_name):
            filter.append({"last_name": re.compile(last_name, re.IGNORECASE)})

        if len(filter):
            author_filter = {"$and": filter}
        else:
            author_filter = {}
        author_cursor = authors_collection.find(author_filter)

        # Store papers as list
        listOfPapersByAuthor = []
        for document in author_cursor:
            for paper in document['papers']:
                listOfPapersByAuthor.append(paper)
        
        return listOfPapersByAuthor

    # [QUERY 3] The program should get the name of a publication, and a year range, and list of papers that is published within that range.
    # query a paper title
    def query_publication(self, name=None, start_year=None, end_year=None):
        publications_collection = self.db.getPublicationsCollection()

        filter = []
        if start_year is not None and end_year is not None and start_year > end_year:
                temp = start_year
                start_year = end_year
                end_year = temp

        if start_year is not None:
            filter.append({"year": {"$gte": start_year}})
        if end_year is not None:
            filter.append({"year": {"$lte": end_year}})
        if name is not None:
            name_regex = re.compile(name, re.IGNORECASE)
            filter.append({"name": name})

        if len(filter):
            filter = {"$and": filter}
        else:
            filter = {}

        results = publications_collection.find(filter)
        publications = []
        for publication in results:
            pub_key = "conference_details" if "conference_details" in publication.keys() else "journal_details"
            pub = {"name": publication['name'],
                "year": publication['year'],
                "iteration": publication['iteration'],
                pub_key : publication[pub_key],
                "papers": publication['papers']}
            publications.append(pub)
        return publications


# [Test Query Class] returns and prints query results for Query class

# myQuery = Query(Database("rcharnley", "ljfsRYJzLQJv0I0C"))
# #print(myQuery.query_paper("The Meaning of Null in Databases and Programming Languages"))
# #myQuery.print_result(myQuery.query_author("Peter", "Lindner"))
# myQuery.print_result(myQuery.query_publication("ACM SIGMOD International Conference on Management of Data", 2000, 2020))
