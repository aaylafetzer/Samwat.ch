import requests


def getDisclosures(url):
    """
    Get disclosures from senatestockwatcher.com
    :param url:
    :return: Array
    """
    data = requests.get(url).json()
    return data
