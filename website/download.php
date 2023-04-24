<?php
    session_start();

    include "top.php";
?>
        <main class="download">
            <h2>Game Downloads</h2>
            <section class="download-section windows">
                <h3>Windows Download (.exe)</h3>
                <button><a href="downloads/chesswithfriends.exe" download>Download</a></button>
            </section>

            <section class="download-section macos">
                <h3>MacOS Download</h3>
                <p>Downloading this file will give you a .zip file which you will need to unzip to play.</p>
                <button><a href="downloads/chesswithfriends.zip" download>Download</a></button>
            </section>

            <section class="download-section additional-info">
                <h3>Please Note:</h3>
                <p>Before you are able to play the game, you must register an account on the Chess With Friends website. You can do so <a href="register.php" class="text-link">here</a>.
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