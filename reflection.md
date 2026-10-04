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

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
