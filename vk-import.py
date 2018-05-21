#!/usr/bin/python
import os
import urllib2
import json
import sys
from os.path import expanduser
import ConfigParser
import psycopg2
from datetime import datetime
from vkontakteapi import ads


def config(filename, section):
    # create a parser
    parser = ConfigParser.ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect(params):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #    if conn is not None:
    #        conn.close()
    #        print('Database connection closed.')
    return conn


# period = day | month | overall

cfg = json.load(open(expanduser("~") + '/.ads-hub/vk-token', 'r'))
ads_client = ads(cfg["access_token"])
# vkontakteapi.init(cfg["access_token"], True)

ids_types = ["ad", "campaign", "client", "office", ]

account_id = int(sys.argv[1])
# if ids_type not in ids_types:
#    raise Exception("Unexpected ids_type: " + ids_type + ". Try to use next - " + str(ids_types).strip('[]'))

# url = "https://api.vk.com/method/ads.getStatistics?access_token=%saccount_id=%d&ids_type=%s&ids=&period=day&date_from=%s&date_to=%s" % (
#        cfg["access_token"], account_id, ids_type,
#        None, datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
#    )

# try:
#     print(ads.get_statistics(
#         account_id, "ad", "month",
#         [42264607, 42264152, 41634720, 41428491]
#     ))
# except urllib2.HTTPError as ex:
#     if ex.code == 400:
#         print "You have not access for this account data"
#     else:
#         print ex.reason
#
# os._exit(0)

ads_list = ads_client.get_ads_layout(account_id)
print(ads_list)

conn = connect(config('database.ini', 'postgresql'))
cur = conn.cursor()

data = None
try:
    url = "https://api.vk.com/method/ads.getAdsLayout" \
          "?" \
          "access_token=%s&account_id=%d&include_deleted=1&v=5.74" % (
              cfg["access_token"], account_id)
    print url

    response = urllib2.urlopen(url)
    data = json.load(response)
except urllib2.HTTPError as ex:
    if ex.code == 400:
        print "You have not access for this account data"
    else:
        print ex.reason

args_str = list()
for row in data["response"]:
    args_str.append(cur.mogrify(
        "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ",
        (
            "vkontakte",
            0,
            datetime.now(),
            "????",
            row["id"],
            row["title"],
            row["link_url"],
            '{}',
            0,
            0,
            0,
            0
        )
    ))
query = "INSERT INTO advertising VALUES " + (", ".join(args_str)) + ";"
print(query)
result = cur.execute(query)
print(result)
conn.commit()
cur.close()
conn.close()
