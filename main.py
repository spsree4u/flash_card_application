
import os
# import logging
from flask import Flask
from flask import render_template

from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore

from application.config import LocalDevelopmentConfig
from application.models import User, Role
from application.api import DecksAPI, DeckAPI, CardAPI, UserAPI
from application.database import db
from application import workers

# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s ')

app = None
api = None
celery = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv("ENV", "development") == 'production':
        raise Exception("Currently no production config is setup")
    else:
        app.config.from_object(LocalDevelopmentConfig)
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(os.path.dirname(__file__), 'db_directory/testdb.sqlite3')
    db.init_app(app)
    api = Api(app)
    # cors settings to make the API working in platforms like swagger
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)

    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask

    app.app_context().push()
    return app, api, celery


app, api, celery = create_app()
from application.controllers import *

# API mapping
api.add_resource(DecksAPI, "/api/decks")
api.add_resource(DeckAPI, "/api/deck/<int:deck_id>", "/api/deck")
api.add_resource(CardAPI, "/api/deck/<int:deck_id>/card/<string:word>", "/api/card")
api.add_resource(UserAPI, "/api/user")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
    # app.debug = True
    # app.run()
    app.run(debug=True, port='3000', host='0.0.0.0')
