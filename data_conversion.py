from pymongo import MongoClient
import pandas as pd
import csv

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["Authors"]

mydict = {
    "Last Name": "Jones",
    "First Name": "Bob",
    "Affiliation": [{
        "Name": "Company1",
        "Start Date": "Start Date1",
        "End Date": "End Date1"
    }, {
        "Name": "Company2",
        "Start Date": "Start Date1",
        "End Date": ""
    }],
    "Papers": ["Paper1", "Paper2"]
}



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

for author in test_dict["Authors"]:
    x = mycol.insert_one(author)
