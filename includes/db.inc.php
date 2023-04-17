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

    // Database functions
    function selectGameHistory($username, $pdo) {
        $sql = "SELECT * FROM tblGames ";
        $sql .= "WHERE pfkChallenger = ? OR pfkAccepter = ?";
        $data = array($username, $username);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $results = $query->fetchAll(PDO::FETCH_ASSOC);

        return $results;
    }

    function selectUserData($username, $pdo) {
        $sql = "SELECT * FROM tblUsers ";
        $sql .= "WHERE pmkUsername = ?";
        $data = array($username);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $results = $query->fetchAll(PDO::FETCH_ASSOC);

        return $results;
    }

?>