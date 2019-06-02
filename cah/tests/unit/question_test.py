import cah
import startup
from startup import client, run_db_script

# Flask renderer escapes special characters into decimal.
# Python builtin html library escapes them into hex
# So we have to roll our own html escape function. 
def html_escape(escape_me):
  escape_table = {
                    '&':"&#35;",
                    '"':"&#34;",
                    "'":"&#39;",
                    "<":"&#60;",
                    ">":"&#62;"
                 }
  
  escaped_string = ""
  for i,c in enumerate(escape_me):
    if c in escape_table:
      escaped_string += escape_table[c]
    else:
      escaped_string += c
  
  return escaped_string

def test_serve_question(client):
  run_db_script("test_serve_question.sql")

  with startup.get_app().app_context(): # For DB access
    
    # Test a random question
    # TODO: Test all questions?
    question = cah.db.get_db().execute(
      'SELECT question FROM current_question').fetchone()['question']
    
    question = html_escape(question)
    question = bytes(question, 'utf-8')

    # Case for regular player (player 1 or 2 in sql script)
    with client.session_transaction() as test_session:
      test_session['username'] = "player 1"
    
    res = client.get('/question-phase', follow_redirects = True)

    assert b"your answer" in res.data
    assert question in res.data
  
    # Case for judge (player 3 in sql script)
    with client.session_transaction() as test_session:
      test_session['username'] = "player 3"
    
    res = client.get('/question-phase', follow_redirects = True)
    assert b"the best answer" in res.data
    assert question in res.data

# TODO: THINK OF SOME MORE ADVERSARIAL TESTS AND PUT THEM HERE :)
