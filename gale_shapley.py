"""
Interface for applicants:
    set_teams([team]) -> None
    get_first_choice() -> team
    rejected(team) -> None
    done() -> bool

Interface for teams:
    apply(applicant) -> nullable applicant
"""

def run(teams, apps):
    i = 0 #TESTING
    full_teams = set()
    num_teams = len(teams)
    rejects = []
    for app in apps:
        app.set_teams(teams)
    while len(apps):
        app = apps.pop()
        team = app.get_first_choice()
        reject = team.apply(app)
        #print(str(i) + ": " + app.name + " applied to " + team.name) #TESTING
        if reject != None:
            #print(reject.name + " removed from " + team.name) #TESTING
            reject.rejected(team)
            if not(reject.done()):
                apps.append(reject)
            else:
                rejects.append(app)
            if reject == app:
                full_teams.add(team)
                if len(full_teams) == num_teams:
                    break
        else:
            full_teams = set()
        i += 1 #TESTING
    return (teams, rejects+apps, i)