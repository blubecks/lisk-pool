import requests, json, datetime,logging
from ConfigParser import SafeConfigParser
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.lisk_pool

parser = SafeConfigParser()
parser.read('config.ini')

logging.basicConfig(format='[%(asctime)s] %(message)s', filename='logger.log', level=logging.INFO)

host = parser.get('Node','protocol')+parser.get('Node','ip')+parser.get('Node','port')
endpoint = parser.get('Node','endpoint')
params = parser.get('Node','params')
pub_key = parser.get('Node','pub_key')


def check_time_diff(last_update, now):
    """
    Return True if more than 24 hours has passed from last update

    :param last_update: 
    :param now: 
    :return: boolean 
    """
    return now - last_update > datetime.timedelta(1)


r = requests.get(host + endpoint + params + pub_key)

voters = json.loads(r.text)['accounts']
voters_already_in_pool = db.voters

for v in voters:
    voter = voters.find_one({'address': v['address']})
    if voter:
        if not check_time_diff(voter['updated_at'], datetime.datetime.now()):
            db.voters.update(
                {'address': v['address']},
                {'$set': {
                    'updated_at': datetime.datetime.now(),
                    'address': v['address'],
                    'username': v['username'],
                    'publicKey': v['publicKey'],
                    'balance': v['balance']
                }
                })
            info_str = "{} day in pool not updated".format(v['username'])
        else:
            db.voters.update(
                {'address': v['address']},
                {'$inc': {'day_in_pool': 1},
                 '$set': {
                     'updated_at': datetime.datetime.now(),
                     'address': v['address'],
                     'username': v['username'],
                     'publicKey': v['publicKey'],
                     'balance': v['balance']
                 }
                 })
            info_str = "{} day in pool updated".format(v['username'])
    else:
        db.voters.insert_one({
            'address': v['address'],
            'day_in_pool': 1,
            'updated_at': datetime.datetime.now(),
            'username': v['username'],
            'publicKey': v['publicKey'],
            'balance': v['balance']
        })
        info_str = "{} welcome".format(v['username'])
    logging.info(info_str)

