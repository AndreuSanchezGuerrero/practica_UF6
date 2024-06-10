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
                        System.out.println("Seleccionat: Llistar tots els jugadors d'un equip");
                        llistarJugadorsEquips();
                        break;
                    case 2:
                        System.out.println("Seleccionat: Calcular la mitjana de punts, rebots, assistències, etc. d'un jugador");
                        calcularMitjanaJugador();
                        break;
                    case 3:
                        System.out.println("Seleccionat: Llistar tots els partits jugats per un equip amb el seu resultat");
                        llistarPartitsEquips();
                        break;
                    case 4:
                        System.out.println("Seleccionat: Afegir un nou jugador a un equip");
                        inserirNouJugador();
                        break;
                    case 5:
                        System.out.println("Seleccionat: Traspassar un jugador a un altre equip");
                        traspassarJugador();
                        break;
                    case 6:
                        System.out.println("MANTENIMENT");
                        break;
                    case 7:
                        System.out.println("Seleccionat: Modificar les estadístiques d'un jugador");
                        modificarEstadistiquesJugador();
                        break;
                    case 8:
                        System.out.println("Seleccionat: Retirar (Eliminar) un jugador");
                        retirarJugador();
                        break;
                    case 9:
                        System.out.println("Seleccionat: Canviar el nom de la franquícia d’un equip");
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
                scanner.next(); // Limpiar el buffer del scanner
            } catch (Exception e) {
                System.out.println("Error: " + e.getMessage());
                e.printStackTrace(); // Añadir rastreo de la pila para más detalles del error
            }

        } while (opcio != 0);
    }

    private void llistarJugadorsEquips() throws Exception {
        String nomEquip = Vista.demanarText("Introdueix el nom d'un equip per llistar els seus jugadors: ");
        System.out.println("Nom de l'equip introduït: " + nomEquip);
        validarNomEquip(nomEquip);

        String temporada = Vista.demanarText("Introdueix l'any de la temporada (e.g., 2022): ");
        System.out.println("Temporada introduïda: " + temporada);

        List<Jugadors> jugadors = jugadorsDAO.getPlayersByTeamNameAndSeason(nomEquip, temporada);
        System.out.println("Jugadors trobats: " + jugadors.size());

        if (jugadors.isEmpty()) {
            Vista.mostrarMissatge("No s'han trobat jugadors per a l'equip " + nomEquip + " en la temporada " + temporada);
        } else {
            Vista.llistarJugadorsEquip(jugadors);
        }
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
