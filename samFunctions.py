import requests
from datetime import datetime, timedelta
import json


def getOpportunitiesData(url, key):
    """
    Get the opportunities data from beta.sam.gov for a given date
    :param url: sam.gov API url
    :param key: sam.gov API key
    :return: dict
    """

    fromDate = datetime.now() - timedelta(days=1)

    getParameters = {
        "api_key": key,
        "limit": 1000,  # Maximum supported by API
        "postedFrom": fromDate.strftime('%m/%d/%Y'),
        "postedTo": datetime.today().strftime('%m/%d/%Y'),
        "offset": 0
    }

    data = None  # Make a blank object to be populated with data later

    # Get data from API
    while True:
        print("Getting opportunities data from beta.sam.gov API")
        r = requests.get(url, params=getParameters)
        workingData = r.json()
        if data is None:
            data = workingData
            continue  # Don't duplicate awards
        if not workingData["opportunitiesData"]:
            break  # No more data to manage
        else:
            data["opportunitiesData"].append(workingData["opportunitiesData"])
            getParameters["offset"] += getParameters["limit"]
            break

    # Sanitize returned data
    for award in data:
        for value in award:
            if value is None:
                award[value] = "None"

    # Return final output
    print("Retrieved " + str(len(data["opportunitiesData"])) + " records")
    return data["opportunitiesData"]
