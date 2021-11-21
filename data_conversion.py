from pymongo import MongoClient
import pandas as pd
import csv


def _author_load(filename):
    authors_dict = {"Authors":[]}
    
    with open(filename, "r") as temp_f:
        authors = []

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

                # check to see if author current exists within database
                author_exists = False
                for key, value in authors_dict.items():
                    for sub_dict in value:
                        if sub_dict["First Name"] == line[firstName_idx] and sub_dict["Last Name"] == line[lastName_idx]:
                            sub_dict["Papers"].append(paperTitle)
                            author_exists = True

                # create a new entry if author does not exist
                if author_exists == False:
                    authors_dict["Authors"].append(
                        {
                            "First Name": line[firstName_idx], 
                            "Last Name": line[lastName_idx],
                            "Affiliation": [
                                {
                                    "Name": line[affiliation_idx],
                                    "Start Date": "Date1",
                                    "End Date": ""
                                }
                            ],
                            "Papers": [paperTitle]
                            }
                    )

                firstName_idx += 3
                lastName_idx += 3
                affiliation_idx += 3

    temp_f.close()
    return authors_dict

def _paper_load(filename):
    papers_dict = {"Papers":[]}
    
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
                
if __name__=="__main__":

    # parameter setting
    connection_string = "mongodb+srv://mwisniewski:nzMIpgjB96hUS2vO@cluster0.817yp.mongodb.net/Cluster0?retryWrites=true&w=majority"
    database_name = "ProjectCS7330"
    authors_collection_name = "Papers"

    # connection protocol
    myclient = MongoClient(connection_string)
    mydb = myclient[database_name]
    mycol = mydb[authors_collection_name]

    # # upload authors
    # test_dict = _author_load("16NovExtraction/conferences.csv")
    # for author in test_dict["Authors"]:
    #     x = mycol.insert_one(author)

    # upload papers
    test_dict = _paper_load("16NovExtraction/conferences.csv")
    for paper in test_dict["Papers"]:
        x = mycol.insert_one(paper)
