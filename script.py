import configparser

# Email imports
import smtplib
import ssl
from email.message import EmailMessage

# Data imports
import datetime
import requests
import copy

# Database imports
import psycopg2


# Read configuration file
config = configparser.ConfigParser()
config.read("config.ini")

# Get Data from SAM.gov
d = datetime.datetime.today()
getParameters = {
    "api_key": config["SAM"]["api_key"],
    "limit": 1000,  # Maximum supported by API
    "postedFrom": f"{d.month}/{d.day-2}/{d.year}",
    "postedTo": f"{d.month}/{d.day-1}/{d.year}",
    "offset": 0
}

data = None  # Define empty variable to be filled with JSON data later

while True:
    print("Getting data from beta.sam.gov API")
    r = requests.get(config["SAM"]["request_url"], params=getParameters)
    workingData = r.json()
    if data is None:
        data = workingData
        continue  # Don't duplicate awards
    if not workingData["opportunitiesData"]:
        break  # No more data to manage
    else:
        data["opportunitiesData"].append(workingData["opportunitiesData"])
        getParameters["offset"] += 1000
        break

data = [item for item in data["opportunitiesData"] if type(item) is dict]  # The rest of the info isn't useful
# Set up email server
# Create Email Message
sender_email = config["EMAIL"]["sender_email"]
sender_password = config["EMAIL"]["sender_password"]
sender_server = config["EMAIL"]["sender_server"]

# Get searches from postgresql database
conn = psycopg2.connect(database="filters",
                        user=config['SQL']['username'],
                        password=config['SQL']['password'],
                        host=config['SQL']['endpoint_url'],
                        port=config['SQL']['port'])
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT sendto FROM searches;")
emails = cursor.fetchall()

# Load html elements
with open(config["TEMPLATES"]["results_template"], 'r') as file:
    message_template = file.read()
with open(config["TEMPLATES"]["result"], 'r') as file:
    result_template = file.read()
with open(config["TEMPLATES"]["search_label"], 'r') as file:
    search_template = file.read()

for email in emails:
    hits = ""
    cursor.execute(f"SELECT * FROM searches WHERE sendto=\'{email[0]}\'")
    searches = cursor.fetchall()
    print("Performing searches for " + email[0])
    for search in searches:
        print(search)
        working_data = copy.deepcopy(data)
        fields = ["id", "sendto", "department", "subTier", "office", "title", "basetype", "solicitationNumber",
                  "naicsCode", "classificiationCode"]
        # Build the search label while results are being processed
        label = "Awards where "
        for i in range(len(fields)):
            if i < 2:
                i += 1
                continue
            if search[i] is None:
                continue
            else:
                if search[i][0:2] == "e/":
                    label += fields[i] + " is \"" + search[i][2:] + "\", "
                    # Test for values equal to the search
                    working_data = [item for item in working_data if item[fields[i]] == search[i][2:]]
                elif search[i][0:2] == "c/":
                    label += fields[i] + " contains \"" + search[i][2:] + "\", "
                    # Test for items that contain the search
                    working_data = [item for item in working_data if search[i][2:].lower() in item[fields[i]].lower()]
        # Add search label to message
        hits += search_template.replace("{Search}", label[:-2] + ":")
        # Add formatted results to message
        if len(working_data) != 0:
            for result in working_data:
                # Get title of NAICS code
                try:
                    r = requests.get(config["NAICS"]["request_url"] + result["naicsCode"])
                    naicsTitle = r.json()["title"]
                except TypeError:
                    naicsTitle = ""
                except KeyError:
                    naicsTitle = ""

                if result["naicsCode"] is None:
                    result["naicsCode"] = ""

                for value in result:
                    if result[value] is None:
                        result[value] = "None"

                render = result_template\
                    .replace("{department}", result["department"])\
                    .replace("{subTier}", result["subTier"])\
                    .replace("{office}", result["office"])\
                    .replace("{title}", result["title"])\
                    .replace("{baseType}", result["baseType"])\
                    .replace("{uiLink}", result["uiLink"])\
                    .replace("{solicitationNumber}", result["solicitationNumber"])\
                    .replace("{naicsCode}", result["naicsCode"])\
                    .replace("{naicsTitle}", naicsTitle)\
                    .replace("{classificationCode}", result["classificationCode"])
                hits += render
        else:
            hits += "<p style=\"line-height: 1.2; word-break: break-word; font-size: 18px; " \
                    "mso-line-height-alt: 22px; margin: 0;\"><span style=\"font-size: 18px;\">No Results</span></p><br>"
    finalMessage = message_template.replace("{Searches}", hits)\
        .replace("{Results}", "")\
        .replace("{year}", str(d.year)) \
        .replace("\xc2\xa0", " ")\
        .replace("Â", " ")
    message = EmailMessage()
    message["Subject"] = "Your Daily Samwat.ch Results"
    message["From"] = "Samwat.ch noreply@samwat.ch"
    message["To"] = email
    # Include this in case people use fpbad clients
    message.preamble = "Unfortunately, you need a MIME-aware mail reader to read Samwat.ch messages"
    # Turn these into plain/html MIMEText objects
    message.set_content(finalMessage, "html")
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    print("Sending email to " + email[0])
    with smtplib.SMTP_SSL(sender_server, 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, email, message.as_string()
        )
