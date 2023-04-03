<footer class="page-footer">
    <section class="footer-section footer-logo">
        <h2>Chess With Friends</h2>
    </section>
    <section class="footer-section">
        <h2>Links</h2>
        <?php
        if(isset($_SESSION) && isset($_SESSION["username"])) {
                print "<p><a href=\"dashboard.php\">Dashboard</a></p>".PHP_EOL;
                print "<p><a href=\"download.php\">Download</a></p>".PHP_EOL;
                print "<p><a href=\"logout.php\">Log Out</a>".PHP_EOL;
            } else {
                print "<p><a href=\"index.php\">Home</a></p>".PHP_EOL;
                print "<p><a href=\"download.php\">Download</a></p>".PHP_EOL;
                print "<p><a href=\"login.php\">Login</a></p>".PHP_EOL;
                print "<p><a href=\"register.php\">Register</a></p>".PHP_EOL; 
            }
        ?>
    </section>
    <section class="footer-section">
        <h2>Authors</h2>
        <p>Anthony Stem</p>
    </section>
</footer>