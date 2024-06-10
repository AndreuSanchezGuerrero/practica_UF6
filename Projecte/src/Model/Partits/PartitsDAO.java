package Model.Partits;

import Model.Partits.Partits;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class PartitsDAO {
    private Connection connection;

    public PartitsDAO(Connection connection) {
        this.connection = connection;
    }

    // Llistar partits per nom d'equip
    //La consulta SQL selecciona el nom de l'equip local i visitant, així com la suma dels punts dels jugadors d'aquests equips per obtenir el resultat final.
    //El mètode retorna una llista de cadenes que conté els resultats dels partits en el format equip_local – equip_visitant: punts_local – punts_visitant.
    public List<String> getGamesByTeamName(String teamName) throws SQLException {
        List<String> games = new ArrayList<>();
        String query = "SELECT g.game_id, t1.team_name AS home_team, t2.team_name AS away_team, " +
                "SUM(CASE WHEN ps.team_id = g.home_team_id THEN ps.pts ELSE 0 END) AS home_team_pts, " +
                "SUM(CASE WHEN ps.team_id = g.away_team_id THEN ps.pts ELSE 0 END) AS away_team_pts " +
                "FROM games g " +
                "JOIN playerstats ps ON g.game_id = ps.game_id " +
                "JOIN teams t1 ON g.home_team_id = t1.team_id " +
                "JOIN teams t2 ON g.away_team_id = t2.team_id " +
                "WHERE t1.team_name = ? OR t2.team_name = ? " +
                "GROUP BY g.game_id, t1.team_name, t2.team_name";

        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, teamName);
            stmt.setString(2, teamName);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                String gameResult = rs.getString("home_team") + " – " + rs.getString("away_team") + ": " +
                        rs.getInt("home_team_pts") + " – " + rs.getInt("away_team_pts");
                games.add(gameResult);
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        return games;
    }
}
