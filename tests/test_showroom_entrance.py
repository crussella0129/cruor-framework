"""The showroom's entrance: the front page's door, which bleeds, opens and
lets a visitor in, played by the showroom's script.

It is played only with script, only for a visitor who has not asked for
less motion, and only on arriving at the place itself. Without it the
showroom is as it is, which the showroom's own tests hold with script off.
"""

import json
import time

import pytest

import browser
import draw_readme
import draw_showroom
from helpers import ROOT, serve

SHOWROOM = "showroom/index.html"


@pytest.fixture(scope="module")
def engine():
    with browser.chromium() as found:
        yield found


@pytest.fixture(scope="module")
def address():
    with serve(ROOT) as (found, _):
        yield found


def entrance(page) -> dict:
    return page.evaluate(
        """() => {
            const veil = document.querySelector('.entrance');
            return {
                shown: !!veil,
                waits: document.documentElement.classList.contains('entrance-waits'),
                pictures: veil ? veil.querySelectorAll('image').length : 0,
                leaves: veil ? veil.querySelectorAll('[clip-path]').length : 0,
                running: document.getAnimations().length,
            };
        }"""
    )


def gone(page, within: float) -> bool:
    deadline = time.monotonic() + within
    while time.monotonic() < deadline:
        if not entrance(page)["shown"]:
            return True
        page.wait_for_timeout(100)
    return False


def test_the_door_is_the_front_pages():
    # The showroom keeps the front page's door as it is, and beside it where
    # its doorway, eyes and mouth lie, as the front page's script finds them.
    kept = ROOT / "showroom"
    assert (kept / draw_showroom.DOOR).read_bytes() == (
        ROOT / "assets" / "readme" / draw_readme.DOOR
    ).read_bytes()
    parts = json.loads((kept / draw_showroom.DOOR_PARTS).read_text(encoding="utf-8"))
    assert parts == draw_readme.door(ROOT).door
    # The doorway lies within the picture, and the head over it.
    assert 0 < parts["apex"] < parts["spring"] < parts["foot"] < parts["height"]
    assert parts["half"] > 0 and 0 < parts["middle"] < parts["width"]
    for x, y in [*parts["eyes"], parts["mouth"]]:
        assert abs(x - parts["middle"]) < parts["half"] and 0 < y < parts["apex"]


def test_the_entrance_plays_and_lets_the_visitor_in(engine, address):
    with browser.opened(engine, address + SHOWROOM, still=False) as page:
        found = entrance(page)
        assert found["shown"], found
        # The door, the two leaves it splits into, and the place behind it
        # held back until the door is up.
        assert found["pictures"] == 3 and found["leaves"] == 2, found
        assert not found["waits"]
        assert found["running"] >= 7
        # It ends, and the place is there.
        assert gone(page, 12), "the entrance never ended"
        assert page.evaluate("getComputedStyle(document.body).visibility") == "visible"
        assert page.locator("#head h1").is_visible()


def test_the_entrance_ends_at_a_key(engine, address):
    with browser.opened(engine, address + SHOWROOM, still=False) as page:
        assert entrance(page)["shown"]
        page.keyboard.press("Escape")
        assert gone(page, 2), "a key did not end the entrance"


def test_no_entrance_for_one_who_asks_for_less_motion(engine, address):
    with browser.opened(engine, address + SHOWROOM, still=True) as page:
        page.wait_for_timeout(500)
        found = entrance(page)
        assert not found["shown"] and not found["waits"], found


def test_no_entrance_into_a_room(engine, address):
    # One sent to a room of the place is let into it at once.
    with browser.opened(engine, address + SHOWROOM + "#rite", still=False) as page:
        page.wait_for_timeout(500)
        found = entrance(page)
        assert not found["shown"] and not found["waits"], found
