import random
import os
import csv
import arxiv

############################################################################################
# Goes out to arXiv.org and finds papers based on the search criteria over the past 5
# years.  All papers will be randomly associated with either a conference or a journal

SEARCH = "relational database"
MIN_YEAR = 2016
MAX_YEAR = 2021
YEAR = range(MIN_YEAR, MAX_YEAR+1)
TOTAL_PAPERS = 500
TOTAL_PAPERS_PER_YEAR = int(round(TOTAL_PAPERS / len(YEAR)))
OPTIONAL_INFO = ['NONE', 'URL', 'PAGES', 'BOTH']
AFFILIATIONS = [None, "University of Michigan", "Southern Methodist University", "Auburn University", "Boston College", "Stanford", "Yale", "New York University", "University of Alaska", "Huntingdon College", "Troy University", None, "Southwest Airlines", "IBM", "American Airlines", "Sofft Layer", "USAA", "State Farm"]


class Conference:
    def __init__(self, name, number, year, location):
        self.name = name
        self.number = number
        self.year = year
        self.location = location


class Journal:
    def __init__(self, name, year, month, volume=None):
        self.name = name
        self.year = year
        self.month = month
        self.volume = volume


CONFERENCES = {2021: [Conference('ACM SIGMOD International Conference on Management of Data', '6th', '2021', "Dallas, TX"),
                      Conference('International Conference on Very Large Databases', '8th', '2021', "El Paso, TX"),
                      Conference('ACM SIGIR Conference on Research and Development in Information Retrieval', '15th', '2021', 'Berlin, Germany')],
               2020: [Conference('ACM SIGMOD International Conference on Management of Data', '5th', '2020', "Dallas, TX"),
                      Conference('International Conference on Very Large Databases', '7th', '2020', "Austin, TX"),
                      Conference('ACM SIGIR Conference on Research and Development in Information Retrieval', '14th', '2020', 'Berlin, Germany')],
               2019: [Conference('ACM SIGMOD International Conference on Management of Data', '4th', '2019', "Dallas, TX"),
                      Conference('International Conference on Very Large Databases', '6th', '2019', "Arlington, TX"),
                      Conference('ACM SIGIR Conference on Research and Development in Information Retrieval', '13th', '2019', 'Hamburg, Germany')],
               2018: [Conference('ACM SIGMOD International Conference on Management of Data', '3rd', '2018', "Dallas, TX"),
                      Conference('International Conference on Very Large Databases', '5th', '2018', "Houston, TX"),
                      Conference('ACM SIGIR Conference on Research and Development in Information Retrieval', '12th', '2018', 'Hamburg, Germany')],
               2017: [Conference('ACM SIGMOD International Conference on Management of Data', '2nd', '2017', "Dallas, TX"),
                      Conference('International Conference on Very Large Databases', '4th', '2017', "Plano, TX"),
                      Conference('ACM SIGIR Conference on Research and Development in Information Retrieval', '11th', '2017', 'Bonn, Germany')],
               2016: [Conference('ACM SIGMOD International Conference on Management of Data', '1st', '2016', "Dallas, TX"),
                      Conference('International Conference on Very Large Databases', '3rd', '2016', "Irving, TX"),
                      Conference('ACM SIGIR Conference on Research and Development in Information Retrieval', '10th', '2016', 'Berlin, Germany')]
              }

JOURNALS = {2021: [Journal('Journal of Big Data', '2021', '01', None),
                   Journal('IEEE Transactions on Big Data', '2021', '03', '28'),
                   Journal('IEEE Transactions on Knowledge and Data Engineering', '2021', '03', '20')],
            2020: [Journal('Journal of Big Data', '2020', '01', None),
                   Journal('IEEE Transactions on Big Data', '2020', '03', '27'),
                   Journal('IEEE Transactions on Knowledge and Data Engineering', '2020', '03', '19')],
            2019: [Journal('Journal of Big Data', '2019', '01', None),
                   Journal('IEEE Transactions on Big Data', '2019', '03', '26'),
                   Journal('IEEE Transactions on Knowledge and Data Engineering', '2019', '03', '18')],
            2018: [Journal('Journal of Big Data', '2018', '01', None),
                   Journal('IEEE Transactions on Big Data', '2018', '03', '25'),
                   Journal('IEEE Transactions on Knowledge and Data Engineering', '2018', '03', '17')],
            2017: [Journal('Journal of Big Data', '2017', '01', None),
                   Journal('IEEE Transactions on Big Data', '2017', '03', '24'),
                   Journal('IEEE Transactions on Knowledge and Data Engineering', '2017', '03', '16')],
            2016: [Journal('Journal of Big Data', '2016', '01', None),
                   Journal('IEEE Transactions on Big Data', '2016', '03', '23'),
                   Journal('IEEE Transactions on Knowledge and Data Engineering', '2016', '03', '15')]
            }


class Author:
    def __init__(self, first, last, affiliation):
        self.first = first
        self.last = last
        self.affiliation = affiliation

    def __str__(self):
        return self.first + ' ' + self.last + ' - ' + self.affiliation


class Paper:
    def __init__(self, title, authors, publication, url=None, pages=None):
        self.title = title
        self.authors = {}
        for index, author in enumerate(authors):
            self.authors[index] = author
        self.publication = publication
        self.url = url
        self.pages = pages


def is_done(paper_count_by_year):
    for count in paper_count_by_year.values():
        if count < TOTAL_PAPERS_PER_YEAR:
            return False
    return True


def is_needed(paper_count_by_year, year):
    if paper_count_by_year[year] < TOTAL_PAPERS_PER_YEAR:
        return True
    return False


