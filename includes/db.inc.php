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

    function selectFollowerCount($username, $pdo) {
        $sql = "SELECT count(*) as 'Count' FROM tblFollowers ";
        $sql .= "WHERE pfkFollowee = ?";
        $data = array($username);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $count = $query->fetchAll(PDO::FETCH_ASSOC);
        
        return $count[0]["Count"];
    }

    function selectFollowers($username, $pdo) {
        $sql = "SELECT pfkFollower FROM tblFollowers ";
        $sql .= "WHERE pfkFollowee = ?";
        $data = array($username);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $results = $query->fetchAll(PDO::FETCH_ASSOC);
        
        return $results;
    }

    function selectFollowingCount($username, $pdo) {
        $sql = "SELECT count(*) as 'Count' FROM tblFollowers ";
        $sql .= "WHERE pfkFollower = ?";
        $data = array($username);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $count = $query->fetchAll(PDO::FETCH_ASSOC);

        return $count[0]["Count"];
    }

    function selectFollowing($username, $pdo) {
        $sql = "SELECT pfkFollowee FROM tblFollowers ";
        $sql .= "WHERE pfkFollower = ?";
        $data = array($username);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $results = $query->fetchAll(PDO::FETCH_ASSOC);
        
        return $results;
    }

    function selectSearchUsers($string, $pdo) {
        $sql = "SELECT * FROM tblUsers ";
        $sql .= "WHERE pmkUsername LIKE \"".$string."%\"";

        $query = $pdo->prepare($sql);
        $query->execute();

        $results = $query->fetchAll(PDO::FETCH_ASSOC);

        return $results;
    }
?>