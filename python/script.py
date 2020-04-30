import configparser
import os

# Import other script files
from fetch import samFunctions
from fetch import disclosuresFunctions
import emailFunctions
import databaseFunctions
import smtpFunctions

import datetime

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

print(datetime.datetime.now())  # Print date to log file

# Read configuration file
config = configparser.ConfigParser()
config.read(FILE_PATH + "/config.ini")

# Create memory database
memConn, memCursor = databaseFunctions.createMemoryDatabase(config["MEMDB"]["path"])
databaseFunctions.createMemoryTables(memCursor)

# Get Opportunities Data from SAM.gov
if config["ACTIONS"]["sam"] == "True":
    opportunitiesData = samFunctions.getOpportunitiesData(config["SAM"]["opportunitiesRequestUrl"],
                                                          config["SAM"]["apiKey"])
    # Put data into memory database
    for opportunity in opportunitiesData:
        if type(opportunity) is not dict:
            continue
        databaseFunctions.insertOpportunity(memCursor,
                                            opportunity["department"],
                                            opportunity["subTier"],
                                            opportunity["office"],
                                            opportunity["title"],
                                            opportunity["solicitationNumber"],
                                            opportunity["naicsCode"],
                                            opportunity["classificationCode"],
                                            opportunity["uiLink"],
                                            opportunity["baseType"])

# Get Senate Disclosures Data from senatestockwatcher
if config["ACTIONS"]["senatedisclosures"] == "True":
    senateDisclosuresData = disclosuresFunctions.getDisclosures(config["SENATEDISCLOSURES"]["url"])
    for senator in senateDisclosuresData:
        senatorName = senator["first_name"] + " " + senator["last_name"]
        for disclosure in senator["transactions"]:
            databaseFunctions.insertSenateDisclosure(memCursor,
                                                     disclosure["transaction_date"],
                                                     disclosure["owner"],
                                                     disclosure["ticker"],
                                                     disclosure["asset_description"],
                                                     disclosure["asset_type"],
                                                     disclosure["type"],
                                                     disclosure["amount"],
                                                     disclosure["comment"],
                                                     senatorName,
                                                     senator["ptr_link"])


# Create connection to pSQL database
managedConn, managedCursor = databaseFunctions.pSQLConnection(config['SQL']['endpointUrl'],
                                                              config['SQL']['port'],
                                                              config['SQL']['username'],
                                                              config['SQL']['password'])

# Get all email addresses from managed database
emails = databaseFunctions.getEmailAddresses(managedCursor)

# Load html elements
searchLabelTemplate = FILE_PATH + config["TEMPLATES"]["searchLabelTemplate"]
opportunityResultTemplate = FILE_PATH + config["TEMPLATES"]["opportunityResultTemplate"]
senateDisclosureResultTemplate = FILE_PATH + config["TEMPLATES"]["senateDisclosureResultTemplate"]
finalMessageTemplate = FILE_PATH + config["TEMPLATES"]["finalMessageTemplate"]
noResultsTemplate = FILE_PATH + config["TEMPLATES"]["noResultsTemplate"]

# Preform searches
for address in [item[0] for item in emails]:  # Email addresses are returned as tuples with a single string
    finalMessageContent = []  # Contain all elements of the mail in an array for easier organization

    # Process contract opportunities
    opportunityFilters = databaseFunctions.getOpportunityFiltersByEmail(managedCursor, address)
    for currentFilter in opportunityFilters:
        print(f"-----\n{currentFilter}")
        # Append search label to message
        finalMessageContent.append(emailFunctions.opportunitySearchLabel(searchLabelTemplate,
                                                                         currentFilter))
        opportunitiesSearchResults = databaseFunctions.searchOpportunities(memCursor, currentFilter)
        print("Found " + str(len(opportunitiesSearchResults)) + " result(s).")
        if len(opportunitiesSearchResults) is not 0:
            for opportunityResult in opportunitiesSearchResults:
                # Append results
                finalMessageContent.append(emailFunctions.opportunityResultTemplate(opportunityResultTemplate,
                                                                                    opportunityResult,
                                                                                    config["NAICS"]["requestUrl"]))
        else:
            finalMessageContent.append(emailFunctions.noResults(noResultsTemplate))  # Append no results

    # Process Senate Financial Disclosures
    senateDisclosureFilters = databaseFunctions.getSenateDisclosureFiltersByEmail(managedCursor, address)
    for currentFilter in senateDisclosureFilters:
        print(f"-----\n{currentFilter}")
        # Appen search label to message
        finalMessageContent.append(emailFunctions.senateDisclosureSearchLabel(searchLabelTemplate,
                                                                              currentFilter))
        senateDisclosuresSearchResults = databaseFunctions.searchSenateDisclosures(memCursor, currentFilter)
        print("Found " + str(len(senateDisclosuresSearchResults)) + " result(s).")
        if len(senateDisclosuresSearchResults) is not 0:
            for disclosure in senateDisclosuresSearchResults:
                # Append results
                finalMessageContent.append(emailFunctions.senateDisclosureResultTemplate(senateDisclosureResultTemplate,
                                                                                         disclosure,
                                                                                         config["STOCKS"]["url"],
                                                                                         config["STOCKS"]["apikey"]))
        else:
            finalMessageContent.append(emailFunctions.noResults(noResultsTemplate))  # Append no results
    # Create final message
    finalMessageHtml = emailFunctions.finalMessage(finalMessageTemplate, finalMessageContent, address)
    if config["ACTIONS"]["mail"] == "send":
        smtpFunctions.sendMail(
            config["EMAIL"]["senderEmail"],
            config["EMAIL"]["senderPassword"],
            config["EMAIL"]["senderServer"],
            config["EMAIL"]["smtpPort"],
            address,
            finalMessageHtml
        )
    elif config["ACTIONS"]["mail"] == "local":
        if not os.path.exists("mail/"):
            os.mkdir("mail")
        with open("mail/" + address + ".html", "w") as outfile:
            outfile.write(finalMessageHtml)
