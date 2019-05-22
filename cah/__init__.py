import os
from flask import Flask, session
from werkzeug.contrib.cache import SimpleCache

def create_app(test_config=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='not so secret, huh?',
    DATABASE=os.path.join(app.instance_path, 'players.sqlite')
  )

  if test_config is None:
    app.config.from_pyfile('config.py', silent=True)
  else:
    app.config.from_mapping(test_config)

  try: os.makedirs(app.instance_path)
  except OSError:
    pass
  
  from . import db
  with app.app_context():
    db.init_app(app)

  from . import login
  app.register_blueprint(login.bp)

  from . import answer
  app.register_blueprint(answer.bp)

  from . import ready
  app.register_blueprint(ready.bp)

  from . import question
  app.register_blueprint(question.bp)

  from . import judge
  app.register_blueprint(judge.bp)

  from . import scoring
  app.register_blueprint(scoring.bp)

  return app

