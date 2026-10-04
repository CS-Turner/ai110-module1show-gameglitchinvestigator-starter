# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

**First Impression:** 
- What did the game look like the first time you ran it?
When I first ran the game, it showed instructions "Guess a number between 1 and 100. Attempts left: 6", a Developer Debug Info dropdown, Enter your guess: field, and Submit Guess and New Game buttons. 

**Bugs noticed:**
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1. Hints are backwards: a guess below the secret says "Go LOWER!"
2. Attempts counter shows 7 instead of 8 before any guess.
3. Score in Debug Info differs from the score in the win message.
4. New Game doesn't reset the game status, so guesses stay blocked after a win.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|------------------------|
| Guess 5 (Secret 52) | "Go HIGHER!" | "Go LOWER!" | none | check_guess() return messages, app.py lines 38, 40 |
| Started the game, made no guess (Attempts allowed: 8) | "Attempts left: 8" | "Attempts left: 7" | none | st.info() , app.py lines 109-112 |
| Guess 6 (Secret 6), win | Developer Debug Info score matches the on-screen final score | On-screen message says "Final score: 55"; Debug Info says "Score: -5" | none | update_score() (app.py lines 50-65), and the debug panel's read of st.session_state.score |
| Won the game, clicked new game, then submitted a guess | Accepts new guesses. | Secret and attempts reset in Debug Info, but the guess it still blocked with message "You already won. Start a new game to play again." | none | never sets new status to playing, app.py lines 134-138 |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? I used copilot in chat, and claude chats in a project. 
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). Noting that the "Go Higher! and "Go lower!" messages were backward let me condense the list of bugs noticed. 
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count. Copilot noticed that the mismatch bug is script-order problem, not a random state corruption bug: on even attempts, the secret is converted to a string before comparing. So the score is not updated properly. I verified this by starting a new game and testing. 

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
