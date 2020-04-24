<?php

    if (!filter_var($_POST["sendTo"], FILTER_VALIDATE_EMAIL)) {
        echo("Invalid email format");
        header("Location: https://samwat.ch/?error=1");
        die();
    }

    var_dump($_POST);
    echo("<hr>");

    $new_query = "INSERT INTO opportunityFilters (";
    $values = " VALUES(";

    $credentials = file('credentials.txt');
    $db_connection = pg_connect("host=$credentials[0] port=$credentials[1] dbname=$credentials[2] user=$credentials[3] password=$credentials[4]");

    $items = 0;
    foreach ($_POST as $key => $value) {
        $value = pg_escape_string($db_connection, $value);
        if (!empty($value) and $value != "e/" and $value != "c/") {
            $new_query .= "$key,";
            if ($key != "sendTo") {
                $values .= "'" . $_POST[$key . "Selection"] . "$value',";
            } else {
                $values .= "'$value'";
            }
            echo("$key is $value <br>");
            $items++;
        } elseif ($value = "e/" or $value = "c/") {
            continue;
        } else {
            echo("$key is not set<br>");
        }
    }
    echo("<hr>");

    if ($items < 2) {
        echo("No filters selected. Stopping.<hr>");
        header("Location: https://samwat.ch/?error=2");
        die();
    }

    $filled_query = substr($new_query, 0, -1) . ")" . $values . ");";
    echo($filled_query . "<hr>");

    $result = pg_query($db_connection, $filled_query);
    echo("Submitted");
    header("Location: https://samwat.ch/?error=0");