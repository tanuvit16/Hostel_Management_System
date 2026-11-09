
package hms;

public class Main {

    public static void main(String[] args) {

        System.out.println("==================================");
        System.out.println(" HOSTEL MANAGEMENT SYSTEM");
        System.out.println(" Java JDBC Backend");
        System.out.println("==================================");

        try {
            // Verify MySQL connectivity first
            try (java.sql.Connection con = Database.getConnection()) {
                System.out.println("MySQL Database Connected!");
            }

            // Start HTTP API
            ApiServer.start();

        } catch (Exception e) {
            System.out.println("Backend startup failed!");
            e.printStackTrace();
        }
    }
}
