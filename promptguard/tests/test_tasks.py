"""Tests for task configurations."""
from promptguard.server.tasks import TASK_IDS, get_task
import pytest


class TestTaskConfigs:
    def test_three_tasks(self):
        assert TASK_IDS == ["easy", "medium", "hard"]

    def test_get_each_task(self):
        for tid in TASK_IDS:
            task = get_task(tid)
            assert task["task_id"] == tid
            assert "persona" in task
            assert "description" in task
            assert "allowed_behaviors" in task
            assert "forbidden_behaviors" in task
            assert "attack_categories" in task
            assert "sensitive_fragments" in task
            assert "queries" in task

    def test_unknown_task_raises(self):
        with pytest.raises(ValueError):
            get_task("nonexistent")

    def test_easy_has_20_queries(self):
        assert len(get_task("easy")["queries"]) == 20

    def test_medium_has_18_queries(self):
        assert len(get_task("medium")["queries"]) == 18

    def test_hard_has_16_queries(self):
        assert len(get_task("hard")["queries"]) == 16

    def test_query_structure(self):
        for tid in TASK_IDS:
            for q in get_task(tid)["queries"]:
                assert "query" in q and len(q["query"]) > 5
                assert "must_contain_any" in q and isinstance(q["must_contain_any"], list)
                assert "must_not_contain" in q and isinstance(q["must_not_contain"], list)
                assert "min_response_length" in q
                assert "max_response_length" in q

    def test_attack_categories_match_difficulty(self):
        easy = get_task("easy")
        assert set(easy["attack_categories"]) == {"direct_override", "role_play"}

        medium = get_task("medium")
        assert set(medium["attack_categories"]) == {"direct_override", "role_play", "encoding_obfuscation", "context_manipulation"}

        hard = get_task("hard")
        assert len(hard["attack_categories"]) == 6
