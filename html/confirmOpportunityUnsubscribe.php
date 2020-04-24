<?php
$credentials = file('credentials.txt');
$db_connection = pg_connect("host=$credentials[0] port=$credentials[1] dbname=$credentials[2] user=$credentials[3] password=$credentials[4]");
foreach ($_POST as $id => $value) {
    pg_query(
        $db_connection, "DELETE FROM opportunityFilters WHERE id = $id;"
    );
}
echo("Unsubscribe complete. You can now close this page.");
header("Location: https://samwat.ch/?error=3");