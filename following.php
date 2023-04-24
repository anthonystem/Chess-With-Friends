<?php
    session_start();

    include "top.php";

    // Check if user is logged in.
    if(session_id() == "" || !isset($_SESSION) || !isset($_SESSION["username"])) {
        header("Location: login.php");
        exit();
    }

    include "includes/db.inc.php";

    if(isset($_POST["txtUnfollow"])) {
        $toUnfollow = $_POST["txtUnfollow"];

        deleteFollow($_SESSION["username"], $toUnfollow, $pdo);
    }

    $username = $_GET["username"];
    $userData = selectUserData($_SESSION["username"], $pdo);
?>

        <main class="following">
            
            <?php 
                if(empty($userData)) {
                    print "<h2>Sorry, but it appears that the user ".$username." does not exist.</h2>";
                } else {
                    print "<h2>".$username."'s Following</h2>";
                }
                print PHP_EOL;

                print "<div class=\"follower-wrapper\">";
                $following = selectFollowing($username, $pdo);  
                if(empty($following)) {
                    print "<p>This user is not following anyone.</p>";
                } else {
                    foreach($following as $follower) {
                        print "<section class=\"follower-entry\">".PHP_EOL;
                        print "<h3><a href=\"dashboard.php?user=".$follower["pfkFollowee"]."\">".$follower["pfkFollowee"]."</a></h3>".PHP_EOL;
                        if($_SESSION["username"] == $username) {
                            print "<form action=\"\" method=\"POST\">".PHP_EOL;
                            print "<input type=\"text\" value=\"".$follower["pfkFollowee"]."\"  name=\"txtUnfollow\" hidden>".PHP_EOL;
                            print "<button type=\"submit\">Unfollow</button>".PHP_EOL;
                            print "</form>".PHP_EOL;
                        }
                        print "</section>".PHP_EOL;
                    }
                }
            ?>
            </div>
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