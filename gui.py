from tkinter import *
from tkinter import ttk
import tkinter as tk
from database import Database
from query import Query
from bonus import Bonus
from insert import Insert
import tkinter.font as font
import itertools as tool

# Setup Tkinter Window
window = Tk()
window.title("Research Papers")
window.geometry("600x600")
window.config(bg = "#D6FEFF")

# Function to search based on Entry Inputs
def search():
    firstname = (firstname_var.get()).strip()
    lastname = (lastname_var.get()).strip()
    title = (title_var.get()).strip()
    publication = (publication_var.get()).strip()
    startyear = int((startyear_var.get()).strip() or 0)
    endyear = int((endyear_var.get()).strip() or 0)
    # [QUERY 1] The program should get the name of a paper and return all relevant info for each paper
    if title != "" and (firstname == "" and lastname == "" and publication == "" and startyear == 0 and endyear == 0):
        print("Search for papers by title " + title)
        mapOfPaperInfo = myQuery.query_paper(title)
        titleResults = Toplevel(window)
        titleResults.title("Paper Results for Search by Title " + title)
        titleResults.geometry("600x600")
        buildString = Text(titleResults)
        for info in mapOfPaperInfo.values():
            if isinstance(info, list): 
                info = ", ".join(info)
            buildString.insert(END, info + "\n")
        buildString.pack()
        titleResults.mainloop()
    # [QUERY 2] The program should get the name of an author (just the name), and list of the papers for that author.
    if firstname != "" and lastname != "" and (title == "" and publication == "" and startyear == 0 and endyear == 0): 
        print("Search for papers by author " + firstname + " " + lastname)
        listOfPapers = myQuery.query_author(firstname, lastname)
        authorResults = Toplevel(window)
        authorResults.title("Paper Results for Search by Author " + firstname + " " + lastname)
        authorResults.geometry("600x600")
        buildString = Text(authorResults)
        for paper in listOfPapers:
            buildString.insert(END, paper + "\n")
        buildString.pack()
        authorResults.mainloop()
    # [QUERY 3] The program should get the name of a publication, and a year range, and list of papers that is published within that range.
    if publication != "" and startyear != 0 and endyear != 0 and (firstname == "" and lastname == "" and title == ""): 
        listOfPapers = myQuery.query_publication(publication, startyear, endyear)
        print("Search for papers by publication " + publication + " between the years of " + str(startyear) + " and " + str(endyear))
        publicationResults = Toplevel(window)
        publicationResults.title("Paper Results for Search by Publication " + publication)
        publicationResults.geometry("600x600")
        buildString = Text(publicationResults)
        for paper in listOfPapers:
            buildString.insert(END, str(paper) + "\n")
        buildString.pack()
        publicationResults.mainloop()
    firstname_var.set("")
    lastname_var.set("")
    title_var.set("")
    publication_var.set("")
    startyear_var.set("")
    endyear_var.set("")

def search_matching_name(): 
    firstname = (firstname_var.get()).strip()
    lastname = (lastname_var.get()).strip()
    title = (title_var.get()).strip()
    publication = (publication_var.get()).strip()
    startyear = int((startyear_var.get()).strip() or 0)
    endyear = int((endyear_var.get()).strip() or 0)
    if firstname != "" and lastname != "" and (title == "" and publication == "" and startyear == 0 and endyear == 0): 
        print("Search for papers by author " + firstname + " " + lastname + " who may share a name with another")
        listOfPeople = myBonus.query_same_name_authors(firstname, lastname)
        matchingNameResults = Toplevel(window)
        matchingNameResults.title("Paper Results for Search by Author " + firstname + " " + lastname)
        matchingNameResults.geometry("600x600")
        buildString = Text(matchingNameResults)
        for person in listOfPeople: 
            buildStr = "Name: " + person[0] + " " + person[1] + "\nAffiliation: " + person[2] + "\nConference(s)/Journal(s): "+ str(person[3]) + "\n"
            buildString.insert(END, str(buildStr) + "\n")
        buildString.pack()
        matchingNameResults.mainloop()
    firstname_var.set("")
    lastname_var.set("")

