package Vista;

import Model.Jugadors.Jugadors;

import java.util.*;

public class Vista {

    public static void mostrarMenu() {
        System.out.println("Benvingut a la nostra base de dades de la NBA");
        System.out.println("Quina acció vols realitzar?");
        System.out.println("1) Llistar tots els jugadors d'un equip");
        System.out.println("2) Calcular la mitjana de punts, rebots, assistències, etc. d'un jugador");
        System.out.println("3) Llistar tots els partits jugats per un equip amb el seu resultat");
        System.out.println("4) Afegir un nou jugador a un equip--MANTENIMENT");
        System.out.println("5) Traspassar un jugador a un altre equip");
        System.out.println("6) Actualitzar les dades de jugadors o equips després d'un partit --MANTENIMENT");
        System.out.println("7) Modificar les estadístiques d'un jugador--MANTENIMENT");
        System.out.println("8) Retirar (Eliminar) un jugador--MANTENIMENT");
        System.out.println("9) Canviar el nom de la franquícia d’un equip--MANTENIMENT");
        System.out.println("0) Sortir");
    }

    // Método para listar jugadores de un equipo
    public static void llistarJugadorsEquip(List<Jugadors> jugadors) {
        for (Jugadors jugador : jugadors) {
            System.out.println(jugador.getPlayer_nickname() + " " + jugador.getPlayer_name());
        }
    }

    // Método para listar las medias de un jugador
    public static void mostrarMitjanaPunts(double mitjana) {
        System.out.println(mitjana);
    }

    // Método para listar partidos y resultados de un equipo
    public static void llistarPartitsIResultats(List<String> llista) {
        for (String partit: llista) {
            System.out.println(partit);
        }
    }

    // Método para mostrar un mensaje
    public static void mostrarMissatge(String missatge) {
        System.out.println(missatge);
    }

    // Método para solicitar un texto al usuario
    public static String demanarText(String missatge) {
        System.out.println(missatge);
        Scanner scanner = new Scanner(System.in);
        return scanner.nextLine();
    }
}
