package Model.StatsJugadors;

public class Stats {
    private static int player_id;
    private static int game_id;
    private static int team_id;
    private static float pts;

    public Stats(int player_id, int game_id, int team_id, float pts) {
        this.player_id = player_id;
        this.game_id = game_id;
        this.team_id = team_id;
        this.pts = pts;
    }

    public static int getPlayer_id() {return player_id;}

    public static int getGame_id() {return game_id;}

    public static int getTeam_id() {return team_id;}

    public static float getPts() {return pts;}

    public void setPlayer_id(int player_id) {this.player_id = player_id;}

    public void setGame_id(int game_id) {this.game_id = game_id;}

    public void setTeam_id(int team_id) {this.team_id = team_id;}

    public void setPts(float pts) {this.pts = pts;}

}