def search_co_authors():
    firstname = (firstname_var.get()).strip()
    lastname = (lastname_var.get()).strip()
    title = (title_var.get()).strip()
    publication = (publication_var.get()).strip()
    startyear = int((startyear_var.get()).strip() or 0)
    endyear = int((endyear_var.get()).strip() or 0)
    if firstname != "" and lastname != "" and (title == "" and publication == "" and startyear == 0 and endyear == 0): 
        print("Search for Co-Authors for " + firstname + " " + lastname + ", level 0-3")
        listOfPapers = myBonus.query_co_author(firstname, lastname)
        levelsString = myBonus.buildLevelListString()
        coAuthorResults = Toplevel(window)
        coAuthorResults.title("Co-Author Results for Search by Author " + firstname + " " + lastname)
        coAuthorResults.geometry("600x600")
        buildString = Text(coAuthorResults)
        buildString.insert(END, levelsString)
        buildString.pack()
        coAuthorResults.mainloop()
    firstname_var.set("")
    lastname_var.set("")

def removeSpaces(listOfItems, convertToInt=False): 
    for i in range(len(listOfItems)):
        listOfItems[i] = listOfItems[i].strip()
        if convertToInt: 
            listOfItems[i] = int(listOfItems[i])
    return listOfItems

def generateInsertWindow():
    option = selection_var.get()

    # insert author variables
    fname_var_auth = tk.StringVar()
    lname_var_auth = tk.StringVar()
    employer_var_auth = tk.StringVar()
    syear_var_auth = tk.StringVar()
    eyear_var_auth = tk.StringVar()
    papers_var_auth = tk.StringVar()

    # insert paper variables 
    fname_var_paper = tk.StringVar()
    lname_var_paper = tk.StringVar()
    publication_var_paper = tk.StringVar()
    title_var_paper = tk.StringVar()
    url_var_paper = tk.StringVar()
    page_num_var_paper = tk.StringVar()

    # insert conference variables 
    papers_var_conf = tk.StringVar()
    name_var_conf = tk.StringVar()
    iteration_var_conf = tk.StringVar()
    location_var_conf = tk.StringVar()
    year_var_conf = tk.IntVar()

    # insert journal variables
    papers_var_jour = tk.StringVar()
    name_var_jour = tk.StringVar()
    iteration_var_jour = tk.StringVar()
    year_var_jour = tk.IntVar()
    vol_var_jour = tk.StringVar()

    if option == 1:
        insertAuthorWindow = Toplevel(window)
        insertAuthorWindow.title("Insert Author")
        insertAuthorWindow.geometry("600x600")
        insertAuthorWindow.config(bg = "#D6FEFF")
        # Title section for insert Authot
        Label(insertAuthorWindow, text = "INSERT AUTHOR", font = SubTitleFont, bg = "#D6FEFF").place(x = 0, y = 0)

        # Enter first name to insert author  
        g = Label(insertAuthorWindow ,text = "First Name", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 50)
        g1 = Entry(insertAuthorWindow, textvariable = fname_var_auth).place(x = 75, y = 50)

    
        # Enter last name to insert author  
        h = Label(insertAuthorWindow ,text = "Last Name", font = LabelFont, bg = "#D6FEFF").place(x = 300, y = 50)
        h1 = Entry(insertAuthorWindow, textvariable = lname_var_auth).place(x = 375, y = 50)

        # Enter papers to insert author  
        i = Label(insertAuthorWindow ,text = "Papers", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 100)
        i1 = Entry(insertAuthorWindow, textvariable = papers_var_auth).place(x = 75, y = 100)
        
        # Enter employer to insert author  
        j = Label(insertAuthorWindow ,text = "Employer", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 150)
        j1 = Entry(insertAuthorWindow, textvariable = employer_var_auth).place(x = 75, y = 150)

        # Enter start year to insert author  
        k = Label(insertAuthorWindow ,text = "Start Date", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 200)
        k1 = Entry(insertAuthorWindow, textvariable = syear_var_auth).place(x = 75, y = 200)

        # Enter end year to insert author  
        l = Label(insertAuthorWindow ,text = "End Date", font = LabelFont, bg = "#D6FEFF").place(x = 300, y = 200)
        l1 = Entry(insertAuthorWindow, textvariable = eyear_var_auth).place(x = 375, y = 200)

        # Button to insert author provided
        btn4 = ttk.Button(insertAuthorWindow ,text = "Insert Author", command = lambda: insertAuthor((fname_var_auth.get()).strip(","), (lname_var_auth.get()).strip(), removeSpaces((papers_var_auth.get()).split(",")), removeSpaces((employer_var_auth.get()).split(",")), removeSpaces((syear_var_auth.get()).split(",")), removeSpaces((eyear_var_auth.get()).split(",")) )).place(x = 0, y = 250)
        
    if option == 2: 
        insertPaperWindow = Toplevel(window)
        insertPaperWindow.title("Insert Paper")
        insertPaperWindow.geometry("600x600")
        insertPaperWindow.config(bg = "#D6FEFF")
        # Title section for insert Author
        Label(insertPaperWindow, text = "INSERT PAPER", font = SubTitleFont, bg = "#D6FEFF").place(x = 0, y = 0)

        # Enter first name to insert author  
        m = Label(insertPaperWindow ,text = "First Name", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 50)
        m1 = Entry(insertPaperWindow, textvariable = fname_var_paper).place(x = 75, y = 50)

        # Enter last name to insert author  
        n = Label(insertPaperWindow ,text = "Last Name", font = LabelFont, bg = "#D6FEFF").place(x = 300, y = 50)
        n1 = Entry(insertPaperWindow, textvariable = lname_var_paper).place(x = 375, y = 50)

        # Enter paper titles name to insert author  
        o = Label(insertPaperWindow ,text = "Paper Title", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 100)
        o1 = Entry(insertPaperWindow, textvariable = title_var_paper).place(x = 75, y = 100)

        # Enter publication to insert author  
        p = Label(insertPaperWindow ,text = "Publication(s)", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 150)
        p1 = Entry(insertPaperWindow, textvariable = publication_var_paper).place(x = 75, y = 150)

        # Enter start year to insert author  
        p = Label(insertPaperWindow ,text = "URL", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 200)
        p1 = Entry(insertPaperWindow, textvariable = url_var_paper).place(x = 75, y = 200)

        # Enter end year to insert author  
        q = Label(insertPaperWindow ,text = "Page Number", font = LabelFont, bg = "#D6FEFF").place(x = 300, y = 200)
        q1 = Entry(insertPaperWindow, textvariable = page_num_var_paper).place(x = 375, y = 200)

        # Button to insert author provided
        btn5 = ttk.Button(insertPaperWindow ,text = "Insert Paper", command = lambda: insertPaper((title_var_paper.get()).strip(), removeSpaces((fname_var_paper.get()).split(",")), removeSpaces((lname_var_paper.get()).split(",")), removeSpaces((publication_var_paper.get()).split(",")), (url_var_paper.get()).strip(), (page_num_var_paper.get()).strip() )).place(x = 0, y = 250)
        
    if option == 3: 
        insertConferenceWindow = Toplevel(window)
        insertConferenceWindow.title("Insert Conference")
        insertConferenceWindow.geometry("600x600")
        insertConferenceWindow.config(bg = "#D6FEFF")
        # Title section for insert Author
        Label(insertConferenceWindow, text = "INSERT CONFERENCE", font = SubTitleFont, bg = "#D6FEFF").place(x = 0, y = 0)

        # Enter conferecnce/journal name to insert publicationr  
        r = Label(insertConferenceWindow ,text = "Conference Name", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 50)
        r1 = Entry(insertConferenceWindow, textvariable = name_var_conf).place(x = 100, y = 50)

        # Enter paper location to insert publication
        s = Label(insertConferenceWindow ,text = "Location", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 100)
        s1 = Entry(insertConferenceWindow, textvariable = location_var_conf).place(x = 75, y = 100)

        # Enter iteration to insert publication  
        t = Label(insertConferenceWindow ,text = "Iterations", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 150)
        t1 = Entry(insertConferenceWindow, textvariable = iteration_var_conf).place(x = 75, y = 150)

        u = Label(insertConferenceWindow ,text = "Year", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 200)
        u1 = Entry(insertConferenceWindow, textvariable = year_var_conf).place(x = 75, y = 200)

        # Enter paper titles to insert publication  
        v = Label(insertConferenceWindow ,text = "Paper Titles:", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 250)
        v1 = Entry(insertConferenceWindow, textvariable = papers_var_conf).place(x = 75, y = 250)

        # Button to insert author provided
        btn5 = ttk.Button(insertConferenceWindow ,text = "Insert Conference", command = lambda: insertConference( removeSpaces((papers_var_conf.get()).split(",")), (name_var_conf.get()).strip(), (iteration_var_conf.get()).strip(), year_var_conf.get(), (location_var_conf.get()).strip() )).place(x = 0, y = 300)
    
    if option == 4: 
        insertJournalWindow = Toplevel(window)
        insertJournalWindow.title("Insert Journal")
        insertJournalWindow.geometry("600x600")
        insertJournalWindow.config(bg = "#D6FEFF")
        # Title section for insert Author
        Label(insertJournalWindow, text = "INSERT JOURNAL", font = SubTitleFont, bg = "#D6FEFF").place(x = 0, y = 0)

        # Enter conferecnce/journal name to insert publicationr  
        w = Label(insertJournalWindow ,text = "Journal Name", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 50)
        w1 = Entry(insertJournalWindow, textvariable = name_var_jour).place(x = 75, y = 50)

        # Enter iteration to insert publication  
        y = Label(insertJournalWindow ,text = "Iterations", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 100)
        y1 = Entry(insertJournalWindow, textvariable = iteration_var_jour).place(x = 75, y = 100)

        # Enter iteration to insert publication  
        z = Label(insertJournalWindow ,text = "Volume", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 150)
        z1 = Entry(insertJournalWindow, textvariable = vol_var_jour).place(x = 75, y = 150)

        aa = Label(insertJournalWindow ,text = "Year", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 200)
        aa1 = Entry(insertJournalWindow, textvariable = year_var_jour).place(x = 75, y = 200)

        # Enter paper titles to insert publication  
        bb = Label(insertJournalWindow ,text = "Paper Titles:", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 250)
        bb1 = Entry(insertJournalWindow, textvariable = papers_var_jour).place(x = 75, y = 250)

        # Button to insert author provided
        btn5 = ttk.Button(insertJournalWindow ,text = "Insert Journal", command = lambda: insertJournal( removeSpaces((papers_var_jour.get()).split(",")), (name_var_jour.get()).strip(), iteration_var_jour.get(), year_var_jour.get(), (vol_var_jour.get()).strip() )).place(x = 0, y = 300)
    
    # Reset
    option = 0
    fname_var_auth.set("")
    lname_var_auth.set("")
    employer_var_auth.set("")
    syear_var_auth.set("")
    eyear_var_auth.set("")
    papers_var_auth.set("")

    fname_var_paper.set("")
    lname_var_paper.set("")
    publication_var_paper.set("")
    title_var_paper.set("")
    url_var_paper.set("")
    page_num_var_paper.set("")

    papers_var_conf.set("")
    name_var_conf.set("")
    iteration_var_conf.set("")
    location_var_conf.set("")
    year_var_conf.set("")

    papers_var_jour.set("")
    name_var_jour.set("")
    iteration_var_jour.set("")
    year_var_jour.set("")
        
