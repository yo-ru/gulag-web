<?php
// Config
$config = include("config.php");

// Database
include "assets/database/database.php";

class Account {
    // User ID
    private $id;

    // Username
    private $username;

    // Username Safe
    private $username_safe;

    // Email
    private $email;

    // Privileges
    private $privileges;

    // Authenticated
    private $authenticated;


    // Constructor
    public function __construct() {
        $this->id = NULL;
        $this->username = NULL;
        $this->email = NULL;
        $this->privileges = NULL;
        $this->authenticated = FALSE;
    }

    // Is Authenticated
    public function isAuthenticated(): bool {
        return $this->authenticated;
    }

    // Get Username
    public function getUsername(): string {
        return $this->username;
    }

    // Get Email
    public function getEmail(): string {
        return $this->email;
    }

    // Get Privileges
    public function getPrivileges(): int {
        return $this->privileges;
    }

    // Get ID 
    public function getID(): int {
        return $this->id;
    }

    // Create Account
    public function createAccount(string $username, string $email, string $password) {
        // Config
        global $config;

        // Database
        global $db;

        // Username must be 2-15 characters in length.
        if (strlen($username) < 2 || strlen($username) > 15) {
            throw new Exception("Username must be 2-15 characters in length.");
        }

        // Username may contain "_" and " ", but not both.
        if ((strpos($username, "_") !== false) && (strpos($username, " ") !== false)) {
            throw new Exception("Username may contain \"_\" and \" \", but not both.");
        }

        // Disallowed username; pick another.
        if (in_array($username, $config->disallowedNames)) {
            throw new Exception("Disallowed username; pick another.");
        }

        // Username already taken by another player.
        $query = $db->query("SELECT 1 FROM users WHERE name = \"" . $db->real_escape_string($username) . "\"");
        if ($query->num_rows > 0) {
            throw new Exception("Username already taken by another player.");
        }
        unset($query);

        // Invalid email syntax.
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new Exception("Invalid email syntax.");
        }

        // Email already taken by another player.
        $query = $db->query("SELECT 1 FROM users WHERE email = \"" . $db->real_escape_string($email) . "\"");
        if ($query->num_rows > 0) {
            throw new Exception("Email already taken by another player.");
        }
        unset($query);

        // Password must be 8-32 characters in length.
        if (strlen($password) < 8 || strlen($password) > 32) {
            throw new Exception("Password must be 8-32 characters in length.");
        }

        // Password was deemed too simple.
        if (in_array($password, $config->disallowedPasswords)) {
            throw new Exception("Password was deemed too simple.");
        }
        
        // Hash password.
        $hash = password_hash($password, PASSWORD_DEFAULT);

        // Make username safe.
        $username_safe = strtolower(str_replace(" ", "_ ", $username));

        // Insert into users table.
        $db->query("INSERT INTO users (name, name_safe, email, pw_hash, creation_time) VALUES (\"" . $db->real_escape_string($username) . "\", \"" . $db->real_escape_string($username_safe) . "\", \"" . $db->real_escape_string($email) . "\", \"" . $hash . "\", NOW())");
        unset($query);

        // Insert into stats table.
        $id = $db->insert_id;
        $db->query("INSERT INTO stats (id) VALUES (" . $id . ")");
        unset($query);

        // After successful registration, relocate to login page.
        header("Location: /login.php");
    }

    // Login
    public function login(string $username, string $password) {
        // Database
        global $db;

        // Check if user exists and attempt to verify password.
        $query = $db->query("SELECT * FROM users WHERE name = \"" . $db->real_escape_string($username) . "\"");
        if ($query->num_rows > 0) {
            // Authentication OK.
            $row = $query->fetch_assoc();
            if (password_verify($password, $row["pw_hash"])) {
                $this->id = $row["id"];
                $this->username = $row["name"];
                $this->username_safe = $row["name_safe"];
                $this->email = $row["email"];
                $this->privileges = $row["priv"];
                $this->authenticated = TRUE;
                $this->registerSession();

                // After successful login, relocate to home page.
                header("Location: /");
            }
            unset($row);
            throw new Exception("The password you entered was incorrect.");
        }
        unset($query);
        throw new Exception("We could not find an account with that username.");
    }

    // Register Session
    public function registerSession() {
        // Database
        global $db;

        // Register session in database.
        if (session_status() === PHP_SESSION_ACTIVE) {
            $db->query("REPLACE INTO user_sessions (session_id, user_id, login_time) VALUES (\"" . session_id() . "\", " . $this->id . ", NOW())");
        }
    }

    public function sessionLogin() {
        // Database
        global $db;

        // Check that the Session has been started.
        if (session_status() === PHP_SESSION_ACTIVE) {
            $query = $db->query("SELECT * FROM users, user_sessions WHERE (user_sessions.session_id = \"" . session_id() . "\") AND (user_sessions.login_time >= (NOW() - INTERVAL 7 DAY)) AND (user_sessions.user_id = users.id)");
            if ($query->num_rows > 0) {
                // Authentication OK.
                $row = $query->fetch_assoc();
                $this->id = $row["id"];
                $this->username = $row["name"];
                $this->username_safe = $row["name_safe"];
                $this->email = $row["email"];
                $this->privileges = $row["priv"];
                $this->authenticated = TRUE;
                unset($row);
            }
            unset($query);   
        }
    }

    public function logout() {
        // Database
        global $db;	
        
        // No ID; No user logged in; Do nothing.
        if (is_null($this->id)) {
            return;
        }
        
        // RESET account properties.
        $this->id = NULL;
        $this->username = NULL;
        $this->username_safe = NULL;
        $this->email = NULL;
        $this->privileges = NULL;
        $this->authenticated = FALSE;
        
        // If there is an open session remove it from the user_sessions table.
        if (session_status() === PHP_SESSION_ACTIVE)
        {
            $db->query("DELETE FROM user_sessions WHERE session_id = \"" . session_id() . "\"");
        }

        // After successful logout, relocate to login page.
        header("Location: /login.php");
    }
}

// Global Account
$account = new Account();
?>