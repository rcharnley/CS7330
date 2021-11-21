from pymongo import MongoClient
import pandas as pd
import csv

# parameter setting
connection_string = "mongodb+srv://mwisniewski:nzMIpgjB96hUS2vO@cluster0.817yp.mongodb.net/Cluster0?retryWrites=true&w=majority"
database_name = "ProjectCS7330"
authors_collection_name = "Authors"

# connection protocol
myclient = MongoClient(connection_string)
mydb = myclient[database_name]
mycol = mydb[authors_collection_name]


def _convert_to_json(filename):
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
                

test_dict = _convert_to_json("16NovExtraction/conferences.csv")

# upload
for author in test_dict["Authors"]:
    x = mycol.insert_one(author)
