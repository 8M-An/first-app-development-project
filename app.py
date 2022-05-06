import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

app = None
api = None


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Starting Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

# Add all restful controllers
from application.api import Deck_api,Card_api,cards_of_deck_api,decks_of_user_api
api.add_resource(Deck_api,'/api/decks/<uname>/<psw>/<int:deck_id>', '/api/decks/<uname>/<psw>')
api.add_resource(Card_api,'/api/cards/<uname>/<psw>/<int:fc_id>','/api/cards/<uname>/<psw>')
api.add_resource(cards_of_deck_api,'/api/deck/cards/<username>/<password>/<int:deck_id>')
api.add_resource(decks_of_user_api,'/api/user/decks/<username>/<password>')

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=5000)
