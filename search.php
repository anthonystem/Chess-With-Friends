<?php
    session_start();

    include "top.php";

    // Check if user is logged in.
    if(session_id() == "" || !isset($_SESSION) || !isset($_SESSION["username"])) {
        header("Location: login.php");
        exit();
    }

    include "includes/db.inc.php";

    if(isset($_POST["txtFollow"])) {
        $toFollow = $_POST["txtFollow"];

        insertFollow($_SESSION["username"], $toFollow, $pdo);
    }
?>

        <main class="search">
            <div class="search-bar-wrapper">
                <form action="search.php" method="POST">
                    <p class="bar">
                        <label for="txtSearch"><i class="fa fa-magnifying-glass"></i></label>
                        <input type="text" name="txtSearch" placeholder="Search for user(s)...">
                    </p>
                    <p>
                        <button type="submit">Search</button>
                    </p>
                </form>
            </div>
            <section class="search-results"> 
                <?php
                    if(isset($_POST["txtSearch"])) {
                        $query = $_POST["txtSearch"];
                        $results = selectSearchUsers($query, $_SESSION["username"], $pdo);
                        $searchQuery = $_POST["txtSearch"];
                        $results = selectSearchUsers($searchQuery, $_SESSION["username"], $pdo);
                        print "<h2>Search Results</h2>";

                        if(empty($results)) {
                            print "<p>No results found.</p>";
                        } else {
                            print "<div class=\"grid-layout\">".PHP_EOL;
                            foreach($results as $user) {
                                print "<section class=\"search-result\">".PHP_EOL;
                                print "<h3>".$user["pmkUsername"]."</h3>".PHP_EOL;
                                print "<form action=\"\" method=\"POST\">".PHP_EOL;
                                print "<input type=\"text\" value=\"".$_POST["txtSearch"]."\" name=\"txtSearch\" hidden>".PHP_EOL;
                                if(!follows($_SESSION["username"], $user["pmkUsername"], $pdo)) {
                                    print "<input type=\"text\" value=\"".$user["pmkUsername"]."\"  name=\"txtFollow\" hidden>".PHP_EOL;
                                    print "<button type=\"submit\">Follow</button>".PHP_EOL;
                                } else {
                                    print "<input type=\"text\" value=\"".$user["pmkUsername"]."\"  name=\"txtUnfollow\" hidden>".PHP_EOL;
                                    print "<button type=\"submit\">Unfollow</button>".PHP_EOL;
                                }

                                print "<a href=\"dashboard.php?user=".$user["pmkUsername"]."\">View Profile</a>".PHP_EOL;
                                print "</form>".PHP_EOL;
                                print "</section>".PHP_EOL;
                            }
                            print "</div>".PHP_EOL;
                        }
        

                    }
                ?>
            </section>
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