# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** 
   - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number guessing game built with Streamlit. The player picks a difficulty (Easy 1-20 with 6 attempts, Normal 1-100 with 8, Hard 1-50 with 5), guesses the secret number, and gets a Higher/Lower hint after each guess. Score starts at 100 and drops by 10 with every wrong guess.

**Bugs found:**
- Hints were backwards (a guess below the secret said "Go LOWER!").
- "Attempts left" did not go down after the first guess.
- The score in Developer Debug Info differed from the final score in the win message. On even-numbered attempts the secret was converted to a string before comparing, so the outcome and score were wrong.
- New Game reset the secret and attempts but not the game status, so guesses stayed blocked after a win.

**Fixes applied:**
- Hints now point toward the secret: "📉 Go LOWER!" for a high guess, "📈 Go HIGHER!" for a low guess.
- Attempts start at 0 and increase by one per submitted guess.
- The secret is always compared as an integer, and score starts at 100, loses 10 per wrong guess, and is kept on a win.
- New Game now sets the status back to "playing".
- Moved game logic (`check_guess`, `parse_guess`, `update_score`, `get_range_for_difficulty`) into `logic_utils.py` and added tests in `tests/test_game_logic.py`.

## 📸 Demo Walkthrough

1. The game starts on Normal difficulty. The sidebar shows "Range: 1 to 100" and "Attempts allowed: 8", and the main panel reads "Guess a number between 1 and 100. Attempts left: 8". The Developer Debug Info expander shows Secret: 89, Attempts: 0, Score: 100, History: [].
2. The player enters 40 and clicks "Submit Guess 🚀". The game shows "📈 Go HIGHER!", attempts left drops to 7, and the score drops to 90.
3. The player enters 90. The game shows "📉 Go LOWER!", attempts left drops to 6, and the score drops to 80.
4. The player enters 89. The game shows "🎉 Correct!" and balloons, along with "You won! The secret was 89. Final score: 80".
5. Any further submit shows "You already won. Start a new game to play again." until "New Game 🔁" is clicked.
6. Clicking "New Game 🔁" resets the game with a new secret, 8 attempts left, and Score: 100, and new guesses are accepted again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

The tests cover `check_guess()`, `update_score()`, and a full-app test that uses Streamlit's `AppTest` to run the app in memory with the secret fixed at 50 and verify attempts and score after each guess.

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
rootdir: ../ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
testpaths: tests
collected 8 items

tests/test_game_logic.py ........                                        [100%]

============================== 8 passed in 0.79s ===============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
