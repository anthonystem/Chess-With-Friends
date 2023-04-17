<?php
    session_start();

    include "top.php";

    // Check if user is logged in.
    if(session_id() == "" || !isset($_SESSION) || !isset($_SESSION["username"])) {
        header("Location: login.php");
    }


?>
        <main class="dashboard">
            <h1>Welcome, <?php print $_SESSION["username"]; ?>!</h1>
            <div class="dashboard-wrapper">
                <section class="dashboard-statistics">
                    <h2>Your Statistics</h2>
                    <p><strong>Wins:</strong></p>
                    <p><strong>Losses:</strong></p>
                    <p><strong>Stalemates:</strong></p>
                </section>
                <aside class="dashboard-history">
                    <h2>Past Games</h2>
                    <div class="games">
                        <?php
                            include "includes/db.inc.php";

                            $history = selectGameHistory($_SESSION["username"], $pdo);

                            foreach($history as $game) {
                                print '<section class="game-summary">';
                                print PHP_EOL;
                                print '<h3>'.$game["pfkChallenger"].' vs. '.$game["pfkAccepter"].'</h3>';
                                print PHP_EOL;
                                if($game["fldIsStalemate"] == 1) {
                                    print '<p style="color: blue">Stalemate</p>';
                                } else if($game["fnkWinner"] == $_SESSION["username"]) {
                                    print '<p style="color: green">Victory</p>';
                                } else {
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