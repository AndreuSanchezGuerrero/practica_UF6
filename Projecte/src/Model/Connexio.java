package Model;

import Vista.Vista;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Connexio {

    private static final String HOST = Vista.demanarText("Introdueix la IP: ");
    private static final String USER = Vista.demanarText("Introdueix l'usuari: ");
    private static final String PASSWORD = Vista.demanarText("Introdueix la password: ");
    private static final String DATABASE = Vista.demanarText("Introdueix el nom de la base de dades: ");
    private static final String PORT = Vista.demanarText("Introdueix el port (per defecte 3306): ");

    // Conexió amb el DriverManager
    public static Connection getConnexio() throws SQLException {
        Connection conne = null;
        String url = "jdbc:mysql://" + HOST + ":" + PORT + "/" + DATABASE + "?useSSL=false&serverTimezone=UTC";
        try {
            conne = DriverManager.getConnection(url, USER, PASSWORD);
            System.out.println("Connexió realitzada amb èxit");
        } catch (SQLException e) {
            System.out.println("Error, no es pot connectar a la base de dades");
            e.printStackTrace(); // Imprimir la traça completa de l'error per depuració
        }
        return conne;
    }
}
