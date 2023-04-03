<?php
    define("DATABASE_NAME", "ASTEM_cs205_cwf_testdb");
    define("DSN", "mysql:host=webdb.uvm.edu;dbname=".DATABASE_NAME);
    define("DATABASE_USERNAME", "astem_writer");
    define("DATABASE_PASSWORD", "W0rBs3QwhJ5K");
    
    try {
        $pdo = new PDO(DSN, DATABASE_USERNAME, DATABASE_PASSWORD);
    } catch(PDOException $error) {
        echo "### ERROR ### ".$error->getMessage();
    }

?>