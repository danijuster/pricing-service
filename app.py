import os
from flask import Flask, render_template
import config
from common.MongoDatabase import MongoDatabase
from common.PostgresqlDatabase import PostgresqlDatabase
from models.model import Model
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
from logger import logger


logger.debug('Initializing app')

app = Flask(__name__)
app.secret_key = 'q1w2e3r4'

app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

logger.debug(app.config['ADMIN'])

db_conf = config.config(section='database')

if db_conf['type'] == "postgresql":
    Model.initialize(PostgresqlDatabase)
else:
    Model.initialize(MongoDatabase)


@app.route('/')
def home():
    return render_template("home.html")


app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(user_blueprint, url_prefix='/users')


if __name__ == "__main__":
    app.run(debug=True)