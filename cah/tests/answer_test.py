import cah
import startup
from startup import client, run_db_script

def test_get_answers(client):
  # TODO: Should /get-answers really be dependent on a session?
  run_db_script("test_get_answers.sql")

  with client.session_transaction() as test_session:
    test_session['username'] = "player 1"

  res = client.get('/get-answers')
  
  # TODO: Right now, get-answers doesn't give the answer
  #       for the player within the current session.
  #       This would go away with the removal of session
  #       dependence.
  # assert b'PLAYER 1 ANSWER' in res.data
  assert b'PLAYER 2 ANSWER' in res.data

def test_all_answered(client):
  run_db_script("test_all_answered.sql")

  with client.session_transaction() as test_session:
    test_session['username'] = "player 1"
  res = client.get('/all-answered')

  assert b'ALL ANSWERED' in res.data

  with startup.get_app().app_context():
    cah.db.get_db().execute(
      "UPDATE players"
      " SET answer = NULL"
    " WHERE name = 'player 3'"
    )
    cah.db.get_db().commit()

  res = client.get('/all-answered')

  assert b'NOT ALL ANSWERED' in res.data
