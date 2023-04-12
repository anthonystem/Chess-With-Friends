<?php
    session_start();
    if(isset($_SESSION) && isset($_SESSION["username"])) {
        header("Location: dashboard.php");
    }
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
                        include "includes/db.inc.php";

                        $validInputs = True;
                        $DEBUG = False;

                        // Check username is valid.
                        if($validInputs && !validateUsernameInput($username)) {
                            $validInputs = False;
                            print "<p class=\"form-error\">Username is not a valid length. Must be between 6 and 32 characters in length.";
                        }

                        // Check if username already exists.
                        if($validInputs) {
                            $sql = "SELECT pmkUsername FROM tblUsers ";
                            $sql .= "WHERE pmkUsername = ?";
                            $data = array($username);
                            $query = $pdo->prepare($sql);
                            $query->execute($data);
                    
                            $results = $query->fetchAll(PDO::FETCH_ASSOC);

                            if(!empty($results)) {
                                $validInputs = False;
                                print "<p class=\"form-error\">The username ".$username." is already taken.</p>";
                            }
                        }

                        // Check password is valid.
                        if($validInputs && !validatePasswordInput($password)) {
                            $validInputs = False;
                            print "<p class=\"form-error\">Password is too short! Must be at least 6 characters in length.";
                        }

                        // Check password and password confirmation match.
                        if($validInputs && $password != $passwordConfirmation) {
                            $validInputs = False;
                            print "<p class=\"form-error\">Passwords do not match!</p>";
                        }

                        // Insert into Users table if valid inputs.
                        if($validInputs && $DEBUG == False) {
                            $passwordHash = password_hash($_POST["txtNewPassword"], PASSWORD_DEFAULT);
                    
                            $sql = "INSERT INTO tblUsers (pmkUsername, fldPassword) ";
                            $sql .= "VALUES (?, ?)";
                            $data = array($username, $passwordHash);
                            $query = $pdo->prepare($sql);
                            $query->execute($data);
                        }

                        // Redirect to dashboard if valid.
                        if($validInputs) {
                            header("Location: dashboard.php");
                        }
                    }
                ?>
                <div class="form-redirect">
                    <p>Already Have An Account? <a href="login.php">Login</a></p>
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