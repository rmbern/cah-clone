import os
import subprocess
import pytest
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import cah

@pytest.fixture
def run_server():
  # Requires correct enviornment at the shell level
  # to run correctly.
  print("Starting server...")
  proc = subprocess.Popen(['flask', 'run'],
                          stdout=open('/dev/null', 'w'),
                          stderr=open('/dev/null', 'w'))
  # Make sure server is fully up before running tests
  time.sleep(1) 
  print("Server started!!!")
  yield proc
  proc.terminate()
  print("Server terminated!!!")

def test_sample_game(run_server):
  class Player:
    def __init__(self, driver, name, answer):
      self.driver = driver
      self.name = name
      self.answer = answer
      self.score = 0

  # Needed for debugging when my tty doesn't have X started.
  # os.environ['DISPLAY'] = ":0"

  options = webdriver.firefox.options.Options()
  options.headless = True

  # Using n unique players:
  # (For now, just use firefox clients.)
  # TODO: Check across multiple browsers.
  n = 3
  rounds = 3 
  # list of lists of the form [ driver index, driver object ] 
  players = [ Player(
                webdriver.Firefox(options=options),
                "Player {}".format(str(i)),
                "Answer for Player {}.".format(str(i))
             ) for i in range(n) ]

  for player in players:
    # Open a window and log in.
    # Note we only do this once per round.
    player.driver.get("http://localhost:5000")
    assert 'CAHCLONE!' in player.driver.find_element_by_tag_name("h1").text

    # Log in with a unique name.
    name_text_input = player.driver.find_element_by_id("username")
    name_text_input.send_keys(player.name)
    name_submit_button = player.driver.find_element_by_id("submit")
    name_submit_button.click()
    assert 'Welcome' in player.driver.find_element_by_tag_name("h1").text
    print(player.name + " has logged in.")

  for _ in range(rounds):
    print("\nROUND BEGIN.")
    for player in players:
      # Click on the ready button once all players have logged in.
      # TODO: Allow players to log into the game after it has started.
      player.driver.find_element_by_tag_name("input").click()
      assert player.name+" is ready!" in \
        player.driver.find_element_by_tag_name("h1").text

      print(player.name + " is ready.")
    

    judge_player = None
    for player in players:
      # Wait for answers if player is judge. Submit a unique one otherwise.
      try:
        # Wait until we see the answer submission form
        WebDriverWait(player.driver, 10).until(
          EC.presence_of_element_located((By.TAG_NAME, "form")))
        # When player is a typical player, submit an answer.
        answer_text_input = player.driver.find_element_by_id("answer")
        answer_text_input.send_keys(player.answer)
        answer_submit_button = player.driver.find_element_by_id("submit")
        answer_submit_button.click()
        assert 'for everyone' \
          in player.driver.find_element_by_tag_name("h1").text

        print('{} has answered "{}"'.format(player.name, player.answer))

      except NoSuchElementException:
        # Note this player is the judge, and then
        # move on to the next player
        if judge_player != None:
          raise ValueError("Multiple judges have been served to this test " + \
                           "in one round!")
        judge_player = player
        print(player.name  + " is the judge.")
        continue 
    
    # Now that we know who is the judge, make them wait until
    # all answers are available
    answers_seen = []
    while len(answers_seen) < len(players) - 1:
      answers_seen = \
        WebDriverWait(judge_player.driver, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, "input")))
    
    # The judge now needs to select an answer.
    print("The judge has seen all answers.")

    # To do this, select a random integer within the number
    # of players for an id to select from the ones assigned
    # to the different radial buttons on the judge menu.

    # Remeber that the js in the judge menu assigns each
    # radial button corresponding to a player answer an id
    # starting from zero and incrementing by one for each
    # button.

    r = random.Random()
    other_players = [ x for x in players if x is not judge_player ] 

    answer_id = r.randrange(0, len(other_players))

    winning_player = other_players[answer_id]

    winning_player.score += 1

    [ winning_answer_button ] = \
      [ x for x in judge_player.driver.find_elements_by_tag_name("input") \
        if x.get_attribute("value") == winning_player.answer ]
    
    winning_answer = winning_answer_button.get_attribute("value")
    winning_answer_button.click()
    
    winning_answer_submit = \
      judge_player.driver.find_element_by_id("submit-button")

    winning_answer_submit.click()

    print('{} has selected "{}" as the winning answer.'.format(
      judge_player.name, winning_answer))

    # Examine the scoreboard from all players, making sure the
    # winning player(s) had their score incremented on each board.
    for player in players:
      WebDriverWait(player.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table")))
      assert winning_answer \
        in player.driver.find_element_by_tag_name("h2").text
      
      # This also contains names, but for simplicity, we don't
      # filter them out.
      scores = [ x.text for x in player.driver.find_elements_by_tag_name("td") ]
      assert str(player.score) in scores

    print("ROUND END.\n")

    # TODO: On a different round, submit a few equal answers.

  for player in players:
    player.driver.quit()
