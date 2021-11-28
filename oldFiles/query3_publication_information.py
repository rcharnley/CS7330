import re

import certifi
from pymongo import MongoClient

# parameter setting
connection_string = "mongodb+srv://rcharnley:ljfsRYJzLQJv0I0C@cluster0.817yp.mongodb.net/admin?ssl=true&ssl_cert_reqs=CERT_NONE"
database_name = "ProjectCS7330"
papers_collection_name = "Papers"
publication_collection_name = "Publications"


# query a paper title
def query_publication(db, name=None, start_year=None, end_year=None):

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
        filter.append({"name": name_regex})

    if len(filter):
        filter = {"$and": filter}
    else:
        filter = {}

    results = db.Publications.find(filter)
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


if __name__ == "__main__":
    client = MongoClient(connection_string, ssl_ca_certs=certifi.where())
    db = client.ProjectCS7330

    result = query_publication(db)
    print(result[0])
    print('-------------')
    result = query_publication(db, 'ACM SIGMOD International Conference on Management of Data')
    print(result[0])
    print('-------------')
    result = query_publication(db, '.*SIGMOD.*')
    print(result[0])
    print('-------------')
    result = query_publication(db, 'ACM SIGMOD International Conference on Management of Data', start_year=2017)
    print(result[0])
    print('-------------')
    result = query_publication(db, 'ACM SIGMOD International Conference on Management of Data', end_year=2017)
    print(result[0])
    print('-------------')
    result = query_publication(db, 'ACM SIGMOD International Conference on Management of Data', 2016, 2017)
    print(result[0])
    print('-------------')
    result = query_publication(db, start_year=2016, end_year=2017)
    print(result[0])
    print('-------------')
    result = query_publication(db, start_year=2000, end_year=2001)
    print(len(result))

