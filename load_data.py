import data

sep_char = '\t'

"""
Parses a row of CSV into an Applicant object.
will need to match format of CSV used
currently calibrated to:
First, Last, Primary Roll, Secondary Roll, Experiance, Experiance, Choices...
with each choice in format:
"Name," other data
"""
def app(s):
    d = s.split(sep_char)
    return data.App(d[0]+' '+d[1], d[2:3] + d[4:5], d[3:4] + d[5:6], [t.split('"')[1][:-1] for t in d[6:]])

"""
Parses a row of CSV into a Team object.
will need to match format of CSV used
currently calibrated to:
Rolls, Team, Orientation
with product-oriented teams marked as:
Product-oriented
"""
def team(s):
    d = s.split(sep_char)
    rolls = d[0].split(', ')
    return data.Team(d[1], rolls, sum(data.needed[roll] for roll in rolls), d[2]=="Product-oriented")

"""
Loads a file into a list of objects
Takes the path of the file and a parser function
that parser should take a life of the file as a string and return an object of the designered type
"""
def load_file(file, parse):
    r = []
    with open(file) as f:
        for line in f.readlines():
            v = parse(line.rstrip())
            v.Data_read_from = line
            r.append(v)
    return r