def insertAuthor(firstname, lastname, paperList, employerList, startyearList, endyearList = []): 
    thisInsert = Insert(Database("rcharnley", "ljfsRYJzLQJv0I0C"))
    index = 0
    for employer, start, end in tool.zip_longest(employerList, startyearList, endyearList):
        if end: thisInsert._authorAffiliation(employerList[index], startyearList[index], endyearList[index])
        else: thisInsert._authorAffiliation(employerList[index], startyearList[index], endyearList[index])
        index = index + 1
    for paper in paperList: 
        thisInsert._authorPapers(paper)
    insert = thisInsert.insertAuthor(firstname, lastname)
    if (isinstance(insert, str)):
        errorWindow = Toplevel(window)
        errorWindow.title("Error")
        errorWindow.geometry("600x100")
        errorWindow.config(bg = "#D6FEFF")
        buildString = Text(errorWindow)
        buildString.config(bg = "#D6FEFF")
        buildString.insert(END, "Error! This Author already exists.\nClose this window and try again.\n")
        buildString.pack()



def insertPaper(title, firstnameList, lastnameList, publicationList, url, pageNum): 
    thisInsert = Insert(Database("rcharnley", "ljfsRYJzLQJv0I0C"))
    for first, last in zip(firstnameList, lastnameList):
        thisInsert._paperAuthors(first, last)
    for pub in publicationList:
        thisInsert._paperPublications(pub)
    insert = thisInsert.insertPaper(title, url, pageNum)
    if (isinstance(insert, str)):
        errorWindow = Toplevel(window)
        errorWindow.title("Error")
        errorWindow.geometry("600x100")
        errorWindow.config(bg = "#D6FEFF")
        buildString = Text(errorWindow)
        buildString.config(bg = "#D6FEFF")
        buildString.insert(END, "Error! This Paper already exists.\nClose this window and try again.\n")
        buildString.pack()

