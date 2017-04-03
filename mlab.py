import mongoengine
# mongodb://<dbuser>:<dbpassword>@ds139430.mlab.com:39430/mango
host = "ds139430.mlab.com"
port = 39430
db_name = "mango"
username = "admin"
password = "admin"

def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)
def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]
def item2json(item):
    import json
    return json.loads(item.to_json())