"""Tests for attack bank integrity."""
from promptguard.server.attacks import ATTACK_CATEGORIES, get_attacks


class TestAttackBank:
    def test_six_categories(self):
        assert len(ATTACK_CATEGORIES) == 6

    def test_total_60_attacks(self):
        all_attacks = get_attacks()
        assert len(all_attacks) == 60

    def test_10_per_category(self):
        all_attacks = get_attacks()
        for cat in ATTACK_CATEGORIES:
            count = sum(1 for a in all_attacks if a["category"] == cat)
            assert count == 10, f"{cat} has {count} attacks, expected 10"

    def test_unique_ids(self):
        all_attacks = get_attacks()
        ids = [a["id"] for a in all_attacks]
        assert len(ids) == len(set(ids))

    def test_valid_structure(self):
        for a in get_attacks():
            assert "id" in a
            assert "category" in a
            assert "prompt" in a and len(a["prompt"]) > 10
            assert "canary" in a and len(a["canary"]) > 0
            assert "difficulty" in a and isinstance(a["difficulty"], list)

    def test_easy_has_20(self):
        assert len(get_attacks("easy")) == 20

    def test_medium_has_40(self):
        assert len(get_attacks("medium")) == 40

    def test_hard_has_60(self):
        assert len(get_attacks("hard")) == 60
