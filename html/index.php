<html>
    <head>
        <title>Samwat.ch</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.8.0/css/bulma.min.css" integrity="sha256-D9M5yrVDqFlla7nlELDaYZIpXfFWDytQtiV+TaH6F1I=" crossorigin="anonymous" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css" integrity="sha256-mmgLkCYLUQbXn0B1SRqzHar6dCnv9oZFPEC1g1cwlkk=" crossorigin="anonymous" />
        <style>
            ul#item li {
                display:inline;
            }
        </style>
    </head>
    <body>
    <nav class="navbar is-transparent">
        <div class="navbar-brand">
            <div class="navbar-burger burger" data-target="navbarExampleTransparentExample">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>

        <div id="navbarExampleTransparentExample" class="navbar-menu">
            <div class="navbar-start">
                <a class="navbar-item" href="https://samwat.ch">
                    Home
                </a>
                <a class="navbar-item" href="https://paypal.me/aaylafetzer">
                    Donate
                </a>
                <a class="navbar-item" href="https://samwat.ch/faq.php">
                    FAQ
                </a>
            </div>
        </div>
    </nav>
    <div class="section">
        <div class="has-text-centered">
            <div class="notification is-success" id="error-0" hidden>
                Your alert was successfully added.
            </div>
            <div class="notification is-danger" id="error-1" hidden>
                Your alert could not be added because the provided email was not a valid format. Please check your spelling and try again.
            </div>
            <div class="notification is-danger" id="error-2" hidden>
                Your alert could not be added because you did not enter any parameters to filter by. Please add some parameters and try again.
            </div>
            <div class="notification is-success" id="error-3" hidden>
                You have been successfully unsubscribed.
            </div>
        <img src="https://s3.fr-par.scw.cloud/static.samwat.ch/branding/Logo.png" alt="Samwath.ch Logo">
        <h1 class="title is-1">Welcome to Samwat.ch!</h1>
            <div class="content">
                <p>Samwat.ch is a free service designed to make it easier for journalists to follow and search US Government data.</p>
                <hr>
                <p>Currently Serving
                <?php
                    $credentials = file('credentials.txt');
                    $db_connection = pg_connect("host=$credentials[0] port=$credentials[1] dbname=$credentials[2] user=$credentials[3] password=$credentials[4]");
                    $result = pg_query($db_connection, "SELECT COUNT(id) FROM filters;");
                    echo(number_format(pg_fetch_result($result, 0)));
                ?> Filters To
                    <?php
                    $result = pg_query($db_connection, "SELECT COUNT(DISTINCT sendto) FROM filters;");
                    echo(number_format(pg_fetch_result($result, 0)));
                    ?>
                Email Addresses</p>
                <hr>
                <h1 class="title is-2">
                    Add your own alert
                </h1>
            </div>
        </div>
        <div class="container">
        <div id="tabs" class="tabs is-boxed">
            <ul>
                <li class="_tabButton is-active" id="OpportunityTabButton"><a onclick="tabClick('OpportunityTab')"><span class="icon is-small"><i class="far fa-file-alt" aria-hidden="true"></i></span>Federal Contract Opportunities</a></li>
                <li class="_tabButton" id="SenateDisclosureTabButton"><a onclick="tabClick('SenateDisclosureTab')"><span class="icon is-small"><i class="fas fa-search-dollar" aria-hidden="true"></i></span>Senate Financial Disclosures</a></li>
            </ul>
            </div>
    <div id="OpportunityTab" class="_tab">
        <form action="registerOpportunity.php" method="post">
            <p>At least one filter is required.</p>
            <div class="container has-text-centered">
                <h2 class="subtitle is-3">Contracting Agency</h2>
                <br>
            </div>
            <div class="columns">
                <div class="column is-one-third">
                    <h3 class="subtitle is-4">Department</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="departmentSelection">
                                    <option value="e/">Is</option>
                                    <option value="c/">Contains</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" name="department" type="text" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <h3 class="subtitle is-4">Subtier</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="subtierSelection">
                                    <option value="e/">Is</option>
                                    <option value="c/">Contains</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" name="subtier" type="text" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <h3 class="subtitle is-4">Office</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="officeSelection">
                                    <option value="e/">Is</option>
                                    <option value="c/">Contains</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" type="text" name="office" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container has-text-centered">
                <hr>
                <h2 class="subtitle is-3">Award Details</h2>
                <br>
            </div>
            <div class="columns">
                <div class="column is-one-half">
                    <h3 class="subtitle is-4">Title</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="titleSelection">
                                    <option value="e/">Is</option>
                                    <option value="c/">Contains</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" name="title" type="text" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-one-half">
                    <h3 class="subtitle is-4">Solicitation Number</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="solicitationNumberSelection">
                                    <option value="e/">Is</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" type="text" name="soliciationNumber" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="container has-text-centered">
                <hr>
                <h2 class="subtitle is-3">Industry Details</h2>
                <br>
            </div>
            <div class="columns">
                <div class="column is-one-half">
                    <h3 class="subtitle is-4">NAICS Code</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="naicsCodeSelection">
                                    <option value="e/">Is</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" type="text" name="naicsCode" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-one-half">
                    <h3 class="subtitle is-4">Product Service Code</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="productServiceCodeSelection">
                                    <option value="e/">Is</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" type="text" name="productServiceCode" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label">Email</label>
                <div class="control has-icons-left has-icons-right">
                    <input class="input is-danger" type="email" name="sendTo" placeholder="Your email address" id="email">
                    <span class="icon is-small is-left">
      <i class="fas fa-envelope"></i>
    </span>
                </div>
            </div>
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link" type="submit" id="submitButton">Submit</button>
                </div>
            </div>
        </form>
    </div>
    <div id="SenateDisclosureTab" class="_tab">
        <form action="registerSenateDisclosure.php" method="post">
            <p>No filters are required. If desired, you can just put in your email.</p><br>
            <div class="columns">
                <div class="column is-one-third">
                    <h3 class="subtitle is-4">Senator</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="senatorSelection">
                                    <option value="e/">Is</option>
                                    <option value="c/">Contains</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" name="senator" type="text" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <h3 class="subtitle is-4">Ticker</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="tickerSelection">
                                    <option value="e/">Is</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" name="ticker" type="text" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <h3 class="subtitle is-4">Asset Type</h3>
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="asset_typeSelection">
                                    <option value="e/">Is</option>
                                    <option value="c/">Contains</option>
                                </select>
                            </div>
                        </div>
                        <br>
                        <div class="field">
                            <div class="control">
                                <input class="input" name="asset_type" type="text" placeholder="Text input">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field">
                <label class="label">Email</label>
                <div class="control has-icons-left has-icons-right">
                    <input class="input is-danger" type="email" name="sendTo" placeholder="Your email address" id="email">
                    <span class="icon is-small is-left">
                            <i class="fas fa-envelope"></i>
                        </span>
                </div>
            </div>
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link" type="submit" id="submitButton">Submit</button>
                </div>
            </div>
        </form>
    </div>
    </div>
    </div>
    <footer class="footer">
        <div class="content has-text-centered">
            <p>Built by Aayla Fetzer. Source code available on <a href="https://gitlab.com/apozho/samwat.ch">Gitlab</a>.</p>
        </div>
    </footer>
    </body>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/js/all.min.js" integrity="sha256-MAgcygDRahs+F/Nk5Vz387whB4kSK9NXlDN3w58LLq0=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script>
    document.addEventListener('DOMContentLoaded', () => {

        // Get all "navbar-burger" elements
        const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

        // Check if there are any navbar burgers
        if ($navbarBurgers.length > 0) {

            // Add a click event on each of them
            $navbarBurgers.forEach( el => {
                el.addEventListener('click', () => {

                    // Get the target from the "data-target" attribute
                    const target = el.dataset.target;
                    const $target = document.getElementById(target);

                    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                    el.classList.toggle('is-active');
                    $target.classList.toggle('is-active');

                });
            });
        }

    });
</script>
<script>
    function tabClick(tabId) {
        let x = document.getElementsByClassName("_tab");
        $(x).hide();
        let y = document.getElementsByClassName("_tabButton");
        $(y).removeClass("is-active");
        let tab = document.getElementById(tabId);
        let tabButton = document.getElementById(tabId + "Button");
        $(tab).show();
        $(tabButton).addClass("is-active");
    }
    tabClick("OpportunityTab");
</script>
<script>
    let searchParams = new URLSearchParams(window.location.search);
    if (searchParams.has('error')) {
        let errorCode = searchParams.get('error');
        $(document.getElementById("error-" + errorCode)).show();
    }
</script>
</html>