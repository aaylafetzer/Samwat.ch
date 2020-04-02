import requests


def opportunitySearchLabel(template, search):
    """
    Populate an opportunity search label for an email
    :param template: Path to the template file
    :param search: Search details
    :return: String
    """
    text = "Awards where "
    fields = ["id", "sendto", "department", "subTier", "office", "title", "solicitationNumber",
              "naicsCode", "classificationCode"]
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
