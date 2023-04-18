<?php
    session_start();

    include "top.php";

    // Check if user is logged in.
    if(session_id() == "" || !isset($_SESSION) || !isset($_SESSION["username"])) {
        header("Location: login.php");
        exit();
    }

    include "includes/db.inc.php";
?>

        <main class="search">
            <div class="search-bar-wrapper">
                <form action="search.php" method="POST">
                    <p>
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
                        print "<h2>Search Results</h2>";

                        if(empty($results)) {
                            print "<p>No results found.</p>";
                        } else {
                            foreach($results as $user) {
                                print "<p>".$user["pmkUsername"]."</p>";
                            }
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