def insertConference(paperList, name, iteration, year, location):
    thisInsert = Insert(Database("rcharnley", "ljfsRYJzLQJv0I0C"))
    for paper in paperList:
        thisInsert._authorPapers(paper)
    insert = thisInsert.insertConference(name, iteration, year, location)
    if (isinstance(insert, str)):
        errorWindow = Toplevel(window)
        errorWindow.title("Error")
        errorWindow.geometry("600x100")
        errorWindow.config(bg = "#D6FEFF")
        buildString = Text(errorWindow)
        buildString.config(bg = "#D6FEFF")
        buildString.insert(END, "Error! This Conference already exists.\nClose this window and try again.\n")
        buildString.pack()

def insertJournal(paperList, name, iteration, year, volume):
    thisInsert = Insert(Database("rcharnley", "ljfsRYJzLQJv0I0C"))
    for paper in paperList:
        thisInsert._authorPapers(paper)
    insert = thisInsert.insertJournal(name, iteration, year, volume)
    if (isinstance(insert, str)):
        errorWindow = Toplevel(window)
        errorWindow.title("Error")
        errorWindow.geometry("600x100")
        errorWindow.config(bg = "#D6FEFF")
        buildString = Text(errorWindow)
        buildString.config(bg = "#D6FEFF")
        buildString.insert(END, "Error! This Journal already exists.\nClose this window and try again.\n")
        buildString.pack()


