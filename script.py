import configparser
import os

# Data manipulation imports
# import requests

# Import other script files
import samFunctions
import emailFunctions
import databaseFunctions
import smtpFunctions

import datetime

print(datetime.datetime.now())

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

# Read configuration file
config = configparser.ConfigParser()
config.read(FILE_PATH + "/config.ini")

# Get Opportunities Data from SAM.gov
opportunitiesData = samFunctions.getOpportunitiesData(config["SAM"]["opportunitiesRequestUrl"],
                                                      config["SAM"]["apiKey"])

# Put data into memory database
memConn, memCursor = databaseFunctions.createMemoryDatabase(config["MEMDB"]["path"])
databaseFunctions.createMemoryTables(memCursor)
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
finalMessageTemplate = FILE_PATH + config["TEMPLATES"]["finalMessageTemplate"]
noResultsTemplate = FILE_PATH + config["TEMPLATES"]["noResultsTemplate"]

# Preform searches
for address in [item[0] for item in emails]:  # Email addresses are returned as tuples with a single string
    finalMessageContent = []  # Contain all elements of the mail in an array for easier organization
    opportunityFilters = databaseFunctions.getFiltersByEmail(managedCursor, address)
    for currentFilter in opportunityFilters:
        print("-----")
        print(currentFilter)
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
    finalMessageHtml = emailFunctions.finalMessage(finalMessageTemplate, finalMessageContent, address)
    smtpFunctions.sendMail(
        config["EMAIL"]["senderEmail"],
        config["EMAIL"]["senderPassword"],
        config["EMAIL"]["senderServer"],
        config["EMAIL"]["smtpPort"],
        address,
        finalMessageHtml
    )
