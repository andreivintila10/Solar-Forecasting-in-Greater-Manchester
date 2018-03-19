<?php
  // Define connection parameters.
  define("DB_SERVER", "localhost");
  define("DB_USERNAME", "u667487650_vinti");
  define("DB_PASSWORD", "Vinti123!");
  define("DB_DATABASE", "u667487650_solar");

  // Create connection.
  $con = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE);
  if (mysqli_connect_errno())
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
?>