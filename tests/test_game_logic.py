from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

@pytest.mark.parametrize(
    ("current_score", "outcome", "expected_score"),
    [
        (100, "Win", 100),
        (100, "Too Low", 90),
        (90, "Too High", 80),
        (80, "Win", 80),
    ],
)
def test_score_starts_at_100_and_deducts_only_for_incorrect_guesses(
    current_score,
    outcome,
    expected_score,
):
    result = update_score(current_score, outcome)
    assert result == expected_score


def test_score_and_attempts_update_for_each_guess():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert app.session_state["attempts"] == 0
    assert app.session_state["score"] == 100

    app.session_state["secret"] = 50
    app.text_input[0].set_value("60")
    app.button[0].click()
    app.run()

    assert app.session_state["attempts"] == 1
    assert app.session_state["score"] == 90

    app.text_input[0].set_value("50")
    app.button[0].click()
    app.run()

    assert app.session_state["attempts"] == 2
    assert app.session_state["score"] == 90
