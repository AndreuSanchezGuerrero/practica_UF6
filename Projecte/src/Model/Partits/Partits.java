package Model.Partits;

public class Partits {
    public String game_id;
    public String season_year;
    public int home_team_id;
    public int away_team_id;

    // Constructor
    public Partits(String game_id, String season_year, int home_team_id, int away_team_id) {
        this.game_id = game_id;
        this.season_year = season_year;
        this.home_team_id = home_team_id;
        this.away_team_id = away_team_id;
    }

    // Getters y setters
    public String getGame_id() { return game_id; }
    public void setGame_id(String game_id) { this.game_id = game_id; }
    public String getSeason_year() { return season_year; }
    public void setSeason_year(String season_year) { this.season_year = season_year; }
    public int getHome_team_id() { return home_team_id; }
    public void setHome_team_id(int home_team_id) { this.home_team_id = home_team_id; }
    public int getAway_team_id() { return away_team_id; }
    public void setAway_team_id(int away_team_id) { this.away_team_id = away_team_id; }


}
