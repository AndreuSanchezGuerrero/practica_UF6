//--- IMPORTS ---
package Controlador;
import Model.Connexio;
import Vista.Vista;

import Model.Equips.EquipsDAO;
import Model.Jugadors.JugadorsDAO;
import Model.Partits.PartitsDAO;
import Model.StatsJugadors.StatsDAO;

import Model.Jugadors.Jugadors;
import Model.Equips.Equips;
import Model.Partits.Partits;
import Model.Seasons.Seasons;
import Model.Seasons.SeasonsDAO;
import Model.StatsJugadors.Stats;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


//--- CLASSE CONTROLADOR ---
public class Controlador {
    private static Connection connection;

    static {
        try {
            connection = Connexio.getConnexio();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    private EquipsDAO equipsDAO = new EquipsDAO(connection);
    private JugadorsDAO jugadorsDAO = new JugadorsDAO(connection);
    private PartitsDAO partitsDAO = new PartitsDAO(connection);
    private StatsDAO statsDAO = new StatsDAO(connection);
    //private SeasonsDAO seasonsDAO = new ;

    public void controladorMenu() {
        Scanner scanner = new Scanner(System.in);
        int opcio = -1; // Inicializamos la variable opcio

        do {
            // Mostrar el menú
            Vista.mostrarMenu();

            try {
                // Comprobar que la entrada es un número
                if (!scanner.hasNextInt()) {
                    throw new IllegalArgumentException("Has de posar un numero");
                }
                opcio = scanner.nextInt();

                // Cridem al mètode correspondent
                switch (opcio) {
                    case 1:
                        llistarJugadorsEquips();
                        break;
                    case 2:
                        calcularMitjanaJugador();
                        break;
                    case 3:
                        llistarPartitsEquips();
                        break;
                    case 4:
                        inserirNouJugador();
                        break;
                    case 5:
                        traspassarJugador();
                        break;
                    case 6:
                        actualitzarDades();
                        break;
                    case 7:
                        modificarEstadistiquesJugador();
                        break;
                    case 8:
                        retirarJugador();
                        break;
                    case 9:
                        canviarNomFranquicia();
                        break;
                    case 0:
                        System.out.println("Sortint...");
                        break;
                    default:
                        System.out.println("Error, has de posar un numero del 0 al 9");
                        break;
                }
            } catch (IllegalArgumentException e) {
                System.out.println("Error: " + e.getMessage());
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
            }

        } while (opcio != 0);
    }


    private void llistarJugadorsEquips() throws Exception {
        String nomEquip = Vista.demanarText("Introdueix el nom d'un equip per llistar els seus jugadors: ");
        validarNomEquip(nomEquip);
        Vista.llistarJugadorsEquip(jugadorsDAO.getPlayersByTeamName(nomEquip));
    }

    private void calcularMitjanaJugador() throws Exception {
        String nomJugador = Vista.demanarText("Introdueix un jugador per calcular la seva mitjana de punts: ");
        validarNomJugador(nomJugador);
        Vista.mostrarMitjanaPunts(statsDAO.getPlayerPointsAverage(nomJugador));
    }

    private void llistarPartitsEquips() throws Exception {
        String nomEquip = Vista.demanarText("Introdueix el nom d'un equip per llistar tots els partits i els seus resultats: ");
        validarNomEquip(nomEquip);
        Vista.llistarPartitsIResultats(partitsDAO.getGamesByTeamName(nomEquip));
    }

    private void inserirNouJugador() throws Exception {
        String nomJugador = Vista.demanarText("Introdueix un jugador per inserir a la taula: ");
        validarNomJugador(nomJugador);
        String nomEquip = Vista.demanarText("Introdueix un equip on unir a aquest jugador: ");
        validarNomEquip(nomEquip);
        jugadorsDAO.addPlayer(new Jugadors(0, nomJugador, "", 0, "",""));
        Vista.mostrarMissatge("Jugador afegit");
    }

    private void traspassarJugador() throws Exception {
        String nomJugador = Vista.demanarText("Introdueix un jugador per traspassar a un altre equip: ");
        validarNomJugador(nomJugador);
        String nouEquip = Vista.demanarText("Introdueix un equip on traspassar aquest jugador: ");
        validarNomEquip(nouEquip);
        jugadorsDAO.transferPlayer(nomJugador, equipsDAO.getTeamByName(nouEquip));
        Vista.mostrarMissatge("Jugador transferit");
    }

    private void actualitzarDades() throws Exception {
        String fitxerPartit = Vista.demanarText("Introdueix el nom del fitxer amb les dades del partit: ");

        BufferedReader lector = new BufferedReader(new FileReader(fitxerPartit));
        String linea;

        List<Stats> stats = new ArrayList<>();
        lector.readLine();

        while ((linea = lector.readLine()) != null) {
            String[] fields = linea.split(",");
            int playerId = Integer.parseInt(fields[0]);
            int gameId = Integer.parseInt(fields[1]);
            int teamId = Integer.parseInt(fields[2]);
            int pts = Integer.parseInt(fields[3]);

            Stats stat = new Stats(playerId,gameId,teamId,pts);
            stats.add(stat);
        }

        jugadorsDAO.updatePlayerStats(stats);
    }

    private void modificarEstadistiquesJugador() throws Exception {
        String nomJugador = Vista.demanarText("Introdueix un jugador per modificar les seves estadístiques: ");
        validarNomJugador(nomJugador);
    }

    private void retirarJugador() throws Exception {
        String nomJugador = Vista.demanarText("Introdueix un jugador per eliminar-lo: ");
        validarNomJugador(nomJugador);
        //Vista.mostrarMissatge(jugadorsDAO.(nomJugador));
    }

    private void canviarNomFranquicia() throws Exception {
        String nomEquip = Vista.demanarText("Introdueix un equip per modificar la seva franquícia: ");
        validarNomEquip(nomEquip);
        String novaFranquicia = Vista.demanarText("Introdueix la nova franquícia: ");
        validarNomEquip(novaFranquicia);
        equipsDAO.updateTeamName(nomEquip, novaFranquicia);
        Vista.mostrarMissatge("Nom canviat");
    }

    // Métodos auxiliares para la validación usando expresiones regulares
    private static void validarNomEquip(String nom) throws Exception {
        if (!nom.matches("[a-zA-Z\\s]+")) {
            throw new Exception("El nom d'un equip no pot contenir números.");
        }
    }

    private static void validarNomJugador(String nom) throws Exception {
        if (!nom.matches("[a-zA-Z\\s]+")) {
            throw new Exception("Un nom només pot contenir lletres.");
        }
    }
}
