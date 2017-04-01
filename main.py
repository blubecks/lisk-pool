import requests, json, datetime
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.lisk_pool

host = 'http://<ip/domain>:7000'
endpoint = '/api/delegates/voters'
params = '?publicKey='
pub_key = '<pool pub keys>'

r = requests.get(host+endpoint+params+pub_key)

voters = json.loads(r.text)['accounts']

for v in voters:
    a = db.voters.update(
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