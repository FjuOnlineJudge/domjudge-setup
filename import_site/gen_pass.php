<?php
  
function dj_password_hash(string $password) : string
{
    return password_hash(
        $password,
        PASSWORD_DEFAULT,
        array('cost' => 10)
    );
}

echo dj_password_hash($argv[1]);
?>