<?php
    include "top.php";
?>
        <main class="login">
            <section class="login-section">
                <h2>Create an Account</h2>
                <form method="POST">
                    <p class="form-element">
                        <label for="txtNewUsername">Username</label>
                        <input type="text" name="txtNewUsername" minlength="3" placeholder="Type Your Username" required>
                    </p>
                    <p class="form-element">
                        <label for="txtNewEmail">Email</label>
                        <input type="email" name="txtNewEmail" minlength="6" placeholder="Type Your Email Address" required>
                    </p>
                    <p class="form-element">
                        <label for="txtNewPassword">Password</label>
                        <input type="password" name="txtNewPassword" minlength="6" placeholder="Type Your Password" required>
                    </p>
                    <p class="form-element">
                        <label for="txtNewPasswordConfirmation">Confirm Password</label>
                        <input type="password" name="txtNewPasswordConfirmation" minlength="6" placeholder="Type Your Password Again" required>
                    </p>
                    <p class="form-element">
                        <button type="submit">Create Account</button>
                    </p>
                </form>
                <?php
                    if($_SERVER["REQUEST_METHOD"] === "POST") {

                        $username = $_POST["txtNewUsername"];
                        $passwordHash = password_hash($_POST["txtNewPassword"], PASSWORD_DEFAULT);
                        $email = $_POST["txtNewEmail"];
                
                        include "includes/db.inc.php";
                
                        $sql = "INSERT INTO Users (username, password, email) ";
                        $sql .= "VALUES (?, ?, ?)";
                        $data = array($username, $passwordHash, $email);
                        $query = $pdo->prepare($sql);
                        $query->execute($data);
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