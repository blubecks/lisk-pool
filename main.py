import requests, json, datetime,logging
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.lisk_pool

logging.basicConfig(format='[%(asctime)s] %(message)s', filename='logger.log', level=logging.INFO)

host = 'http://<ip/pool-domain>:7000'
endpoint = '/api/delegates/voters'
params = '?publicKey='
pub_key = '<pub-key>'

r = requests.get(host+endpoint+params+pub_key)

voters = json.loads(r.text)['accounts']

for v in voters:
    db.voters.update(
        {'address': v['address']},
        {

            '$inc': {'day_in_pool': 1},
            '$set': {
                'updated_at': datetime.datetime.now(),
                'address': v['address'],
                'username': v['username'],
                'publicKey': v['publicKey'],
                'balance': v['balance']
            }

        },
        True)
    info_str = "{} stored/updated".format(v['username'])
    logging.info(info_str)
