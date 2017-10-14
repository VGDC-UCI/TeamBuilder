import load_data
import gale_shapley

if __name__ == "__main__":
    print("Starting...")
    teams = load_data.load_file("teams.csv",load_data.team)
    print("Loaded teams...")
    apps = load_data.load_file("applicants.csv", load_data.app)
    print("Loaded applicants...")
    _, rejects = gale_shapley.run(teams, apps)
    print("Process done...")
    with open("out.csv") as f:
        for team in teams:
            f.write(team.Data_read_from+'\n')
            for member in teams:
                f.write(member.Data_read_from+'\n')
        f.write("Teamless\n")
        for reject in rejects:
            f.write(reject.Data_read_from+'\n')