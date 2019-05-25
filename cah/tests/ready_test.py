import startup
from startup import client, run_db_script
import cah.db

def test_ready(client):
  
  run_db_script("test_ready.sql")

  with client.session_transaction() as test_session:
    test_session['username'] = 'asdf'

  res = client.post('/submit-ready', follow_redirects = True)
  with startup.get_app().app_context():
    rec = cah.db.get_db().execute("SELECT ready FROM players"
                                  " WHERE name = 'asdf'").fetchone()
    assert rec['ready'] == 1 
    assert b'asdf is ready' in res.data

def test_bad_session_ready(client):
  res = client.post('/submit-ready', follow_redirects = True)

  assert b"You don't exist!" in res.data

def test_all_ready(client):
  run_db_script("test_all_ready.sql")

  res = client.get('/ask-if-ready', follow_redirects = True)

  assert b"READY" in res.data
  assert b"NOT" not in res.data

def test_not_all_ready(client):
  run_db_script("test_not_all_ready.sql")

  res = client.get('/ask-if-ready', follow_redirects = True)

  assert b"NOT READY" in res.data
