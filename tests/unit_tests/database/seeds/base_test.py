import logging
from unittest import mock

import pytest

from carnage.database.seeds import base


def test_monster_seed_init(database_session_mock):
    seed = base.BaseSeed()

    assert seed.name is not None
    assert seed.data is not None


@pytest.mark.parametrize(
    ("seed_exist"),
    (
        (True),
        (False),
    ),
)
def test_seed(seed_exist, database_session_mock, caplog):
    caplog.set_level(logging.INFO)
    seed = base.BaseSeed(mock.Mock())
    with mock.patch.object(seed, "validate_seed", lambda seed: seed_exist):
        seed.data = [{"name": "test"}]
        seed.seed()

        if not seed_exist:
            assert "Seeded 'base' successfully" in caplog.records[-1].message


def test_seed_value_error():
    seed = base.BaseSeed(mock.Mock())
    seed.data = None
    with pytest.raises(ValueError, match="No seed data found for base"):
        seed.seed()


@pytest.mark.parametrize(
    ("seed_exist"),
    (
        (True),
        (False),
    ),
)
def test_validate_seed(seed_exist, database_session_mock):
    seed = base.BaseSeed()
    with mock.patch.object(
        seed.repository,
        "select_by_name",
        lambda name: seed_exist,
    ):
        # We don't care too much about the rest
        assert seed.validate_seed(seed={"name": "test"}) == seed_exist
