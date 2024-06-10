package Model.Jugadors;

import Model.Equips.Equips;
import Model.Jugadors.Jugadors;
import Model.StatsJugadors.Stats;
import Vista.Vista;
import Model.DAO;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class JugadorsDAO {
    private Connection connection;

    public JugadorsDAO(Connection connection) {
        this.connection = connection;
    }
    

    // Create
    public void addPlayer(Jugadors Jugador) throws SQLException {
        String query = "INSERT INTO players (player_id, player_name, player_nickname, team_id, team_name, seasonYear) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, Jugador.getPlayer_id());
            stmt.setString(2, Jugador.getPlayer_name());
            stmt.setString(3, Jugador.getPlayer_nickname());
            stmt.setInt(4, Jugador.getTeam_Id());
            stmt.setString(5, Jugador.getTeam_name());
            stmt.setString(6, Jugador.getSeasonYear());
            stmt.executeUpdate();
        }
    }

    // Read by ID
    public Jugadors getPlayerById(int playerId) throws SQLException {
        String query = "SELECT * FROM players WHERE player_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, playerId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new Jugadors(
                        rs.getInt("player_id"),
                        rs.getString("player_name"),
                        rs.getString("player_nickname"),
                        rs.getInt("team_id"),
                        rs.getString("team_name"),
                        rs.getString("seasonYear")
                );
            }
        }
        return null;
    }

    // Llistar jugadors per nom d'equip
    public List<Jugadors> getPlayersByTeamName(String teamName) throws SQLException {
        List<Jugadors> players = new ArrayList<>();
        String query = "SELECT * FROM players WHERE team_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, teamName);
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                players.add(new Jugadors(
                        rs.getInt("player_id"),
                        rs.getString("player_name"),
                        rs.getString("player_nickname"),
                        rs.getInt("team_id"),
                        rs.getString("team_name"),
                        rs.getString("seasonYear")
                ));
            }
        }
        return players;
    }



    // Read all
    public List<Jugadors> getAllPlayers() throws SQLException {
        List<Jugadors> players = new ArrayList<>();
        String query = "SELECT * FROM players";
        try (Statement stmt = connection.createStatement()) {
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                players.add(new Jugadors(
                        rs.getInt("player_id"),
                        rs.getString("player_name"),
                        rs.getString("player_nickname"),
                        rs.getInt("team_id"),
                        rs.getString("team_name"),
                        rs.getString("seasonYear")
                ));
            }
        }
        return players;
    }

    // Update
    public void updatePlayer(Jugadors player) throws SQLException {
        String query = "UPDATE players SET player_name = ?, player_nickname = ?, team_id = ?, team_name = ?, seasonYear = ? WHERE player_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, player.getPlayer_name());
            stmt.setString(2, player.getPlayer_nickname());
            stmt.setInt(3, player.getTeam_Id());
            stmt.setString(4, player.getTeam_name());
            stmt.setString(5, player.getSeasonYear());
            stmt.setInt(6, player.getPlayer_id());
            stmt.executeUpdate();
        }
    }

    // Traspassar un jugador a un altre equip
    public void transferPlayer(String playerName, Equips equips) throws SQLException {
        String updateQuery = "UPDATE players SET team_name = ?, team_id = ? WHERE player_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(updateQuery)) {
            stmt.setString(1, equips.getFullName());
            stmt.setInt(2, equips.getId());
            stmt.setString(3, playerName);
            stmt.executeUpdate();
        }
    }

    // Actualitzar les estadístiques dels jugadors després d'un partit
    public void updatePlayerStats(List<Stats> playerStatsList) throws SQLException {
        String updateQuery = "INSERT INTO playerstats (player_id, game_id, team_id, pts) VALUES (?, ?, ?, ?) " +
                "ON DUPLICATE KEY UPDATE pts = VALUES(pts)";
        try (PreparedStatement stmt = connection.prepareStatement(updateQuery)) {
            for (Stats stats : playerStatsList) {
                stmt.setInt(1, stats.getPlayer_id());
                stmt.setInt(2, stats.getGame_id());
                stmt.setInt(3, stats.getTeam_id());
                stmt.setFloat(4, stats.getPts());
                stmt.executeUpdate();
            }
        }
    }

    // Modificar les estadístiques d'un jugador
    public void updatePlayerStats(String playerName, int gameId, int points) throws SQLException {
        String updateQuery = "UPDATE playerstats ps " +
                "JOIN players p ON ps.player_id = p.player_id " +
                "SET ps.pts = ?" +
                "WHERE p.player_name = ? AND ps.game_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(updateQuery)) {
            stmt.setInt(1, points);
            stmt.setString(2, playerName);
            stmt.setInt(3, gameId);
            stmt.executeUpdate();
        }
    }

    // Delete
    public void deletePlayer(int playerId) throws SQLException {
        String query = "DELETE FROM players WHERE player_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, playerId);
            stmt.executeUpdate();
        }
    }
}