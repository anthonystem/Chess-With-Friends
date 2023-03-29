<?php
    include "top.php";
?>
        <main class="login">
            <section class="login-section">
                <h2>Login</h2>
                <form method="POST">
                    <p class="form-element">
                        <label for="txtUsername">Username</label>
                        <input type="text" name="txtUsername" minlength="3" placeholder="Type Your Username" required>
                    </p>
                    <p class="form-element">
                        <label for="txtPassword">Password</label>
                        <input type="password" name="txtPassword" minlength="6" placeholder="Type Your Password" required>
                    </p>
                    <p class="form-element">
                        <button type="submit">Log In</button>
                    </p>
                </form>
                <?php
                    if($_SERVER["REQUEST_METHOD"] === "POST") {

                        $username = $_POST["txtUsername"];
                        $password = $_POST["txtPassword"];
                
                        include "includes/db.inc.php";
                
                        $sql = "SELECT password FROM Users ";
                        $sql .= "WHERE username = ?";
                        $data = array($username);
                        $query = $pdo->prepare($sql);
                        $query->execute($data);
                
                        $results = $query->fetchAll(PDO::FETCH_ASSOC);
                
                        // Check if username exists.
                        if(!empty($results)) {
                            // Verify password is correct.
                            if(password_verify($password, $results[0]["password"])) {
                                print "<p>Log in success</p>";
                            } else {
                                print "<p>Log in fail (wrong pass)</p>";
                            }
                        } else {
                            print "<p>Log in fail (no user)</p>";
                        }
                    }
                ?>
                <div class="login-signup">
                    <p><a href="#">Don't Have An Account?</a></p>
                </div>
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