
package hms;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.sql.*;
import java.util.*;

public class ApiServer {

    private static HttpServer server;

    public static void start() throws IOException {
        server = HttpServer.create(
            new InetSocketAddress("localhost", 8080), 0
        );

        server.createContext("/api/", ApiServer::handleRequest);
        server.setExecutor(null);
        server.start();

        System.out.println("Hostel Management API started!");
        System.out.println("URL: http://localhost:8080/api/");
    }

    private static void handleRequest(HttpExchange ex)
            throws IOException {

        try {
            Map<String, String> p = getParams(ex);
            String path = ex.getRequestURI().getPath();
            String method = ex.getRequestMethod();

            String result;

            if (path.equals("/api/login") && method.equals("POST")) {
                result = login(p);

            } else if (path.equals("/api/stats") && method.equals("GET")) {
                result = stats();

            } else if (path.equals("/api/students")) {
                result = students(method, p);

            } else if (path.equals("/api/rooms")) {
                result = rooms(method, p);

            } else if (path.equals("/api/allocations")) {
                result = allocations(method, p);

            } else if (path.equals("/api/fees")) {
                result = fees(method, p);

            } else {
                result = "{\"success\":false,\"message\":\"Invalid endpoint\"}";
                send(ex, 404, result);
                return;
            }

            send(ex, 200, result);

        } catch (Exception e) {
            e.printStackTrace();
            send(ex, 400,
                "{\"success\":false,\"message\":\""
                + escape(e.getMessage()) + "\"}");
        }
    }

    // Read URL parameters and POST form data
    private static Map<String, String> getParams(HttpExchange ex)
            throws IOException {

        Map<String, String> map = new HashMap<>();

        String query = ex.getRequestURI().getRawQuery();

        if (query != null) {
            parseParams(query, map);
        }

        if (!ex.getRequestMethod().equals("GET")) {
            String body = new String(
                ex.getRequestBody().readAllBytes(),
                StandardCharsets.UTF_8
            );
            parseParams(body, map);
        }

        return map;
    }

    private static void parseParams(
            String data, Map<String, String> map) {

        if (data == null || data.isEmpty()) return;

        for (String pair : data.split("&")) {
            String[] parts = pair.split("=", 2);

            String key = URLDecoder.decode(
                parts[0], StandardCharsets.UTF_8
            );

            String value = parts.length > 1
                ? URLDecoder.decode(parts[1], StandardCharsets.UTF_8)
                : "";

            map.put(key, value);
        }
    }

    private static String val(Map<String, String> p, String key) {
        return p.getOrDefault(key, "").trim();
    }

    private static void send(
            HttpExchange ex, int status, String response)
            throws IOException {

        byte[] bytes = response.getBytes(StandardCharsets.UTF_8);

        ex.getResponseHeaders().set(
            "Content-Type", "application/json; charset=UTF-8"
        );

        ex.getResponseHeaders().set(
            "Access-Control-Allow-Origin", "*"
        );

        ex.sendResponseHeaders(status, bytes.length);

        try (OutputStream os = ex.getResponseBody()) {
            os.write(bytes);
        }
    }

    private static String escape(String s) {
        if (s == null) return "";

        return s.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r");
    }

    private static String success(String message) {
        return "{\"success\":true,\"message\":\""
            + escape(message) + "\"}";
    }

    // Convert SQL results into JSON
    private static String getRows(
            String sql, Object... values) throws SQLException {

        StringBuilder json = new StringBuilder("[");
        
        try (Connection con = Database.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            for (int i = 0; i < values.length; i++) {
                ps.setObject(i + 1, values[i]);
            }

            try (ResultSet rs = ps.executeQuery()) {
                ResultSetMetaData md = rs.getMetaData();
                int columns = md.getColumnCount();

                boolean firstRow = true;

                while (rs.next()) {
                    if (!firstRow) json.append(",");
                    firstRow = false;

                    json.append("{");

                    for (int i = 1; i <= columns; i++) {
                        if (i > 1) json.append(",");

                        String name = md.getColumnLabel(i);
                        Object value = rs.getObject(i);

                        json.append("\"").append(escape(name)).append("\":");

                        if (value == null) {
                            json.append("null");
                        } else if (value instanceof Number) {
                            json.append(value);
                        } else {
                            json.append("\"")
                                .append(escape(value.toString()))
                                .append("\"");
                        }
                    }

                    json.append("}");
                }
            }
        }

        return json.append("]").toString();
    }

