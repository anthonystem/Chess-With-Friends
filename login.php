<?php
    session_start();
    if(isset($_SESSION) && isset($_SESSION["username"])) {
        header("Location: dashboard.php");
    }

    include "top.php";
?>
        <main class="login">
            <section class="login-section">
                <h2>Login</h2>
                <form method="POST">
                    <p class="form-element">
                        <label for="txtUsername">Username</label>
                        <input type="text" name="txtUsername" placeholder="Type Your Username" required>
                    </p>
                    <p class="form-element">
                        <label for="txtPassword">Password</label>
                        <input type="password" name="txtPassword" placeholder="Type Your Password" required>
                    </p>
                    <p class="form-element">
                        <button type="submit">Log In</button>
                    </p>
                </form>
                <?php
                    if($_SERVER["REQUEST_METHOD"] === "POST") {

                        include "includes/functions.inc.php";


                        $username = sanitize($_POST["txtUsername"]);
                        $password = $_POST["txtPassword"];

                        include "includes/db.inc.php";
            
                        $sql = "SELECT fldPassword FROM tblUsers ";
                        $sql .= "WHERE pmkUsername = ?";
                        $data = array($username);
                        $query = $pdo->prepare($sql);
                        $query->execute($data);
                
                        $results = $query->fetchAll(PDO::FETCH_ASSOC);
                
                        // Check if username exists.
                        if(!empty($results)) {
                            // Verify password is correct.
                            if(password_verify($password, $results[0]["fldPassword"])) {
                                // Success: Redirect user to dashboard.php and store username in session variable.
                                $_SESSION["username"] = $username;
                                header("Location: dashboard.php");
                                exit();
                            } else {
                                print "<p class=\"form-error\">Incorrect username or password.</p>";
                            }
                        } else {
                            print "<p class=\"form-error\">Incorrect username or password.</p>";
                        }
                    }
                        
                ?>
                <div class="form-redirect">
                    <p>Don't Have An Account? <a href="register.php">Register.</a></p>
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