# Define classes
myDB = Database("rcharnley", "ljfsRYJzLQJv0I0C")
myQuery = Query(myDB)
myBonus = Bonus(myDB, myQuery)
myInsert = Insert(myDB)           

# Query variables     
firstname_var = tk.StringVar()      
lastname_var = tk.StringVar()
title_var = tk.StringVar()
publication_var = tk.StringVar()
startyear_var = tk.StringVar()
endyear_var = tk.StringVar()

# Insert selection variable 
selection_var = tk.IntVar()

# Font Types
TitleFont = font.Font(family = "Times New Roman", size = "16")
SubTitleFont = font.Font(family = "Times New Roman", size = "14")
LabelFont = font.Font(family = "Times New Roman", size = "12")

# Title for search section
Label(window, text = "SEARCH DATABASE", font = TitleFont, bg = "#D6FEFF").place(x = 0, y = 0)

# Enter first name to query 
a = Label(window ,text = "First Name", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 50)
a1 = Entry(window, textvariable = firstname_var).place(x = 75, y = 50)

# Enter last name to query 
b = Label(window ,text = "Last Name", font = LabelFont, bg = "#D6FEFF").place(x = 300, y = 50)
b1 = Entry(window, textvariable = lastname_var).place(x = 375, y = 50)

# Enter paper titles to query 
c = Label(window ,text = "Title", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 100)
c1 = Entry(window, textvariable = title_var).place(x = 75, y = 100)

# Enter publication ot query 
d = Label(window ,text = "Publication", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 150)
d1 = Entry(window, textvariable = publication_var).place(x = 75, y = 150)

# Enter start year to query 
e = Label(window ,text = "Start Year", font = LabelFont, bg = "#D6FEFF").place(x = 0, y = 200)
e1 = Entry(window, textvariable = startyear_var).place(x = 75, y = 200)


# Enter end year to query  
f = Label(window ,text = "End Year", font = LabelFont, bg = "#D6FEFF").place(x = 300, y = 200)
f1 = Entry(window, textvariable = endyear_var).place(x = 375, y = 200)

# Button to  query information provided
# Checks occur in search
btn1 = ttk.Button(window ,text = "Search", command = search).place(x = 0, y = 250)

# Button to query information provided if name is believed to be duplicate
# Checks occur in search
btn2 = ttk.Button(window ,text = "Search Matching Name", command = search_matching_name).place(x = 100, y = 250)

# Button to query information provided searching for co-authors
# Checks occur in search
btn3 = ttk.Button(window ,text = "Search for Co-Authors", command = search_co_authors).place(x = 300, y = 250)

# Title for insert section
Label(window, text = "INSERT INTO DATABASE", font = TitleFont, bg = "#D6FEFF").place(x = 0, y = 300)
# Title section for insert Authot
Label(window, text = "Select type of insert: ", font = SubTitleFont, bg = "#D6FEFF").place(x = 0, y = 350)

# Radio Button to decide type of insert 
Radiobutton(window,text="Author", variable= selection_var, value=1, bg = "#D6FEFF", font = LabelFont).place(x=100,y=375)
Radiobutton(window,text="Paper", variable= selection_var, value=2, bg = "#D6FEFF", font = LabelFont).place(x=200,y=375)
Radiobutton(window,text="Conference", variable= selection_var, value=3, bg = "#D6FEFF", font = LabelFont).place(x=300,y=375)
Radiobutton(window,text="Journal", variable= selection_var, value=4, bg = "#D6FEFF", font = LabelFont).place(x=400,y=375)

# Button to submit selection
btn4 = ttk.Button(window ,text = "Submit", command = generateInsertWindow).place(x = 0, y = 400)

window.mainloop()
