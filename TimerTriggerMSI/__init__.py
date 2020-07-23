import datetime
import logging
import requests
import pyodbc
import os
import struct
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    #calling msi function to connect to db
    connection_db=connect_msi_db()
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

"""
Our team is successfully using Azure, Python, Linux, and ODBC Driver 17 for SQL Server to connect to Azure databases using Managed Service Identities.
We aren't using `Authentication=ActiveDirectoryMsi` in the connection string to do this.
Instead we are pulling in the `"MSI_SECRET` and `MSI_ENDPOINT` environment variables to retrieve and access token.
and we include that token with the connection string.
"""
def connect_msi_db():
    try:
        logging.info("using msi to connect to db")
        #retirves db connections from setting.json
        driver =  os.environ["driver"]
        server =  os.environ["server"]
        database =  os.environ["database"]
        #to get msi_endpoint and msi_secret , enable Identity in function app settings
        msi_endpoint = os.environ["MSI_ENDPOINT"]
        msi_secret = os.environ["MSI_SECRET"]
        #url is used to get the token for connection
        resource_uri = 'https://database.windows.net/'
        token_auth_uri = f"{msi_endpoint}?resource={resource_uri}&api-version=2017-09-01"
        head_msi = {'Secret': msi_secret}
        resp = requests.get(token_auth_uri, headers=head_msi)
        access_token = resp.json()['access_token']
        accesstoken = bytes(access_token, 'utf-8')
        exptoken = b""
        for i in accesstoken:
            exptoken += bytes({i})
            exptoken += bytes(1)
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken
        conn_string = 'driver=%s; server=%s; database=%s;' % (driver, server, database)
        logging.info(f'connection string : {conn_string}')
        conn = pyodbc.connect(conn_string,attrs_before={1256: bytearray(tokenstruct)})
        logging.info(f'connected to db : {os.environ["database"]}')
        return conn
    except Exception as ex :    
         logging.info (f"DB connection Failed : {ex}")
         raise Exception(f"DB connection Failed : {ex}")