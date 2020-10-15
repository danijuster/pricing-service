from app import db_conf
from common.MongoDatabase import MongoDatabase
from common.PostgresqlDatabase import PostgresqlDatabase
from models.alert import Alert
from dotenv import load_dotenv

from models.model import Model

load_dotenv()
if db_conf['type'] == "postgresql":
    Model.initialize(PostgresqlDatabase)
else:
    Model.initialize(MongoDatabase)

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()
    alert.json()

if not alerts:
    print("No alerts have been created. Add an item and an alert to begin!")