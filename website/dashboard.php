<?php
    session_start();

    include "top.php";

    // Check if user is logged in.
    if(session_id() == "" || !isset($_SESSION) || !isset($_SESSION["username"])) {
        header("Location: login.php");
        exit();
    }

    // Get username.
    $username;
    if(!isset($_GET["user"])) {
        $username = $_SESSION["username"];
    } else {
        $username = $_GET["user"];
    }
    
    include "includes/db.inc.php";
    $userData = selectUserData($username, $pdo);

    if(empty($userData)) {
        header("Location: dashboard.php");
        exit();
    }
    print PHP_EOL;
?>
        <main class="dashboard">
            <?php
                if($username != $_SESSION["username"]) {
                    print "<h1>".$username."'s Profile</h1>".PHP_EOL;
                } else {
                    print "<h1>Welcome, ".$username."!</h1>";
                }
            ?>
            <div class="dashboard-wrapper">
                <section class="dashboard-connections">
                <div class="information-wrapper">
                    <h3>Followers</h3>
                    <p><a href="followers.php?username=<?php print $username ?>"><?php print selectFollowerCount($username, $pdo); ?></a></p>
                </div>
                <div class="information-wrapper">
                    <h3>Following</h3>
                    <p><a href="following.php?username=<?php print $username ?>"><?php print selectFollowingCount($username, $pdo); ?></a></p>
                </div>
                </section>
                <section class="dashboard-statistics">
                    <?php 
                        if($username != $_SESSION["username"]) {
                            print "<h2>".$username."'s Statistics</h2>".PHP_EOL;
                        } else {
                            print "<h2>Your Statistics</h2>".PHP_EOL;
                        }

                        print "<p><strong>Wins: </strong>".$userData[0]["fldWins"]."</p>";
                        print "<p><strong>Losses: </strong>".$userData[0]["fldLosses"]."</p>";
                        print "<p><strong>Stalemates: </strong>".$userData[0]["fldStalemates"]."</p>";
                    ?>
                </section>
                <aside class="dashboard-history">
                    <h2>Past 5 Games</h2>
                    <div class="games">
                        <?php
                            $history = selectGameHistory($username, $pdo);

                            foreach($history as $game) {
                                print '<section class="game-summary">';
                                print PHP_EOL;
                                print '<h3>'.$game["pfkPlayer1"].' vs. '.$game["pfkPlayer2"].'</h3>';
                                print PHP_EOL;
                                if($game["fldIsStalemate"] == 1) {
                                    print '<p style="color: blue">Stalemate</p>';
                                } else if($game["fnkWinner"] == $username) {
                                    print '<p style="color: green">Victory</p>';
                                } else if($game["fnkWinner"] != $username) {
                                    print '<p style="color: red">Loss</p>';
                                }
                                print PHP_EOL;
                                print '</section>';
                                print PHP_EOL;
                            }
                        ?>
                    </div>
                </aside>
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
</html>