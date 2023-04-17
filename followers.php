<?php
    session_start();

    include "top.php";

    // Check if user is logged in.
    if(session_id() == "" || !isset($_SESSION) || !isset($_SESSION["username"])) {
        header("Location: login.php");
        exit();
    }

    include "includes/db.inc.php";
    // Check if username is set.
    if(!isset($_GET["username"])) {
        header("Location: dashboard.php");
        exit();
    }

    $username = $_GET["username"];
    $userData = selectUserData($_SESSION["username"], $pdo);
?>

        <main class="followers">
            <?php 
                if(empty($userData)) {
                    print "<h2>Sorry, but it appears that the user ".$username." does not exist.</h2>";
                } else {
                    print "<h2>".$username."'s Followers</h2>";
                }
                print PHP_EOL;

                $followers = selectFollowers($username, $pdo);  
                if(empty($followers)) {
                    print "<p>This user does not have any followers.</p>";
                } else {
                    foreach($followers as $follower) {
                        print "<section class=\"follower-entry\">".PHP_EOL;
                        print "<h3>".$follower["pfkFollower"]."</h3>".PHP_EOL;
                        print "</section>".PHP_EOL;
                    }
                }
            ?>
        </main>

        <?php
            include "footer.php";
        ?>

        <script type="text/javascript">

            // Handle Navigation Hamburger Button.
            const hamburgerButton = document.querySelector(".hamburger-button");
            const hamburgerCloseButton = document.querySelector(".hamburger-close-button");
            const navigationLinks = document.querySelector(".navigation-links");

            hamburgerButton.addEventListener('click', () => {
                navigationLinks.classList.toggle("show");
                hamburgerCloseButton.classList.toggle("show");
            });

            hamburgerCloseButton.addEventListener('click', () => {
                navigationLinks.classList.toggle("show");
                hamburgerCloseButton.classList.toggle("show");
            });
        </script>
    </body>
</html>