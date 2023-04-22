<?php
    include "top.php";
?>

        <main class="landing">
            <div class="hero-banner">
                <section class="hero-content">
                    <h2>Chess With Friends</h2>
                    <p><span class="emphasize">Connect</span> with your friends. <span class="emphasize">Play</span> chess. <span class="emphasize">Win</span>.</p>
                    <nav class="cta-nav">
                        <p><a href="register.php" class="cta">Register &amp; Play</a></p>
                        <p><a href="#about" class="cta secondary-cta">Learn More</a></p>
                    </nav>
                </section>
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