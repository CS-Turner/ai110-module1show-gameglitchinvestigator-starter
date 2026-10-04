# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**First Impression:** 
When I first ran the game, it showed instructions "Guess a number between 1 and 100. Attempts left: 8", a Developer Debug Info dropdown, Enter your guess: field, and Submit Guess and New Game buttons.

**Bugs I noticed from the start:**
1. Hints are backwards: a guess below the secret says "Go LOWER!"
2. Attempts counter didn't go down after my first guess.
3. Score in Debug Info differs from the score in the win message.
4. New Game doesn't reset the game status, so guesses stay blocked after a win.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|------------------------|
| Guess 5 (Secret 52) | "Go HIGHER!" | "Go LOWER!" | none | check_guess() return messages, app.py |
| Started the game (Attempts allowed: 8), then made one guess | "Attempts left: 7" after the first guess | "Attempts left: 8" (no change after the first guess) | none | attempts counter initialization and increment, app.py |
| Guess 6 (Secret 6), win | Developer Debug Info score matches the on-screen final score | On-screen message says "Final score: 55"; Debug Info says "Score: -5" | none | update_score() (app.py), and the debug panel's read of st.session_state.score |
| Won the game, clicked new game, then submitted a guess | Accepts new guesses. | Secret and attempts reset in Debug Info, but the guess was still blocked with message "You already won. Start a new game to play again." | none | New Game button never sets new status to playing, app.py |

---

## 2. How did you use AI as a teammate?

**AI tools I used on this project:** I used GitHub Copilot in VS Code chat to diagnose bugs and make code changes, and Claude chats in a project to talk through the steps and documentation.

**One AI suggestion that I accepted as correct:** When the Debug Info score didn't match the final score in the win message, Copilot pointed out that this was a script-order problem, not random state corruption. I probed further and found the real cause: on even-numbered attempts, the secret was converted to a string before the comparison, so the outcome and score came out wrong. Copilot's diagnosis was correct, and I verified it by starting a new game, guessing on both odd and even attempts, and confirming the Debug Info score and the win message matched.

**Suggestion I did not accept as written:** Copilot's first fix reported the score after applying the current attempt's deduction, so a first-try win showed 90 instead of 100. I restored the checkpoint because that didn't match how scoring should work, and told the assistant the rule I wanted: the score is 100 at the start, drops 10 for each incorrect guess, and stays unchanged on a correct guess. Copilot then reworked `update_score()` into a remaining-score model. I verified it by playing games won on the 1st, 2nd, 3rd, 4th, and 8th attempts, where a win on attempt 3 shows 100 → 90 → 80 → 80 and the Debug Info score matches the win message. I also added pytest cases for `update_score()`, such as 100 with a Win staying 100 and 100 with Too Low becoming 90.

---

## 3. Debugging and testing your fixes

**How I decided a bug was really fixed:** After each fix I restarted the app, since a new game generates a new secret, and replayed the inputs from my reproduction log to compare against the expected behavior. I guessed above and below the secret to check the hints, confirmed attempts left dropped by one per guess, and clicked New Game after a win to confirm my next guess was accepted. For the score, I played games won on the 1st, 2nd, 3rd, 4th, and 8th attempts and checked that the Debug Info score matched the win message.

**One test I ran and what it showed:** My `tests/test_game_logic.py` checks `check_guess()` for a win, too high, and too low, and checks `update_score()` at several points in a game (for example, a win at 100 keeps the score, and a wrong guess at 90 drops it to 80). The most useful test was `test_score_and_attempts_update_for_each_guess`. Because the real secret is random, the test uses Streamlit's `AppTest` to run the app in memory and fix the secret at 50, so it can guess 60 and then 50 and check attempts and score after each guess. It mattered because my earlier score tests passed while the app still showed the wrong score, which showed me that testing a single function wasn't enough to catch a bug in how the app flows from guess to guess.

**How AI helped me understand tests:** When the score tests passed but the app was still wrong, I asked Copilot to rewrite the tests to cover more score cases (a win keeping the score, wrong guesses dropping it by 10) instead of only the case I had been checking. When plain `pytest` failed with `ModuleNotFoundError: No module named 'logic_utils'` while `python -m pytest` worked, I used a Claude chat to understand why. I added a `pytest.ini` with `pythonpath = .`, and all 8 tests passed. I learned that pytest needs to be told where to find my modules.

---

## 4. What did you learn about Streamlit and state?

**What a rerun is:** Every time a player interacts with the page, such as clicking Submit Guess or New Game, Streamlit runs the whole script from top to bottom.

**What session state is:** Normal variables are rebuilt on every rerun, but values stored in `st.session_state` survive them. That is why the secret stays the same until the New Game button is clicked.

**Where my bugs came from:** The score mismatch had two causes. One was a script-order problem: the Debug Info was drawn before the score was updated, so it showed the previous run's value and disagreed with the final score message. The other was a logic problem: on even-numbered attempts the secret was converted to a string before the comparison, so the outcome and score came out wrong. The New Game bug was a state problem: session state keeps its values across reruns, so nothing resets unless the code resets it, and New Game never set `status` back to `"playing"`.

---

## 5. Looking ahead: your developer habits

**A habit I want to reuse:** Documenting as I go. My prompting strategy worked well, but I got carried away implementing changes before writing down the problem and the fix. Next time I'll write the reproduction row first, then fix the bug, then commit, so each bug gets its own commit and the history tells the evolution.

**What I would do differently with AI:** I would stick with one assistant at a time. I used Copilot for the code changes and Claude chats for planning and documentation, and some feedback and fixes were lost in translation between them.

**How this changed my thinking about AI-generated code:** Your honest answer, 1 to 2 sentences. For example: AI-generated code can look finished and still be wrong, since the starter shipped with four bugs. Good diagnosis still requires validation, like when I rejected Copilot's first scoring fix because it didn't follow the rule I had intended.