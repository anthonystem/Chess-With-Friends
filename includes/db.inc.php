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
        $sql .= "WHERE pfkPlayer1 = ? OR pfkPlayer2 = ?";
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

    function selectSearchUsers($string, $exclude, $pdo) {
        if(strlen($string) == 0) {
            return array();
        }
        
        $sql = "SELECT * FROM tblUsers ";
        $sql .= "WHERE pmkUsername LIKE \"".$string."%\" AND pmkUsername != ?";
        $data = array($exclude);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $results = $query->fetchAll(PDO::FETCH_ASSOC);

        return $results;
    }

    function insertFollow($follower, $followee, $pdo) {
        $sql = "INSERT INTO tblFollowers (pfkFollower, pfkFollowee) ";
        $sql .= "VALUES (?, ?)";
        $data = array($follower, $followee);

        $query = $pdo->prepare($sql);
        $query->execute($data);
    }

    function deleteFollow($follower, $followee, $pdo) {
        $sql = "DELETE FROM tblFollowers ";
        $sql .= "WHERE pfkFollower = ? AND pfkFollowee = ?";
        $data = array($follower, $followee);

        $query = $pdo->prepare($sql);
        $query->execute($data);
    }

    function follows($follower, $followee, $pdo) {
        $sql = "SELECT * FROM tblFollowers ";
        $sql .= "WHERE pfkFollower = ? AND pfkFollowee = ?";
        $data = array($follower, $followee);

        $query = $pdo->prepare($sql);
        $query->execute($data);

        $results = $query->fetchAll(PDO::FETCH_ASSOC);

        if(empty($results)) {
            return False;
        }

        return True;
    }
?>