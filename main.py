import load_data
import gale_shapley

team_file = "teams.tsv"
app_file = "applicants.tsv"
out_file = "out.csv"

if __name__ == "__main__":
    print("Starting...")
    teams = load_data.load_file(team_file,load_data.team)
    print("Loaded teams...")
    apps = load_data.load_file(app_file, load_data.app)
    print("Loaded applicants...")
    teams, rejects, itterations = gale_shapley.run(teams, apps)
    print("Process done in "+str(itterations)+" iterations...")
    with open(out_file, 'w') as f:
        sep_char = ","
        for team in teams:
            #f.write("==\t"+team.Data_read_from)
            f.write("'=="+sep_char+team.serialize(sep_char)+'\n')
            for member in team.members:
                #f.write(team.name+"\t"+member.Data_read_from)
                f.write(team.name + sep_char + member.serialize(sep_char)+'\n')
        f.write("'=="+sep_char+"Teamless\n")
        for reject in rejects:
            f.write(reject.Data_read_from)
    print("File written")