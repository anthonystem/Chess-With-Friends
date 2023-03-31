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

                        $username = isset($_POST["txtNewUsername"]) ? $_POST["txtNewUsername"] : 0;
                        $password = isset($_POST["txtNewPassword"]) ? $_POST["txtNewPassword"] : 0;
                        $passwordConfirmation = isset($_POST["txtNewPasswordConfirmation"]) ? $_POST["txtNewPasswordConfirmation"] : "";

                        include "includes/functions.inc.php";

                        $validInputs = True;
                        $DEBUG = True;

                        // Check username is valid.
                        if($validInputs && !validateUsernameInput($username)) {
                            $validInputs = False;
                            print "<p>Username is not a valid length. Must be between 6 and 32 characters in length.";
                        }


                        // Check password is valid.
                        if($validInputs && !validatePasswordInput($password)) {
                            $validInputs = False;
                            print "<p>Password is too short! Must be at least 6 characters in length.";
                        }

                        // Check password and password confirmation match.
                        if(validInputs && $password != $passwordConfirmation) {
                            $validInputs = False;
                            print "<p>Passwords do not match!</p>";
                        }

                        // Insert into Users table if valid inputs.
                        if($validInputs && $DEBUG == False) {
                            $passwordHash = password_hash($_POST["txtNewPassword"], PASSWORD_DEFAULT);
                            $email = $_POST["txtNewEmail"];
                    
                            include "includes/db.inc.php";
                    
                            $sql = "INSERT INTO Users (username, password, email) ";
                            $sql .= "VALUES (?, ?, ?)";
                            $data = array($username, $passwordHash, $email);
                            $query = $pdo->prepare($sql);
                            $query->execute($data);
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