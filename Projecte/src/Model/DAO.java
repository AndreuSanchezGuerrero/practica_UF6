package Model;
import java.sql.Connection;
import java.sql.SQLException;

public interface DAO<T> {
    //Insertar
    boolean insertar(T obj, Connection connexio) throws SQLException;
    //Actualitzar
    boolean actualitzar(T obj, Connection connexio) throws SQLException;
    //Esborrar
    boolean esborrar(T obj, Connection connexio) throws SQLException;
    //Cercar
    T cercar(int id, Connection connexio) throws SQLException;
    //Contar
    int count(Connection connexio) throws SQLException;
}
