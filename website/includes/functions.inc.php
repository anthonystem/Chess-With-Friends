<?php
    function sanitize($data) {
        $data = trim($data);
        $data = stripslashes($data);
        $data = htmlspecialchars($data);

        return $data;
    }

    function validateUsernameInput($username) {
        $isValid = True;

        // Check that username is not less than 3 characters and that its not greater than 32 characters.
        if(strlen($username) < 3 || strlen($username) > 32) {
            $isValid = False;
        }

        return $isValid;
    }

    function validatePasswordInput($password) {
        $isValid = True;

        // Check it is not shorter than 6 characters.
        if(strlen($password) < 6) {
            $isValid = False;
        }

        return $isValid;
    }
?>