import json
import logging
import os

import requests
from azure.storage.blob import BlobClient


logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))


def etl():
    # request existing data from webservices endpoint
    api_key = os.environ["API_KEY"]
    conn_str = os.environ["AzureWebJobsStorage"]
    container_name = os.environ["CONTAINER_NAME"]
    file_name = os.getenv("FILE_NAME", "ita_taxonomy_labels.json")
    url = f"https://api.trade.gov/ita_taxonomies/search?api_key={api_key}&size=-1"
    req = requests.get(url)
    json_response = req.json()
    logging.info(f"Loaded {json_response['total']} records from {url}")
    # upload results JSON array to Blob
    blob = BlobClient.from_connection_string(
        conn_str=conn_str, container_name=container_name, blob_name=file_name
    )
    blob.upload_blob(json.dumps(json_response["results"]), overwrite=True)
    logging.info(f"Uploaded JSON to {file_name} blob in {container_name} container")


if __name__ == "__main__":
    # execute only if run as a script
    etl()
