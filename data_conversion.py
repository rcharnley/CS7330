from datetime import date, datetime, timedelta

import certifi
from pymongo import MongoClient
import os
import csv

# Globals
connection_string = "mongodb+srv://mwisniewski:nzMIpgjB96hUS2vO@cluster0.817yp.mongodb.net/Cluster0?retryWrites=true&w=majority"
database_name = "ProjectCS7330"
extraction = "24NovExtraction"


class PublicationPair:
    def __init__(self, details, papers):
        self.details = details
        self.papers = papers


def get_datetime(month, year):
    return datetime.combine(date(year, month, 1), datetime.min.time())


def handle_affiliation(affiliations, name, month, year):
    for index in range(len(affiliations)):
        if affiliations[index]['name'] == name:
            return
    if name is not None and len(name):
        start_date = get_datetime(year, month)
        end_date = start_date - timedelta(1)
        affiliations[-1]["end_date"] = end_date
        affiliations.append({"name": name,
                             "start_date": start_date})


def _author_load_file(authors_dict, filename, isConference):
    with open(filename, "r") as temp_f:
        authors = []

        for line in csv.reader(temp_f):
            paperTitle = line[0]
            if isConference:
                year = int(line[3])
                month = 1  # Conferences don't have months
            else:
                year = int(line[2])
                month = int(line[3])

            # author info
            firstName_idx = 5
            lastName_idx = 6
            affiliation_idx = 7

            while affiliation_idx <= len(line):

                # check to see if author current exists within database
                author_exists = False
                for key, value in authors_dict.items():
                    for sub_dict in value:
                        if sub_dict["first_name"] == line[firstName_idx] and sub_dict["last_name"] == line[lastName_idx]:
                            sub_dict["papers"].append(paperTitle)
                            handle_affiliation(sub_dict['affiliations'], line[affiliation_idx], month, year)
                            author_exists = True

                # create a new entry if author does not exist
                if author_exists == False:
                    affiliation = []
                    if line[affiliation_idx] is not None and len(line[affiliation_idx]):
                        affiliation.append({"name": line[affiliation_idx],
                                            "start_date": get_datetime(month, year)})
                    authors_dict["Authors"].append(
                        {
                            "first_name": line[firstName_idx],
                            "last_name": line[lastName_idx],
                            "affiliations": affiliation,
                            "papers": [paperTitle]
                        }
                    )

                firstName_idx += 3
                lastName_idx += 3
                affiliation_idx += 3

    temp_f.close()

def _author_load(conferences_papers, journal_papers):
    authors_dict = {"Authors": []}
    _author_load_file(authors_dict, conferences_papers, isConference=True)
    _author_load_file(authors_dict, journal_papers, isConference=False)
    return authors_dict


def _paper_load(filename):
    papers_dict = {"Papers": []}

    with open(filename, "r") as temp_f:
        papers = []

        for line in csv.reader(temp_f):
            paperTitle = line[0]
            conferenceName = line[1]
            iteration = line[2]
            year = line[3]
            location = line[4]

            # author info
            firstName_idx = 5
            lastName_idx = 6
            affiliation_idx = 7

            while affiliation_idx <= len(line):

                # check to see if paper current;y exists within database
                paper_exists = False
                for key, value in papers_dict.items():
                    for sub_dict in value:
                        if sub_dict["Title"] == paperTitle:
                            sub_dict["Authors"].append(f'{line[firstName_idx]} {line[lastName_idx]}')
                            paper_exists = True

                # create a new entry if author does not exist
                if paper_exists == False:
                    papers_dict["Papers"].append(
                        {
                            "Title": paperTitle,
                            "Authors": [f'{line[firstName_idx]} {line[lastName_idx]}'],
                            "URL": "TESTURL.COM",
                            "Page Number": "TEST#",
                            "Publication": [conferenceName]
                        }
                    )

                firstName_idx += 3
                lastName_idx += 3
                affiliation_idx += 3

    temp_f.close()
    return papers_dict


def _load_pubs(filename, isConference):
    pubs = {}
    with open(filename, "r") as temp_f:
        reader = csv.reader(temp_f)
        next(reader, None)  # skip the headers
        for line in reader:
            paper = line[0]
            name = line[1]
            if isConference:
                iteration = line[2]
                year = int(line[3])
                location = line[4]
            else:
                year = int(line[2])
                iteration = line[3]
                volume = None if not line[4] else line[4]
            if name not in pubs.keys():
                pubs[name] = {}
            if year not in pubs[name].keys():
                pubs[name][year] = {}
            if iteration not in pubs[name][year] .keys():
                details = []
                if isConference:
                    details.append(location)
                elif volume is not None:
                    details.append(volume)
                pubs[name][year][iteration] = PublicationPair(details, [])
            pubs[name][year][iteration].papers.append(paper)

    # Create the documents
    docs = []
    for name in pubs.keys():
        for year in pubs[name].keys():
            for iteration in pubs[name][year].keys():
                if isConference:
                    details_key = "conference_details"
                    details = {"location": pubs[name][year][iteration].details[0] }
                else:
                    details_key = "journal_details"
                    details = {}
                    if len(pubs[name][year][iteration].details):
                        details['volume'] = pubs[name][year][iteration].details[0]
                doc = {"name": name,
                       "year": year,
                       "iteration": iteration,
                       details_key: details,
                       "papers": pubs[name][year][iteration].papers}
                docs.append(doc)
    return docs


def _load_authors():
    # parameter setting
    authors_collection_name = "Authors"

    # connection protocol
    myclient = MongoClient(connection_string, ssl_ca_certs=certifi.where())
    mydb = myclient[database_name]
    mycol = mydb[authors_collection_name]

    # # upload authors
    test_dict = _author_load(os.path.join(extraction, "conferences_papers.csv"),
                             os.path.join(extraction, "journal_papers.csv"))
    for author in test_dict["Authors"]:
        x = mycol.insert_one(author)


def _load_papers():
    collection_name = "Papers"

    # connection protocol
    myclient = MongoClient(connection_string)
    mydb = myclient[database_name]
    mycol = mydb[collection_name]

    # upload papers
    test_dict = _paper_load("16NovExtraction/conferences.csv")
    for paper in test_dict["Papers"]:
        x = mycol.insert_one(paper)


def _load_publications():

    client = MongoClient(connection_string, ssl_ca_certs=certifi.where())
    db = client.ProjectCS7330
    confs = _load_pubs(os.path.join(extraction, "conferences_papers.csv"), isConference=True)
    journals = _load_pubs(os.path.join(extraction, "journal_papers.csv"), isConference=False)
    db.Publications.insert_many(confs)
    db.Publications.insert_many(journals)


if __name__ == "__main__":

    _load_authors()
    # _load_papers()
    #_load_publications()
