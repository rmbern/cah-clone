import sqlite3
from flask import g, current_app

def get_db():
  if 'db' not in g:
    # TODO: Move database to memory? Since this is a game,
    #       there's no need for the data to persist

    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
  
  # TODO: Return a cursor instead of a connection for posterity/portability?
  #       Will have to change any uses of connection.total_changes
  #       to cursor.connection.total_changes if we do this.
  return g.db

def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()
    

def init_db():
  db = get_db()

  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf-8'))

def init_app(app):
  init_db()
  app.teardown_appcontext(close_db)
