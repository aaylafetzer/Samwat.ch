import configparser
import os

# Data manipulation imports
# import requests

# Import other script files
import samFunctions
import emailFunctions
import databaseFunctions

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Read configuration file
config = configparser.ConfigParser()
config.read(FILE_PATH + "/config.ini")

# Get Opportunities Data from SAM.gov
opportunitiesData = samFunctions.getOpportunitiesData(config["SAM"]["opportunitiesRequestUrl"],
                                                      config["SAM"]["apiKey"])

# Put data into memory database
memConn, memCursor = databaseFunctions.createMemoryDatabase()
databaseFunctions.createMemoryTables(memCursor)
for opportunity in opportunitiesData:
    databaseFunctions.insertOpportunity(memCursor,
                                        opportunity["department"],
                                        opportunity["subTier"],
                                        opportunity["office"],
                                        opportunity["title"],
                                        opportunity["solicitationNumber"],
                                        opportunity["naicsCode"],
                                        opportunity["classificationCode"])
memCursor.execute("SELECT * FROM opportunities;")
with open("out.txt", "w") as outfile:
    x = memCursor.fetchall()
    for line in x:
        outfile.write(line)

exit()
# Set up email server
emailFunctions.createSever(config["EMAIL"]["senderEmail"],
                           config["EMAIL"]["senderPassword"],
                           config["EMAIL"]["senderServer"])

# Create connection to pSQL database
conn, cursor = databaseFunctions.pSQLConnection(config['SQL']['endpointUrl'],
                                                config['SQL']['port'],
                                                config['SQL']['username'],
                                                config['SQL']['password'])

# Get searches from pSQL database
emails = databaseFunctions.getEmailAddresses(cursor)

# Load html elements
with open(FILE_PATH + config["TEMPLATES"]["results_template"], 'r') as file:
    message_template = file.read()
with open(FILE_PATH + config["TEMPLATES"]["result"], 'r') as file:
    result_template = file.read()
with open(FILE_PATH + config["TEMPLATES"]["search_label"], 'r') as file:
    search_template = file.read()


# for email in emails:
#     email = email[0]  # Because it's a fucking tuple with one element for some dipshit reason
#     for search in databaseFunctions.getFiltersByEmail(memCursor, email):
#         opportunityResults = databaseFunctions.searchOpportunities(memCursor, search)
#
#         # TODO: Populate a results template
#
#
#     hits = ""
#     print("Performing searches for " + email[0])
#
#         # Add search label to message
#         hits += search_template.replace("{Search}", label[:-2] + ":")
#         # Add formatted results to message
#         if len(working_data) != 0:
#             for result in working_data:
#                 # Get title of NAICS code
#                 try:
#                     r = requests.get(config["NAICS"]["request_url"] + result["naicsCode"])
#                     naicsTitle = r.json()["title"]
#                 except TypeError:
#                     naicsTitle = ""
#                 except KeyError:
#                     naicsTitle = ""
#
#                 if type(result) is not dict:  # STOP GIVING ME MALFORMED DATA YOU CRETINS
#                     continue
#
#                 for value in result:
#                     if result[value] is None:
#                         result[value] = "None"
#
#                 render = result_template\
#                     .replace("{department}", result["department"])\
#                     .replace("{subTier}", result["subTier"])\
#                     .replace("{office}", result["office"])\
#                     .replace("{title}", result["title"])\
#                     .replace("{baseType}", result["baseType"])\
#                     .replace("{uiLink}", result["uiLink"])\
#                     .replace("{solicitationNumber}", result["solicitationNumber"])\
#                     .replace("{naicsCode}", result["naicsCode"])\
#                     .replace("{naicsTitle}", naicsTitle)\
#                     .replace("{classificationCode}", result["classificationCode"])
#                 hits += render
#         else:
#             hits += "<p style=\"line-height: 1.2; word-break: break-word; font-size: 18px; " \
#                     "mso-line-height-alt: 22px; margin: 0;\"><span style=\"font-size: 18px;\">" \
#                     "No Results</span></p><br>"
#     finalMessage = message_template.replace("{Searches}", hits)\
#         .replace("{Results}", "")\
#         .replace("{year}", str(d.year)) \
#         .replace("{email}", email[0]) \
#         .replace("\xc2\xa0", " ")\
#         .replace("Â", " ")
#     message = EmailMessage()
#     message["Subject"] = "Your Daily Samwat.ch Results"
#     message["From"] = "Samwat.ch noreply@samwat.ch"
#     message["To"] = email
#     # Include this in case people use bad clients
#     message.preamble = "Unfortunately, you need a MIME-aware mail reader to read Samwat.ch messages"
#     # Turn these into plain/html MIMEText objects
#     message.set_content(finalMessage, "html")
#     # Create secure connection with server and send email
#     context = ssl.create_default_context()
#     print("Sending email to " + email[0])
#     with smtplib.SMTP_SSL(sender_server, 465, context=context) as server:
#         server.login(sender_email, sender_password)
#         server.sendmail(
#             sender_email, email, message.as_string()
#         )
