import requests
import xmltodict
import json
from datetime import datetime


def customSort(filename):
    return datetime.strptime(filename[-15:-5], '%m_%d_%Y')


def getDisclosures(url):
    """
    Get disclosures from senatestockwatcher.com
    :param url:
    :return: Array
    """
    # Get list of files from S3 bucket
    data = requests.get(url).text
    data = xmltodict.parse(data)
    data = json.loads(json.dumps(data))
    data = data["ListBucketResult"]["Contents"]
    # Find newest file
    filenames = [item["Key"] for item in data if "data/" in item["Key"]][1:]
    filenames.sort(key=customSort)
    # Get data from latest report
    latest = requests.get(url + filenames[-1]).json()
    return latest
