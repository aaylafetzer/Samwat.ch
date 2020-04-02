import requests
import datetime


def getOpportunitiesData(url, key, date=datetime.datetime.today()):
    """
    Get the opportunities data from beta.sam.gov for a given date
    :param url: sam.gov API url
    :param key: sam.gov API key
    :param date: Today's date
    :return: dict
    """
    getParameters = {
        "api_key": key,
        "limit": 1000,  # Maximum supported by API
        "postedFrom": f"{date.month}/{date.day - 2}/{date.year}",
        "postedTo": f"{date.month}/{date.day - 1}/{date.year}",
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
            break  # TODO: REMOVE FOR PRODUCTION
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