    // 1. ADMIN LOGIN
    private static String login(Map<String, String> p)
            throws SQLException {

        String sql = "SELECT admin_id FROM Admin "
                   + "WHERE username=? AND password=?";

        try (Connection con = Database.getConnection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, val(p, "username"));
            ps.setString(2, val(p, "password"));

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return "{\"success\":true,\"message\":\"Login successful\"}";
                }
            }
        }

        return "{\"success\":false,\"message\":\"Invalid username or password\"}";
    }

    // 2. DASHBOARD STATISTICS
    private static String stats() throws SQLException {

        String sql =
            "SELECT " +
            "(SELECT COUNT(*) FROM Students) AS total_students, " +
            "(SELECT COUNT(*) FROM Rooms) AS total_rooms, " +
            "(SELECT COUNT(*) FROM Rooms WHERE occupied > 0) AS occupied_rooms, " +
            "(SELECT COUNT(*) FROM Rooms WHERE occupied < capacity) AS available_rooms, " +
            "(SELECT COUNT(*) FROM Fees WHERE payment_status='Pending') AS pending_fees";

        String data = getRows(sql);

        return "{\"success\":true,\"data\":" + data + "}";
    }

    // 3. STUDENT MANAGEMENT
    private static String students(
            String method, Map<String, String> p)
            throws SQLException {

        if (method.equals("GET")) {
            String search = val(p, "search");

            String sql = "SELECT * FROM Students "
                       + "WHERE student_name LIKE ? "
                       + "OR roll_number LIKE ? "
                       + "OR phone_number LIKE ? "
                       + "ORDER BY student_id DESC";

            String s = "%" + search + "%";

            return "{\"success\":true,\"data\":"
                + getRows(sql, s, s, s) + "}";
        }

        if (method.equals("POST")) {
            String sql =
                "INSERT INTO Students "
                + "(student_name,roll_number,phone_number,email,"
                + "department,gender,student_type,address,"
                + "guardian_contact,facilities) "
                + "VALUES (?,?,?,?,?,?,?,?,?,?)";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setString(1, val(p, "student_name"));
                ps.setString(2, val(p, "roll_number"));
                ps.setString(3, val(p, "phone_number"));
                ps.setString(4, val(p, "email"));
                ps.setString(5, val(p, "department"));
                ps.setString(6, val(p, "gender"));
                ps.setString(7, val(p, "student_type"));
                ps.setString(8, val(p, "address"));
                ps.setString(9, val(p, "guardian_contact"));
                ps.setString(10, val(p, "facilities"));

                ps.executeUpdate();
            }

            return success("Student added successfully");
        }

        if (method.equals("PUT")) {
            String sql =
                "UPDATE Students SET student_name=?, roll_number=?, "
                + "phone_number=?, email=?, department=?, gender=?, "
                + "student_type=?, address=?, guardian_contact=?, "
                + "facilities=? WHERE student_id=?";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setString(1, val(p, "student_name"));
                ps.setString(2, val(p, "roll_number"));
                ps.setString(3, val(p, "phone_number"));
                ps.setString(4, val(p, "email"));
                ps.setString(5, val(p, "department"));
                ps.setString(6, val(p, "gender"));
                ps.setString(7, val(p, "student_type"));
                ps.setString(8, val(p, "address"));
                ps.setString(9, val(p, "guardian_contact"));
                ps.setString(10, val(p, "facilities"));
                ps.setInt(11, Integer.parseInt(val(p, "student_id")));

                if (ps.executeUpdate() == 0)
                    return "{\"success\":false,\"message\":\"Student not found\"}";
            }

            return success("Student updated successfully");
        }

        if (method.equals("DELETE")) {
            String sql = "DELETE FROM Students WHERE student_id=?";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, Integer.parseInt(val(p, "student_id")));

                if (ps.executeUpdate() == 0)
                    return "{\"success\":false,\"message\":\"Student not found\"}";
            }

            return success("Student deleted successfully");
        }

        return "{\"success\":false,\"message\":\"Invalid method\"}";
    }

    // 4. ROOM MANAGEMENT
    private static String rooms(
            String method, Map<String, String> p)
            throws SQLException {

        if (method.equals("GET")) {
            return "{\"success\":true,\"data\":"
                + getRows("SELECT * FROM Rooms ORDER BY room_id") + "}";
        }

        if (method.equals("POST")) {
            String sql =
                "INSERT INTO Rooms "
                + "(room_number,room_type,capacity,monthly_fee) "
                + "VALUES (?,?,?,?)";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setString(1, val(p, "room_number"));
                ps.setString(2, val(p, "room_type"));
                ps.setInt(3, Integer.parseInt(val(p, "capacity")));
                ps.setBigDecimal(4,
                    new java.math.BigDecimal(val(p, "monthly_fee")));

                ps.executeUpdate();
            }

            return success("Room added successfully");
        }

        if (method.equals("PUT")) {
            String sql =
                "UPDATE Rooms SET room_number=?, room_type=?, "
                + "capacity=?, monthly_fee=? WHERE room_id=? "
                + "AND capacity >= occupied";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setString(1, val(p, "room_number"));
                ps.setString(2, val(p, "room_type"));
                ps.setInt(3, Integer.parseInt(val(p, "capacity")));
                ps.setBigDecimal(4,
                    new java.math.BigDecimal(val(p, "monthly_fee")));
                ps.setInt(5, Integer.parseInt(val(p, "room_id")));

                if (ps.executeUpdate() == 0)
                    return "{\"success\":false,\"message\":\"Room not found or capacity is below occupancy\"}";
            }

            return success("Room updated successfully");
        }

        if (method.equals("DELETE")) {
            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(
                     "DELETE FROM Rooms WHERE room_id=?")) {

                ps.setInt(1, Integer.parseInt(val(p, "room_id")));

                if (ps.executeUpdate() == 0)
                    return "{\"success\":false,\"message\":\"Room not found\"}";
            }

            return success("Room deleted successfully");
        }

        return "{\"success\":false,\"message\":\"Invalid method\"}";
    }

    // 5. ROOM ALLOCATION
    private static String allocations(
            String method, Map<String, String> p)
            throws SQLException {

        if (method.equals("GET")) {
            String sql =
                "SELECT a.allocation_id, s.student_name, "
                + "s.roll_number, r.room_number, r.room_type, "
                + "a.allocation_date, a.allocation_status "
                + "FROM Room_Allocation a "
                + "JOIN Students s ON a.student_id=s.student_id "
                + "JOIN Rooms r ON a.room_id=r.room_id "
                + "ORDER BY a.allocation_id DESC";

            return "{\"success\":true,\"data\":" + getRows(sql) + "}";
        }

        if (method.equals("POST")) {
            int studentId = Integer.parseInt(val(p, "student_id"));
            int roomId = Integer.parseInt(val(p, "room_id"));

            try (Connection con = Database.getConnection()) {
                con.setAutoCommit(false);

                try {
                    String check =
                        "SELECT COUNT(*) FROM Room_Allocation "
                        + "WHERE student_id=? AND allocation_status='Active'";

                    try (PreparedStatement ps = con.prepareStatement(check)) {
                        ps.setInt(1, studentId);

                        try (ResultSet rs = ps.executeQuery()) {
                            rs.next();
                            if (rs.getInt(1) > 0)
                                throw new SQLException("Student already has an active room");
                        }
                    }

                    String update =
                        "UPDATE Rooms SET occupied=occupied+1, "
                        + "room_status=CASE WHEN occupied+1 >= capacity "
                        + "THEN 'Occupied' ELSE 'Available' END "
                        + "WHERE room_id=? AND occupied < capacity";

                    try (PreparedStatement ps = con.prepareStatement(update)) {
                        ps.setInt(1, roomId);

                        if (ps.executeUpdate() == 0)
                            throw new SQLException("Room is full or does not exist");
                    }

                    String insert =
                        "INSERT INTO Room_Allocation "
                        + "(student_id,room_id,allocation_date) "
                        + "VALUES (?,?,?)";

                    try (PreparedStatement ps = con.prepareStatement(insert)) {
                        ps.setInt(1, studentId);
                        ps.setInt(2, roomId);
                        ps.setDate(3, java.sql.Date.valueOf(val(p, "allocation_date")));
                        ps.executeUpdate();
                    }

                    con.commit();

                } catch (Exception e) {
                    con.rollback();
                    throw e;
                } finally {
                    con.setAutoCommit(true);
                }
            }

            return success("Room allocated successfully");
        }

        return "{\"success\":false,\"message\":\"Invalid method\"}";
    }

    // 6. FEE MANAGEMENT
    private static String fees(
            String method, Map<String, String> p)
            throws SQLException {

        if (method.equals("GET")) {
            String sql =
                "SELECT f.*, s.student_name, s.roll_number "
                + "FROM Fees f JOIN Students s "
                + "ON f.student_id=s.student_id "
                + "ORDER BY f.fee_id DESC";

            return "{\"success\":true,\"data\":" + getRows(sql) + "}";
        }

        if (method.equals("POST")) {
            String sql =
                "INSERT INTO Fees "
                + "(student_id,amount,payment_date,payment_status,payment_method) "
                + "VALUES (?,?,?,?,?)";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setInt(1, Integer.parseInt(val(p, "student_id")));
                ps.setBigDecimal(2,
                    new java.math.BigDecimal(val(p, "amount")));

                String date = val(p, "payment_date");

                if (date.isEmpty()) ps.setNull(3, Types.DATE);
                else ps.setDate(3, java.sql.Date.valueOf(date));

                ps.setString(4, val(p, "payment_status"));
                ps.setString(5, val(p, "payment_method"));

                ps.executeUpdate();
            }

            return success("Fee record added successfully");
        }

        if (method.equals("PUT")) {
            String sql =
                "UPDATE Fees SET amount=?, payment_date=?, "
                + "payment_status=?, payment_method=? WHERE fee_id=?";

            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(sql)) {

                ps.setBigDecimal(1,
                    new java.math.BigDecimal(val(p, "amount")));

                String date = val(p, "payment_date");

                if (date.isEmpty()) ps.setNull(2, Types.DATE);
                else ps.setDate(2, java.sql.Date.valueOf(date));

                ps.setString(3, val(p, "payment_status"));
                ps.setString(4, val(p, "payment_method"));
                ps.setInt(5, Integer.parseInt(val(p, "fee_id")));

                if (ps.executeUpdate() == 0)
                    return "{\"success\":false,\"message\":\"Fee record not found\"}";
            }

            return success("Fee record updated successfully");
        }

        if (method.equals("DELETE")) {
            try (Connection con = Database.getConnection();
                 PreparedStatement ps = con.prepareStatement(
                     "DELETE FROM Fees WHERE fee_id=?")) {

                ps.setInt(1, Integer.parseInt(val(p, "fee_id")));

                if (ps.executeUpdate() == 0)
                    return "{\"success\":false,\"message\":\"Fee record not found\"}";
            }

            return success("Fee record deleted successfully");
        }

        return "{\"success\":false,\"message\":\"Invalid method\"}";
    }
}