def increment(paper_count_by_year, year):
    paper_count_by_year[year] += 1


def initialize_paper_count_by_year():
    paper_count_by_year = {}
    for year in YEAR:
        paper_count_by_year[year] = 0
    return paper_count_by_year


def decode(result):
    try:
        title = bytes(result.title, "latin-1").decode("utf-8")
        result.title = title

        for author in result.authors:
            name = bytes(author.name, "latin-1").decode("utf-8")
            author.name = name
    except UnicodeDecodeError:
        return False
    except UnicodeEncodeError:
        return False

    return True

def get_authors(result, affiliations, duplicate_authors):
    authors = []
    for author in result.authors:
        first, last = author.name.split(maxsplit=1)
        if author.name in affiliations.keys():
            if not author.name in duplicate_authors.keys():
                duplicate_authors[author.name] = 1
            duplicate_authors[author.name] += 1
        else:
            affiliations[author.name] = random.choice(AFFILIATIONS)
        authors.append(Author(first, last, affiliations[author.name]))
    return authors

def get_paper(result, year, conference_papers, conferences, journal_papers, journals):
    # Randomly select a journal or conference
    paper = None
    if random.randint(0, 1) == 0:
        conference = random.choice(CONFERENCES[year])
        paper = Paper(result.title, authors, conference)
        conference_papers.append(paper)
        if conference.name not in conferences.keys():
            conferences[conference.name] = {}
        if year not in conferences[conference.name] .keys():
            conferences[conference.name][year] = {}
        if conference.number not in conferences[conference.name][year].keys():
            conferences[conference.name][year][conference.number] = 0
        conferences[conference.name][year][conference.number] += 1
    else:
        journal = random.choice(JOURNALS[year])
        paper = Paper(result.title, authors, journal)
        journal_papers.append(paper)
        if journal.name not in journals.keys():
            journals[journal.name] = {}
        if year not in journals[journal.name] .keys():
            journals[journal.name][year] = {}
        if journal.month not in journals[journal.name][year].keys():
            journals[journal.name][year][journal.month] = 0
        journals[journal.name][year][journal.month] += 1

    return paper


def add_optionals(result, paper):
    # Randomly select the optional features
    optional = random.choice(OPTIONAL_INFO)
    if (optional == 'URL') or (optional == 'BOTH'):
        paper.url = result.pdf_url
    if (optional == 'PAGES') or (optional == 'BOTH'):
        pageA = random.randint(1, 250)
        pageB = random.randint(pageA + 1, pageA + 15)
        paper.pages = "{}-{}".format(pageA, pageB)


def write_journal_papers(journal_papers):
    with open("journal_papers.csv", 'w', newline='') as journals:
        writer = csv.writer(journals)
        for paper in journal_papers:
            author_info = []
            for author_index in sorted(paper.authors.keys()):
                author_info.append(paper.authors[author_index].first)
                author_info.append(paper.authors[author_index].last)
                author_info.append(paper.authors[author_index].affiliation)
            paper_info = [paper.title,
                          paper.publication.name,
                          paper.publication.year,
                          paper.publication.month,
                          paper.publication.volume]
            paper_info.extend(author_info)
            writer.writerow(paper_info)


def write_journals(journals):
    with open("journals.csv", 'w', newline='') as journals_file:
        writer = csv.writer(journals_file)
        for name in journals.keys():
            for year in journals[name].keys():
                for iteration in journals[name][year].keys():
                    writer.writerow([name, year, iteration, journals[name][year][iteration]])


def write_conference_papers(conference_papers):
    with open("conferences_papers.csv", 'w', newline='') as conferences:
        writer = csv.writer(conferences)
        for paper in conference_papers:
            author_info = []
            for author_index in sorted(paper.authors.keys()):
                author_info.append(paper.authors[author_index].first)
                author_info.append(paper.authors[author_index].last)
                author_info.append(paper.authors[author_index].affiliation)
            paper_info = [paper.title,
                          paper.publication.name,
                          paper.publication.number,
                          paper.publication.year,
                          paper.publication.location]
            paper_info.extend(author_info)
            writer.writerow(paper_info)


def write_conferences(conferences):
    with open("conferences.csv", 'w', newline='') as conferences_file:
        writer = csv.writer(conferences_file)
        for name in conferences.keys():
            for year in conferences[name].keys():
                for iteration in conferences[name][year].keys():
                    writer.writerow([name, year, iteration, conferences[name][year][iteration]])


def write_authors(duplicate_authors):
    with open("authors.csv", 'w', newline='') as authors:
        writer = csv.writer(authors)
        for author in duplicate_authors.items():
            writer.writerow(author)


if __name__ == "__main__":

    search = arxiv.Search(
        query=SEARCH,
        max_results=float('inf'),
        sort_by=arxiv.SortCriterion.Relevance
    )

    paper_count_by_year = initialize_paper_count_by_year()
    affiliations = {}
    journal_papers = []
    conference_papers = []
    duplicate_authors = {}
    conferences = {}
    journals = {}

    for result in search.results():
        if is_done(paper_count_by_year):
            break
        if decode(result):
            try:
                year = result.published.year
                if (MIN_YEAR <= year <= MAX_YEAR) and is_needed(paper_count_by_year, year):
                    authors = get_authors(result, affiliations, duplicate_authors)
                    paper = get_paper(result, year, conference_papers, conferences, journal_papers, journals)
                    add_optionals(result, paper)
                    increment(paper_count_by_year, year)
            except:
                pass

    write_journal_papers(journal_papers)
    write_journals(journals)
    write_conference_papers(conference_papers)
    write_conferences(conferences)
    write_authors(duplicate_authors)