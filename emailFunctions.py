import requests
import numpy as np


def searchLabel(search, fields):
    text = ""
    for i in range(len(fields)):
        if i <= 1 or search[i] is None:
            continue  # Ignore id and sendto and don't search by NoneType
        else:
            text += fields[i]
        switch = search[i][:2]
        if switch == "c/":
            text += " contains "
        elif switch == "e/":
            text += " is "
        else:
            continue  # Database error
        text += search[i][2:] + ";"
    return text


def opportunitySearchLabel(template, search):
    """
    Populate an opportunity search label for an email
    :param template: Path to the template file
    :param search: Search details
    :return: String
    """
    text = "Opportunities where "
    fields = ["id", "sendto", "department", "subTier", "office", "title", "solicitationNumber",
              "naicsCode", "classificationCode"]
    text += searchLabel(search, fields)
    with open(template, "r") as source:
        return source.read()\
            .strip()\
            .replace("{Search}", text)


def senateDisclosureSearchLabel(template, search):
    """
    Populate an opportunity search label for an email
    :param template: Path to the template file
    :param search: Search details
    :return: String
    """
    text = "Senate Financial Disclosures where "
    fields = ["id", "sendto", "transaction_date", "owner", "ticker", "asset_type", "transaction_type", "amount",
              "comment", "senator", "ptr_link"]
    text += searchLabel(search, fields)
    with open(template, "r") as source:
        return source.read()\
            .strip()\
            .replace("{Search}", text)


def opportunityResultTemplate(template, result, naicsURL):
    with open(template, "r") as source:
        text = source.read()

    # Fill information known about opportunity from SAM API
    fields = ["id", "{department}", "{subTier}", "{office}", "{title}", "{solicitationNumber}",
              "{naicsCode}", "{classificationCode}", "{uiLink}", "{baseType}"]
    for i in range(len(fields)):
        text = text.replace(fields[i], str(result[i]))

    # Fill in NAICS Title
    if result[6] is not None:
        r = requests.get(naicsURL + result[6])
        try:
            text = text.replace("{naicsTitle}", r.json()["title"])
        except KeyError:
            text = text.replace(" - {naicsTitle}", "")
    else:
        text = text.replace(" - {naicsTitle}", "")

    text = text.replace("Â", "")  # Remove weird utf-8 artifacts
    return text


def senateDisclosureResultTemplate(template, result, url, key):
    with open(template, "r") as source:
        text = source.read()
    print(result)
    # Fill information known about opportunity from SAM API
    fields = ["id", "{transaction_date}", "{owner}", "{ticker}", "{asset_description}", "{asset_type}",
              "{transaction_type}", "{amount}", "{comment}", "{senator}", "{ptr_link}"]
    for i in range(len(fields)):
        text = text.replace(fields[i], str(result[i]).strip())
    text = text.replace("--", "N/A")

    # Test for ticker price
    if result[3] != "--" and "Stock" in result[5]:
        getParameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": result[3],
            "apikey": key
        }

        try:
            r = requests.get(url, params=getParameters).json()
            r = r["Time Series (Daily)"]
            x = next(iter(r))
            text = text.replace("{price}", str(np.round(float(r[x]["4. close"]), 2)))
            priceChange = np.round(float(r[x]["4. close"]) - float(r[x]["1. open"]), 2)
            percentChange = np.round(100 * (priceChange / float(r[x]["1. open"])), 2)
            print(priceChange)
            if priceChange > 0:
                # Stock gained value
                priceChange = "+" + str(priceChange)
                text = text.replace("{priceStatus}", "green")
            elif priceChange < 0:
                # Stock lost value
                print("Oof")
                text = text.replace("{priceStatus}", "red")
            text = text.replace("{priceChange}", f"{priceChange} ({percentChange}%)")
        except KeyError:
            pass
    return text


def noResults(template):
    """
    Return the no results template
    :param template: String path to no results template file
    :return:
    """
    with open(template, "r") as source:
        return source.read()


def finalMessage(template, content, address):
    """
    Create the html for a final message to be delivered
    :param template: path to template
    :param content: array of content to add
    :param address: email address
    :return: string of html
    """
    content = "".join([item for item in content if item is not None])
    with open(template, "r") as source:
        text = source.read()
    text = text\
        .replace("{Content}", content.strip())\
        .replace("{email}", address)
    return text
