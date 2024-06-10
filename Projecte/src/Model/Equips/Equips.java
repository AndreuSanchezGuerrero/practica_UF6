package Model.Equips;

public class Equips {
    public static int id;
    public String team_name;
    public String team_abbrevation;


    // Constructor
    public Equips(int id, String team_name, String team_abbrevation) {
        this.id = id;
        this.team_name = team_name;
        this.team_abbrevation = team_abbrevation;

    }

    // Getters y setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getFullName() { return team_name; }
    public void setFullName(String team_name) { this.team_name = team_name; }
    public String getAbbrevation() { return team_abbrevation; }
    public void setAbbrevation(String team_abbrevation) { this.team_abbrevation = team_abbrevation; }

}