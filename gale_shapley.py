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
    full_teams = set()
    num_teams = len(teams)
    rejects = []
    for app in apps:
        app.set_teams(teams)
    while len(apps):
        app = apps.pop()
        team = app.get_first_choice()
        reject = team.apply(app)
        if reject != None:
            reject.rejected(team)
            if not(reject.done()):
                apps.append(reject)
            else:
                rejects.append(app)
            if reject == app
                full_teams.add(team)
                if len(full_teams) == num_teams:
                    break
        else:
            full_teams = set()
    return (teams, rejects+apps)