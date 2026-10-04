def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """Compare a guess against the secret and return the outcome label."""
    if guess == secret:
        return "Win"

    try:
        guess_value = int(guess)
        secret_value = int(secret)
    except (TypeError, ValueError):
        guess_text = str(guess)
        secret_text = str(secret)
        if guess_text == secret_text:
            return "Win"
        return "Too High" if guess_text > secret_text else "Too Low"

    if guess_value > secret_value:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str):
    """Deduct 10 points for an incorrect guess; retain the score on a win."""
    if outcome == "Win":
        return current_score
    return current_score - 10
