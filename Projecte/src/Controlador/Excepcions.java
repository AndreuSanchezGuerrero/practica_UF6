package Controlador;

public class Excepcions {
    //--- CLASSE ILLEGALARGUMENTEXCEPTION ---
    static class illegalArgumentException extends Exception {
        public illegalArgumentException(String message) {
            super(message);
        }
    }
}
