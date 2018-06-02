# coding=utf-8
import json
from os.path import expanduser

import facebook_business
import facebookads

from connector.facebook_api import some_import_method

auth_config = json.load(
    open(expanduser("~") + '/.ads-hub/fb-token', 'r')
)

app_id = auth_config["app_id"]
app_secret = auth_config["app_secret"]
access_token = auth_config["access_token"]

facebookads.FacebookAdsApi.init(app_id, app_secret, access_token)
facebook_business.FacebookAdsApi.init(app_id, app_secret, access_token)

# ids = (1034901646550640, 122961418485088, 1868848106489319,)

# for _id in ids:
#     try:
some_import_method(0)
# except Exception as e:
#     print e.message
