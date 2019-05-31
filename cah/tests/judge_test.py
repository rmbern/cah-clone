import string

import cah
import startup
from startup import client, run_db_script

def test_select_winner(client):
  run_db_script("test_select_winner.sql")
  
  with client.session_transaction() as test_session:
    test_session['username'] = 'player 3' # Set to judge in sql file

  res = client.post('/select-winner',
              data = {"answer-button":"Player 1 answer"},
              follow_redirects = True)
  assert b'<td> player 1 </td>' in res.data
  assert b'<td> 7 </td>' in res.data

def test_judge_answered(client):
  run_db_script("test_judge_answered.sql")
  
  res = client.get('/judge-answered', follow_redirects = True)

  assert b'DID NOT ANSWER' in res.data

  with startup.get_app().app_context():
    cah.db.get_db().execute(
      "UPDATE players"
      " SET ANSWER = 'Player 3 answer'"
      " WHERE judge = 1"
    )
    cah.db.get_db().commit()

  res = client.get('/judge-answered', follow_redirects = True)

  assert b'ANSWERED' in res.data    
