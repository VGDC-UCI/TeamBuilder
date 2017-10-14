from collections import defaultdict

needed = {"Artist" : 2, "Gameplay Designer" : 2, "Audio Designer" : 1, "Producer" : 1, "Programmer" : 3, "Writer" : 1}

#all priority lists highest -> lowest

class App():

    def __init__(self, name, rolls, exps, pref_names):
        self.name = name
        self.rolls = rolls
        self.exps = dict(zip(rolls,exps))
        self.pref_names = pref_names
        self.prefs = []

    def serialize(self, sep_char):
        return sep_char.join([self.name]+ [ roll + sep_char + self.exps[roll] for roll in self.rolls ] + self.pref_names)

    def _get_pref(self, team):
        if team.name in self.pref_names:
            return self.pref_names.index(team.name)
        else:
            return len(self.pref_names)

    def set_teams(self, teams):
        self.prefs = sorted(teams, key = self._get_pref)

    def get_first_choice(self):
        return self.prefs[0]

    def rejected(self, team):
        self.prefs.remove(team)

    def done(self):
        return not len(self.prefs)

class Team():

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

    def serialize(self, sep_char):
        return sep_char.join([self.name]+self.rolls)

    def _get_pref(self, app):
        roll_unneeded = [ not roll in self.rolls for roll in app.rolls ]
        have_roll = [ self.roll_counts[roll] - needed[roll] for roll in app.rolls ]
        exps = [ app.exps[roll] for roll in app.rolls ] #favor inexperianced membrs
        have_exp = [ self.exp_counts[exp] for exp in exps ]
        return (roll_unneeded, have_roll, have_exp, exps)

    def _product_get_pref(self, app):
        default = Team._get_pref(self, app)
        return (default[0], default[1], [-1* e for e in default[3]])

    def _account(self, app, co = 1):
        primary = True
        for roll in app.rolls:
            v = co*(1 if primary else 0.3)
            self.roll_counts[roll] += v
            self.exp_counts[app.exps[roll]] += v
            primary = False
        self.spaces -= co

    def apply(self, app):
        self._account(app)
        self.members.append(app)
        self.members.sort(key=self._get_pref)
        if self.spaces < 0:
            reject = self.members.pop(-1)
            self._account(reject, -1)
            return reject