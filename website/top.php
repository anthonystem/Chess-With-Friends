<?php
    $path = pathinfo(htmlentities($_SERVER['PHP_SELF'], ENT_QUOTES, "UTF-8"))['filename'];
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Chess With Friends |
            <?php 
                if($path == "index") {
                    print " Home";
                } else if($path == "login") {
                    print " Login";
                } else if($path == "register") {
                    print " Register";
                } else if($path == "dashboard") {
                    print " Profile";
                } else if($path == "search") {
                    print " Player Search";
                } else if($path == "followers") {
                    print " Followers";
                } else if($path == "following") {
                    print " Following";
                } else if($path == "download") {
                    print " Download";
                } else if($path == "logout") {
                    print " Logout";
                }
            ?>
        </title>
        <link rel="stylesheet" href="css/styles.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.3.0/css/all.min.css" integrity="sha512-SzlrxWUlpfuzQ+pcUCosxcglQRNAq/DZjVsC0lE40xsADsfeQoEypE+enwcOiGjk/bSuGGKHEyjSoQ1zVisanQ==" crossorigin="anonymous" referrerpolicy="no-referrer">    
    </head>
    <body>

<?php
    include "nav.php";
?>