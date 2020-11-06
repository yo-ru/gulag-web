<?php
// Config
$config = include("config.php");

// Global Database Object
$db = new mysqli($config->host, $config->username, $config->password, $config->database);

// Handle connection failure.
if ($db->connect_error) {
    printf("MySQL connection failed: %s\n", $db->connect_error);
    exit();
}
?>