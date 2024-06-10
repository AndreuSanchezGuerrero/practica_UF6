package Model.Equips;

import Model.Equips.Equips;
import Model.DAO;
import Vista.Vista;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class EquipsDAO {
    private Connection connection;

    public EquipsDAO(Connection connection) {
        this.connection = connection;
    }

    // Create
    public void addTeam(Equips equips) throws SQLException {
        String query = "INSERT INTO teams (id, team_name, team_abbreviation) VALUES (?, ?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, equips.getId());
            stmt.setString(2, equips.getFullName());
            stmt.setString(3, equips.getAbbrevation());
            stmt.executeUpdate();
        }
    }

    // Read by ID
    public Equips getTeamById(int teamId) throws SQLException {
        String query = "SELECT * FROM teams WHERE team_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, teamId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new Equips(
                        rs.getInt("team_id"),
                        rs.getString("team_name"),
                        rs.getString("team_abbreviation")
                );
            }
        }
        return null;
    }

    public Equips getTeamByName(String teamName) throws SQLException {
        String query = "SELECT * FROM teams WHERE team_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, teamName);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new Equips(
                        rs.getInt("team_id"),
                        rs.getString("team_name"),
                        rs.getString("team_abbreviation")
                );
            }
        }
        return null;
    }

    // Read all
    public List<Equips> getAllTeams() throws SQLException {
        List<Equips> teams = new ArrayList<>();
        String query = "SELECT * FROM teams";
        try (Statement stmt = connection.createStatement()) {
            ResultSet rs = stmt.executeQuery(query);
            while (rs.next()) {
                teams.add(new Equips(
                        rs.getInt("team_id"),
                        rs.getString("team_name"),
                        rs.getString("team_abbreviation")
                ));
            }
        }
        return teams;
    }

    // Update
    public void updateTeam(Equips equips) throws SQLException {
        String query = "UPDATE teams SET team_name = ?, team_abbreviation = ? WHERE team_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setString(1, equips.getFullName());
            stmt.setString(2, equips.getAbbrevation());
            stmt.setInt(3, equips.getId());
            stmt.executeUpdate();
        }
    }

    // Canviar el nom de la franquícia d'un equip
    public void updateTeamName(String currentTeamName, String newTeamName) throws SQLException {
        String updateQuery = "UPDATE teams SET team_name = ? WHERE team_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(updateQuery)) {
            stmt.setString(1, newTeamName);
            stmt.setString(2, currentTeamName);
            stmt.executeUpdate();
        }

        // També actualitzem el nom de l'equip a la taula de jugadors
        String updatePlayersQuery = "UPDATE players SET team_name = ? WHERE team_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(updatePlayersQuery)) {
            stmt.setString(1, newTeamName);
            stmt.setString(2, currentTeamName);
            stmt.executeUpdate();
        }

        // També actualitzem el nom de l'equip a la taula de partits
        String updateGamesQuery = "UPDATE games SET team_name = ? WHERE team_name = ?";
        try (PreparedStatement stmt = connection.prepareStatement(updateGamesQuery)) {
            stmt.setString(1, newTeamName);
            stmt.setString(2, currentTeamName);
            stmt.executeUpdate();
        }
    }

    // Delete
    public void deleteTeam(int teamId) throws SQLException {
        String query = "DELETE FROM teams WHERE team_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(query)) {
            stmt.setInt(1, teamId);
            stmt.executeUpdate();
        }
    }
}