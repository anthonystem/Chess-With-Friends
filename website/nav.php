<nav class="navigation-bar">
    <div class="hamburger-button">
        <span></span>
        <span></span>
        <span></span>
    </div>
    <div class="hamburger-close-button">
        <span>&times;</span>
    </div>
    <section class="navigation-logo">
        <h1>Chess With Friends</h1>
    </section>
    <ul class="navigation-links">
        <?php
            if(isset($_SESSION) && isset($_SESSION["username"])) {
                print "<li><a href=\"dashboard.php\">Dashboard</a></li>".PHP_EOL;
                print "<li><a href=\"download.php\">Download</a></li>".PHP_EOL;
                print "<li><a href=\"search.php\">Find Players</a></li>".PHP_EOL;
                print "<li><a href=\"logout.php\">Log Out</a></li>".PHP_EOL;
            } else {
                print "<li><a href=\"index.php\">Home</a></li>".PHP_EOL;
                print "<li><a href=\"download.php\">Download</a></li>".PHP_EOL;
                print "<li><a href=\"login.php\">Login</a></li>".PHP_EOL;
                print "<li><a href=\"register.php\">Register</a></li>".PHP_EOL; 
            }
        ?>
    </ul>
</nav>