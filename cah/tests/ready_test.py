import startup
from startup import client, run_db_script
import cah.db

def test_ready(client):
  
  run_db_script("test_ready.sql")

  with client.session_transaction() as test_session:
    test_session['username'] = 'asdf'

  res = client.post('/submit-ready', follow_redirects = True)
  assert b'asdf is ready' in res.data

  with startup.get_app().app_context():
    
    # Check ready and answer flags are properly set
    rec = cah.db.get_db().execute("SELECT ready, answer FROM players"
                                  " WHERE name = 'asdf'").fetchone()
    assert rec['ready'] == 1 
    assert rec['answer'] == None

  # TODO: Check judge and question did not change

def test_ready_with_updates(client):
  # Similar to the test above, but all playrs will be ready
  # once the post is sent, so the judge and question should
  # be updated.
  run_db_script("test_ready_with_updates.sql")

  # Get all information before our post switches to
  # a new round, which involves a lot of changes to
  # the database.
  initial_judge = ""
  initial_question = ""
  inital_player_recs = []
  with startup.get_app().app_context():

    initial_judge = cah.db.get_db().execute(
      'SELECT name FROM players'
      ' WHERE judge = 1'
    ).fetchone()['name']

    initial_question = cah.db.get_db().execute(
      'SELECT question FROM current_question'
    ).fetchone()['question']
    with client.session_transaction() as test_session:
      test_session['username'] = "asdf"

    res = client.post('/submit-ready', follow_redirects = True)
    assert b'asdf is ready' in res.data

    # Check ready and answer flags are properly set
    rec = cah.db.get_db().execute("SELECT ready, answer FROM players"
                                  " WHERE name = 'asdf'").fetchone()
    assert rec['ready'] == 1 
    assert rec['answer'] == None

    # Check that the question has changed.
    new_question = cah.db.get_db().execute(
      "SELECT question FROM current_question"
    ).fetchone()['question']

    assert new_question != initial_question

    # Check that the judge has changed.
    new_judge = cah.db.get_db().execute(
      "SELECT name FROM players"
      " WHERE judge = 1"
    ).fetchone()['name']

    assert new_judge != initial_judge

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
