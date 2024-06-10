package Model.StatsJugadors;

import Model.Jugadors.Jugadors;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class StatsDAO {
    private Connection connection;

    public StatsDAO(Connection connection) {
        this.connection = connection;
    }

    //Insertar un EstadisticaJugador.
    public void insertar(Stats stats, Connection connexio) throws SQLException {
        PreparedStatement stmt = connexio.prepareStatement(
                "INSERT INTO playerstats (player_id,game_id,team_id,pts) VALUES (?,?,?,?)"
        );
        stmt.setInt(1,stats.getPlayer_id());
        stmt.setInt(2,stats.getGame_id());
        stmt.setInt(3,stats.getTeam_id());
        stmt.setFloat(4,stats.getPts());
    }

    public void actualitzar(Stats stats, Connection connexio) throws SQLException {
        PreparedStatement stmt = connexio.prepareStatement(
                "UPDATE playerstats SET player_id=?,game_id=?,team_id=?,pts=? WHERE player_id=?,game_id=?,team_id=?,pts=?"
        );
        stmt.setInt(1,stats.getPlayer_id());
        stmt.setInt(2,stats.getGame_id());
        stmt.setInt(3,stats.getTeam_id());
        stmt.setFloat(4,stats.getPts());
    }

    public void esborrar(Stats stats, Connection connexio) throws SQLException {
        PreparedStatement sentencia = connexio.prepareStatement(
                "DELETE FROM playerstats WHERE player_id = ? AND team_id = ? AND game_id = ?"
        );
        sentencia.setInt(1,stats.getPlayer_id());
        sentencia.setInt(2,stats.getTeam_id());
        sentencia.setInt(3,stats.getGame_id());
    }

    // Obtenir mitjana de punts d'un jugador per nom
    public double getPlayerPointsAverage(String playerName) throws SQLException {
        String query = "SELECT AVG(ps.pts) AS avg_pts FROM playerstats ps " +
                "JOIN players p ON ps.player_id = p.player_id WHERE p.player_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, playerName);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return rs.getDouble("avg_pts");
            }
        }
        return 0.0;
    }
}