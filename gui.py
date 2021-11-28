from tkinter import *
from tkinter import ttk
import tkinter as tk
from database import Database
from query import Query
from bonus import Bonus
import author_insert as author_insert

def search():
    firstname = (firstname_var.get()).strip()
    lastname = (lastname_var.get()).strip()
    title = (title_var.get()).strip()
    publication = (publication_var.get()).strip()
    startyear = int((startyear_var.get()).strip() or 0)
    endyear = int((endyear_var.get()).strip() or 0)
    # [QUERY 1] The program should get the name of a paper and return all relevant info for each paper
    if title != "":
        print("Search for papers by title " + title)
        mapOfPaperInfo = myQuery.query_paper(title)
        titleResults = Toplevel(window)
        titleResults.title("Paper Results for Search by Title " + title)
        titleResults.geometry("600x600")
        buildString = Text(titleResults)
        for info in mapOfPaperInfo.values():
            if isinstance(info, list): 
                info = ", ".join(info)
            buildString.insert(END, info + '\n')
        buildString.pack()
        titleResults.mainloop()
    # [QUERY 2] The program should get the name of an author (just the name), and list of the papers for that author.
    if firstname != "" and lastname != "": 
        print("Search for papers by author " + firstname + " " + lastname)
        listOfPapers = myQuery.query_author(firstname, lastname)
        authorResults = Toplevel(window)
        authorResults.title("Paper Results for Search by Author " + firstname + " " + lastname)
        authorResults.geometry("600x600")
        buildString = Text(authorResults)
        for paper in listOfPapers:
            buildString.insert(END, paper + '\n')
        buildString.pack()
        authorResults.mainloop()
    # [QUERY 3] The program should get the name of a publication, and a year range, and list of papers that is published within that range.
    if publication != "" and startyear != 0 and endyear != 0: 
        listOfPapers = myQuery.query_publication(publication, str(startyear), str(endyear))
        print("Search for papers by publication " + publication + " between the years of " + str(startyear) + " and " + str(endyear))
        publicationResults = Toplevel(window)
        publicationResults.title("Paper Results for Search by Publication " + publication)
        publicationResults.geometry("600x600")
        buildString = Text(publicationResults)
        for paper in listOfPapers:
            buildString.insert(END, paper + '\n')
        buildString.pack()
        publicationResults.mainloop()
    firstname_var.set("")
    lastname_var.set("")
    title_var.set("")
    publication_var.set("")
    startyear_var.set("")
    endyear_var.set("")

def removeSpaces(listOfItems, convertToInt): 
    for i in range(len(listOfItems)):
        listOfItems[i] = listOfItems[i].strip()
        if convertToInt: 
            listOfItems[i] = int(listOfItems[i])
    return listOfItems


def insert(): 
    firstname = (fname_var.get()).strip()
    lastname = (lname_var.get()).strip()
    employer = removeSpaces(employer_var.get().split(','), False)
    startyear = removeSpaces(syear_var.get().split(','), True)
    endyear = removeSpaces(eyear_var.get().split(','), True)
    papers = removeSpaces(papers_var.get().split(','), False)
    thisInsert = author_insert.insertAuthor()
    for i in range(len(employer)):
        thisInsert._authorAffiliation(employer[i], startyear[i], endyear[i])
    for paper in papers: 
        thisInsert._authorPapers(paper)
    authoObject = thisInsert.insertAuthor(lastname, firstname, thisInsert.affiliation, thisInsert.papers)
    fname_var.set("")
    lname_var.set("")
    employer_var.set("")
    syear_var.set("")
    eyear_var.set("")
    papers_var.set("")
    

# define classes
myDB = Database("rcharnley", "ljfsRYJzLQJv0I0C")
myQuery = Query(myDB)
myBonus = Bonus(myDB, myQuery)
#Set tkinter Window
window = Tk()
window.title("Research Papers")
window.geometry('700x600')
window.configure(background = "white")
# query variables
firstname_var = tk.StringVar()
lastname_var = tk.StringVar()
title_var = tk.StringVar()
publication_var = tk.StringVar()
startyear_var = tk.StringVar()
endyear_var = tk.StringVar()
# insert variables
fname_var = tk.StringVar()
lname_var = tk.StringVar()
employer_var = tk.StringVar()
syear_var = tk.StringVar()
eyear_var = tk.StringVar()
papers_var = tk.StringVar()
window.columnconfigure(0, weight=1)
Label(window, text = 'SEARCH DATABASE').grid(row = 0, sticky = "ew")
a = Label(window ,text = "First Name").grid(row = 1,column = 0)
b = Label(window ,text = "Last Name").grid(row = 1,column = 2)
c = Label(window ,text = "Title").grid(row = 2,column = 0)
d = Label(window ,text = "Publication").grid(row = 3,column = 0)
e = Label(window ,text = "Start Year").grid(row = 4,column = 0)
f = Label(window ,text = "End Year").grid(row = 4,column = 2)
a1 = Entry(window, textvariable = firstname_var).grid(row = 1,column = 1)
b1 = Entry(window, textvariable = lastname_var).grid(row = 1,column = 3)
c1 = Entry(window, textvariable = title_var).grid(row = 2,column = 1)
d1 = Entry(window, textvariable = publication_var).grid(row = 3,column = 1)
e1 = Entry(window, textvariable = startyear_var).grid(row = 4,column = 1)
f1 = Entry(window, textvariable = endyear_var).grid(row = 4,column = 3)
btn = ttk.Button(window ,text = "Search", command = search).grid(row=6,column=0)
window.columnconfigure(0, weight=1)
Label(window, text = 'INSERT DATABASE').grid(row = 7, sticky = "ew")
g = Label(window ,text = "First Name").grid(row = 8,column = 0)
h = Label(window ,text = "Last Name").grid(row = 8,column = 2)
i = Label(window ,text = "Employer").grid(row = 9,column = 0)
j = Label(window ,text = "Start Year").grid(row = 10,column = 0)
k = Label(window ,text = "End Year").grid(row = 10,column = 2)
l = Label(window ,text = "Papers").grid(row = 11,column = 0)
g1 = Entry(window, textvariable = fname_var).grid(row = 8,column = 1)
h1 = Entry(window, textvariable = lname_var).grid(row = 8,column = 3)
i1 = Entry(window, textvariable = employer_var).grid(row = 9,column = 1)
j1 = Entry(window, textvariable = syear_var).grid(row = 10,column = 1)
k1 = Entry(window, textvariable = eyear_var).grid(row = 10,column = 3)
k1 = Entry(window, textvariable = papers_var).grid(row = 11,column = 1)
btn = ttk.Button(window ,text = "Insert", command = insert).grid(row=12, column=0)
window.mainloop()