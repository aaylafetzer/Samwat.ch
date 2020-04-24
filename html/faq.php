<html>
    <head>
        <title>Samwat.ch - FAQ</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.8.1/css/bulma.min.css" integrity="sha256-1nEaE91OpXJD7M6W5uSiqxhdmrY+lOOTHC1iUxU9Pds=" crossorigin="anonymous" />
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
                <img src="https://s3.fr-par.scw.cloud/static.samwat.ch/branding/Logo.png" alt="Samwath.ch Logo">
                <h1 class="title is-1">FAQ</h1>
                <div class="content" style="text-align: left">
                    <ol>
                        <li>Why are there no results when I search by agency/subtier/office?</li><br>
                        <p>This is because what is displayed on the beta.sam.gov page as the agency name is not always the same as how it is stored in the database. </p>
                        <p>For example, if you search for everything where the Subtier is "U.S. Immigration and Customs Enforcement (ICE)" as the title is displayed on the beta.sam.gov page, the search will not return any results. This is because the name is written as "US Immigration and Customs Enforcement", without the periods in "US." To avoid this, I recommend searching by "contains" instead of searching for exact match with "is." For example, searching for awards where the department contains "Homeland Security" instead of searching for "Department of Homeland Security."</p>
                        <li>Is the data I enter private?</li><br>
                        <p>The Samwat.ch page is secured with SSL, so the information you input will not be intercepted by others on the network without significant effort and access. However, your email address is saved in plaintext, as that is required to be able to send you emails, in a database I control. All access to said database requires a 128 character password, but breaches are always possible.</p>
                        <li>When will I receive my results?</li><br>
                        <p>The Federal Service Desk allows <a href="https://gsafsddev.servicenowservices.com/fsd-gov/answer.do?sysparm_kbid=003670c1db5108106861fd721f9619dd&sysparm_search=pmr">10 requests per day</a> to their APIs for non-government users. Because of this limitation, it is impossible for Samwat.ch to search on demand.</p><p> To work around this, every day at 11am UTC, Samwat.ch uses 2-4 requests to get and save all Federal Award Notices from the last 24 hours. Then, searches are performed on the local copy of the data. When the searches are complete, you will receive a single email with all of the results. This process will repeat every 24 hours until you unsubscribe.</p>
                    </ol>
                </div>
    </body>
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
</html>