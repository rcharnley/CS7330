from tkinter import *
from tkinter import ttk
import tkinter as tk
import query1_paper_information as queryByTitle
import query2_author_paper as queryByAuthor

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
        mapOfPaperInfo = queryByTitle.query_paper(title)
        titleResults = Toplevel(window)
        titleResults.title("Paper Results for Search by Title " + title)
        titleResults.geometry("400x400")
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
        listOfPapers = queryByAuthor.query_author(firstname, lastname)
        authorResults = Toplevel(window)
        authorResults.title("Paper Results for Search by Author " + firstname + " " + lastname)
        authorResults.geometry("600x600")
        buildString = Text(authorResults)
        for paper in listOfPapers:
            buildString.insert(END, paper + '\n')
        buildString.pack()
        authorResults.mainloop()
    # The program should get the name of a publication, and a year range, and list of papers that is published within that range.
    if publication != "" and startyear != 0 and endyear != 0: 
        print("Search for papers by publication " + publication + " between the years of " + str(startyear) + " and " + str(endyear))
        publicationResults = Toplevel(window)
        publicationResults.title("Paper Results for Search by Publication " + publication)
        publicationResults.geometry("400x400")
        Label(publicationResults, "Paper Results").pack()
    firstname_var.set("")
    lastname_var.set("")
    title_var.set("")
    publication_var.set("")
    startyear_var.set("")
    endyear_var.set("")

window = Tk()
window.title("Research Papers")
window.geometry('600x600')
window.configure(background = "white")
firstname_var = tk.StringVar()
lastname_var = tk.StringVar()
title_var = tk.StringVar()
publication_var = tk.StringVar()
startyear_var = tk.StringVar()
endyear_var = tk.StringVar()
a = Label(window ,text = "First Name").grid(row = 0,column = 0)
b = Label(window ,text = "Last Name").grid(row = 0,column = 2)
c = Label(window ,text = "Title").grid(row = 1,column = 0)
d = Label(window ,text = "Publication").grid(row = 2,column = 0)
e = Label(window ,text = "Start Year").grid(row = 3,column = 0)
f = Label(window ,text = "End Year").grid(row = 4,column = 0)
a1 = Entry(window, textvariable = firstname_var).grid(row = 0,column = 1)
b1 = Entry(window, textvariable = lastname_var).grid(row = 0,column = 3)
c1 = Entry(window, textvariable = title_var).grid(row = 1,column = 1)
d1 = Entry(window, textvariable = publication_var).grid(row = 2,column = 1)
e1 = Entry(window, textvariable = startyear_var).grid(row = 3,column = 1)
f1 = Entry(window, textvariable = endyear_var).grid(row = 4,column = 1)
btn = ttk.Button(window ,text = "Search", command = search).grid(row=5,column=0)
window.mainloop()