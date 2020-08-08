import msal
import logging
import requests
import json

config = {
    "authority": "https://login.microsoftonline.com/9f4083b0-0ac6-4dee-b0bb-b78b1436f9f3",
    "client_id": "d584a43a-c4c1-4fbe-9c1c-3cae87420e6e",
    "scope": [ "https://graph.microsoft.com/.default" ],
    "secret": "v_a6AzL9BdlFzu5.RVKaehho-4J3s~w667",
    "endpoint": "https://graph.microsoft.com/v1.0/users"
}



# Create a preferably long-lived app instance that maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"]
    )

# The pattern to acquire a token looks like this.
result = None

# First, the code looks up a token from the cache.
# Because we're looking for a token for the current app, not for a user,
# use None for the account parameter.
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    # Call a protected API with the access token.
    endpoint_root = 'https://graph.microsoft.com/v1.0'
    http_headers = {
        'Authorization' : 'Bearer ' + result['access_token'],
        'Accept'        : 'application/json',
        'Content-Type'  : 'application/json'
    }
    # Look for our site
    siteName='MFPersonal'
    endpoint = '{}/sites?search={}'.format(endpoint_root, siteName)
    siteq = requests.get(endpoint, headers=http_headers, stream=False).json()
    # We may not have a site
    try:
        our_site = None
        for a_site in siteq['value']:
            if a_site['name'] == siteName:
                our_site = a_site
                break
    
        list_ep = '{}/sites/{}/lists/{}'.format(endpoint_root, our_site['id'], 'Test%20List')
        the_list = requests.get(list_ep, headers=http_headers, stream=False).json()
        listitem_ep  = '{}/sites/{}/lists/{}/items'.format(endpoint_root, our_site['id'], the_list['id'])
        the_items = requests.get(listitem_ep, headers=http_headers, stream=False).json()
        an_item_ep = '{}/sites/{}/lists/{}/items/1'.format(endpoint_root, our_site['id'], the_list['id'])
        an_item = requests.get(an_item_ep, headers=http_headers, stream=False).json()
        new_item = {
            'fields': {
                'Title' : 'Another item',
                'testfield' : 'another test field'
            }
        }
        payload = json.dumps(new_item)
        new_item_ep = '{}/sites/{}/lists/{}/items'.format(endpoint_root, our_site['id'], the_list['id'])
        make_new_item = requests.post(new_item_ep, headers=http_headers, data=payload, stream=False).json()
    except Error as e:
        print(str(e))

    print(result["token_type"])
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You might need this when reporting a bug.