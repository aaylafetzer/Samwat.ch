<?php
    if (!isset($_GET["email"])) {
        echo("No key provided. Please use the link in the email you received to unsubscribe.");
        die();
    }
?>

<html>
<head>
    <title>Samwat.ch - Unsubscribe</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.8.0/css/bulma.min.css" integrity="sha256-D9M5yrVDqFlla7nlELDaYZIpXfFWDytQtiV+TaH6F1I=" crossorigin="anonymous" />
</head>
<body>
    <div class="section">
        <h1 class="title">Unsubscribe</h1>
        <h1 class="subtitle">Filters Being Sent To <?php echo($_GET["email"])?></h1>
        <p>Please select any filters you would like to remove.</p>
        <hr>
        <div class="columns">
            <div class="column is-one-half">
        <form action="confirmOpportunityUnsubscribe.php" method="post">
        <?php
        $credentials = file('credentials.txt');
        $db_connection = pg_connect("host=$credentials[0] port=$credentials[1] dbname=$credentials[2] user=$credentials[3] password=$credentials[4]");

        $OpportunityResult = pg_query($db_connection, "SELECT * FROM opportunityFilters WHERE LOWER(sendto) = LOWER('" . pg_escape_string($db_connection, $_GET["email"]) . "');");
        $senateDisclosureResult = pg_query($db_connection, "SELECT * FROM senateDisclosureFilters WHERE LOWER(sendto) = LOWER('" . pg_escape_string($db_connection, $_GET["email"]) . "');");

        $OpportunityResult = pg_fetch_all($OpportunityResult);
        $senateDisclosureResult = pg_fetch_all($senateDisclosureResult);

        if (empty($OpportunityResult)) {
            echo("There are no Federal Contract Opportunities associated with this address");
        } else {
            foreach ($OpportunityResult as $filter) {
                $id = $filter["id"];
                $text = "Federal Contract Opportunities where ";
                foreach ($filter as $key => $value) {
                    if (!is_null($value)) {
                        if ($key == "id" or $key == "sendto") {
                            continue;
                        } else {
                            $text .= $key;
                            if (substr($value, 0, 2) == "e/") {
                                $text .= " is ";
                            } elseif (substr($value, 0, 2) == "c/") {
                                $text .= " contains ";
                            } else {
                                $text = "An Error Occurred While Processing This Result";
                            }
                        }
                        $text .= substr($value, 2) . "; ";
                    }
                }
                echo("<br><label class='checkbox'><input type='checkbox' name='$id' class='unsubBox'>$text</label><br>");
    //            echo("<label class=\"checkbox\"><input type=\"checkbox\">$value</label>");
            }
        }
        ?>
            <br>
            <div class="control">
                <button class="button is-link">Submit</button>
            </div>
        </form>
            </div>
            <div class="column is-one-half">
            <form action="confirmSenateDisclosureUnsubscribe.php" method="post">
            <?php
        if (empty($senateDisclosureResult)) {
            echo("There are no Senate Financial Disclosures associated with this address");
        } else {
            foreach($senateDisclosureResult as $filter) {
                    $id = $filter["id"];
                    $text = "Senate Financial Disclosures where ";
                    foreach ($filter as $key => $value) {
                        if (!is_null($value)) {
                            if ($key == "id" or $key == "sendto") {
                                continue;
                            } else {
                                $text .= $key;
                                if (substr($value, 0, 2) == "e/") {
                                    $text .= " is ";
                                } elseif (substr($value, 0, 2) == "c/") {
                                    $text .= " contains ";
                                } else {
                                    $text = "An Error Occurred While Processing This Result";
                                }
                            }
                            $text .= substr($value, 2) . "; ";
                        }
                    }
                    echo("<br><label class='checkbox'><input type='checkbox' name='$id' class='unsubBox'>$text</label><br>");
                    //            echo("<label class=\"checkbox\"><input type=\"checkbox\">$value</label>");
                }
        }
        ?>
            <br>
                <div class="control">
                    <button class="button is-link">Submit</button>
                </div>
        </form>
            </div>
        </div>
    </div>
</body>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
</html>
