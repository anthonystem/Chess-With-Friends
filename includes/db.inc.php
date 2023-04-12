<?php
    define("DATABASE_NAME", "chesswithfriends");
    define("DSN", "mysql:host=chesswithfriends.cwqryofoppjg.us-east-2.rds.amazonaws.com;dbname=".DATABASE_NAME);
    define("DATABASE_USERNAME", "admin");
    define("DATABASE_PASSWORD", "password");
    
    try {
        $pdo = new PDO(DSN, DATABASE_USERNAME, DATABASE_PASSWORD);
    } catch(PDOException $error) {
        echo "### ERROR ### ".$error->getMessage();
    }

?>