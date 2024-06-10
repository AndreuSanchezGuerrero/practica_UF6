package Model.Jugadors;

public class Jugadors {
    private int player_id;
    private String player_name;
    private String player_nickname;
    private int team_id;
    private String team_name;
    private String seasonYear;

    // Constructor
    public Jugadors(int player_id, String player_name, String player_nickname, int team_id, String team_name, String seasonYear) {
        this.player_id = player_id;
        this.player_name = player_name;
        this.player_nickname = player_nickname;
        this.team_id = team_id;
        this.team_name = team_name;
        this.seasonYear = seasonYear;
    }

    // Getters and Setters
    public int getPlayer_id() {
        return player_id;
    }

    public void setPlayer_id(int player_id) {
        this.player_id = player_id;
    }

    public String getPlayer_name() {
        return player_name;
    }

    public void setPlayer_name(String player_name) {
        this.player_name = player_name;
    }

    public String getPlayer_nickname() {
        return player_nickname;
    }

    public void setPlayer_nickname(String player_nickname) {
        this.player_nickname = player_nickname;
    }

    public int getTeam_Id() {
        return team_id;
    }

    public void setTeam_Id(int team_id) {
        this.team_id = team_id;
    }

    public String getTeam_name() {
        return team_name;
    }

    public void setTeam_name(String team_name) {
        this.team_name = team_name;
    }

    public String getSeasonYear() {
        return seasonYear;
    }

    public void setSeasonYear(String seasonYear) {
        this.seasonYear = seasonYear;
    }
}
