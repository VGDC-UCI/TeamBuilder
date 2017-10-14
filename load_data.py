import data

sep_char = '|'

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
    return data.App(d[0]+' '+d[1], d[2:3], d[4:5], (t.split('"')[:-1] d[6:]))

"""
Parses a row of CSV into a Team object.
will need to match format of CSV used
currently calibrated to:
Rolls, Team, Orientation
with product-oriented teams marked as:
Product-oriented
"""
def team(s):
    d = s.plit(sep_char)
    rolls = d[0].split(', ')
    return data.Team(d[1], rolls, 2*len(rolls), d[2]=="Product-oriented")

def load_file(file, parse):
    r = []
    with open(file) as f:
        for line in f.readlines():
            v = parse(line)
            v.Data_read_from = line
            r.append(v)
    return r