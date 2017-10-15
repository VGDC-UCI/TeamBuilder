"""
Takes a list of teams, and a list of applicants (interfaces bellow)
and produces stable marriage between them. 
Returns (teams, rejected applicants, itterations taken)

Interface for applicants:
    set_teams([team]) -> None
    get_first_choice() -> team
    rejected(team) -> None
    done() -> bool

Interface for teams:
    apply(applicant) -> nullable applicant
"""

def run(teams, apps):
    i = 0 #Counts itterations
    full_teams = set() #set of all teams that have finalized/stopped changing
    num_teams = len(teams) #number of teams
    rejects = [] #list of applicants all teams have rejected
    for app in apps:
        #initialize the applicants
        app.set_teams(teams)
    while len(apps):
        app = apps.pop()
        team = app.get_first_choice()
        reject = team.apply(app)
        if reject != None:
            reject.rejected(team)
            #if the applicant has no more prefs, do not requeue them
            if not(reject.done()): 
                apps.append(reject)
            else:
                rejects.append(app)
            #if the team reject the applicant, assume the team has stopped changing
            if reject == app:
                full_teams.add(team)
                #if all teams have stopped changing, stop the algorithm
                if len(full_teams) == num_teams:
                    break
        else:
            #if find a place for an applicant, assume any team could still change
            full_teams = set()
        i += 1
    return (teams, rejects+apps, i)