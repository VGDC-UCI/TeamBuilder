from collections import defaultdict

"""
Estimates of how many of each roll form the perfect team that the system uses:
"""
needed = {"Artist" : 2, "Gameplay Designer" : 2, "Audio Designer" : 1, "Producer" : 1, "Programmer" : 3, "Writer" : 1}

#all priority lists highest -> lowest

"""
A class to represent an applicant
"""
class App():

    """
    name : string name
    rolls: list of strings of roll
    exps: list of experiance with those roles (any consistent data type)
    pref_names: names of the project would like to work on, in order
    """
    def __init__(self, name, rolls, exps, pref_names):
        self.name = name
        self.rolls = rolls
        self.exps = dict(zip(rolls,exps))
        self.pref_names = pref_names
        self.prefs = []

    """
    Returns the applicant in CSV format
    Takes the sepperator character
    """
    def serialize(self, sep_char):
        return sep_char.join([self.name]+ [ roll + sep_char + self.exps[roll] for roll in self.rolls ] + self.pref_names)

    """
    Returns a number indicating preference of a team
    (0 : first choice, 1 : second choice...)
    Numbers are not necessarily unique
    """
    def _get_pref(self, team):
        if team.name in self.pref_names:
            return self.pref_names.index(team.name)
        else:
            return len(self.pref_names)

    """
    Takes the world of teams the applicant will prioritize
    Must be called before Get First Choice
    """
    def set_teams(self, teams):
        self.prefs = sorted(teams, key = self._get_pref)

    """
    Returns the applicant's firs-choice team
    """
    def get_first_choice(self):
        return self.prefs[0]

    """
    To be called after the applicant has been rejected from a team
    The applicant will not apply to that team again
    """
    def rejected(self, team):
        self.prefs.remove(team)

    """
    Returns True if the applicant has been rejected from every team
    """
    def done(self):
        return not len(self.prefs)

"""
A class to represent teams/projects applicants can be put on
"""
class Team():

    """
    name : the string name of the project (same from pref_names in App)
    rolls : list of strings of rolls needed
    spaces : number of spaces on the team
    product : is the project product oriented
    """
    def __init__(self, name, rolls, spaces, product = False):
        def zeros():
            while True:
                yield 0
        self.name = name
        self.rolls = rolls
        self.roll_counts = defaultdict(int)
        self.exp_counts = defaultdict(int)
        self.spaces = spaces
        self.members = []
        if product:
            self._get_pref = self._product_get_pref

    """
    Returns the team in CSV format
    Takes the sepperator character
    DOES NOT INCLUDE INFO ABOUT CURRENT TEAM MEMBERS
    """
    def serialize(self, sep_char):
        return sep_char.join([self.name]+self.rolls)

    """
    Returns a turple (for use in lexicological sorting) indicating
    the teams preference for a member
    """
    def _get_pref(self, app):
        roll_unneeded = [ not roll in self.rolls for roll in app.rolls ] #priorizes members whose rolls are needed
        had_rolls = set()
        def check_first(roll): #used to keep atleast one member of an overcrowed dept
            if roll in had_rolls:
                return 0
            had_rolls.add(roll)
            return -1
        have_roll = [ max([self.roll_counts[roll] - needed[roll], -1]) + check_first(roll) for roll in app.rolls ] #priortizes members with fewer other people in their dept
        exps = [ app.exps[roll] for roll in app.rolls ] #favor inexperianced membrs
        passion = 0
        """
        Comment the bellow list to recude number of first and last choice assignments
        """
        passion = -1*len(app.prefs) #favor members who wanted to be on the team more
        have_exp = [ self.exp_counts[exp] for exp in exps ] #favor members with a different level of experiance than other members
        """
        Change the bellow line to re-rank priorities (will need to change Product Get Pref accordingly)
        """
        return (roll_unneeded, passion, have_roll, have_exp, exps) 

    """
    An altered priority algorithm for product-oriented teams
    Forsakes diverse levels of experiance for maxing experience level
    """
    def _product_get_pref(self, app):
        default = Team._get_pref(self, app)
        return (default[0], default[1], default[2], [-1* e for e in default[-1]])

    """
    A helper function that tracks the reprsentation of experiance levels and rolls
    Must be called with co = 1 on new members
    Must be called with co = -1 on leaving members
    """
    def _account(self, app, co = 1):
        primary = True
        for roll in app.rolls:
            v = co*(1 if primary else 0.3)
            self.roll_counts[roll] += v
            self.exp_counts[app.exps[roll]] += v
            primary = False
        self.spaces -= co

    """
    Takes a applicant applying to the team
    Returns any applicant removed from the team (may be none)
    """
    def apply(self, app):
        self._account(app)
        self.members.append(app)
        self.members.sort(key=self._get_pref) #keeps members sort most->least valuable
        if self.spaces < 0: #only removes members in the team is full
            reject = self.members.pop(-1)
            self._account(reject, -1)
            return reject