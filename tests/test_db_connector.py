import pytest
import supabase
from src import db_connector


@pytest.fixture
def sample_url() -> str:
    return "test_url"


@pytest.fixture
def sample_short_code() -> str:
    return "abcdef"


@pytest.fixture
def sample_validity_days() -> int:
    return -1


def test_add_and_get_url(sample_url, sample_short_code, sample_validity_days):
    db_connector.add_url(sample_url, sample_short_code, sample_validity_days)

    assert db_connector.get_url(sample_short_code) == sample_url


def test_add_existing_url(sample_url, sample_short_code, sample_validity_days):
    with pytest.raises(supabase.PostgrestAPIError):
        db_connector.add_url(sample_url, sample_short_code, sample_validity_days)


def test_increment_clicks(sample_short_code):
    db_connector.increment_clicks(sample_short_code)

    assert db_connector.get_data(sample_short_code)["clicks"] == 1


def test_delete_short_code(sample_short_code):
    db_connector.delete_url(sample_short_code)

    assert db_connector.get_data(sample_short_code) == None
    assert db_connector.get_url(sample_short_code) == None


def test_delete_expired_urls(sample_url, sample_short_code, sample_validity_days):
    db_connector.add_url(sample_url, sample_short_code, sample_validity_days)
    db_connector.delete_expired_urls()

    assert db_connector.get_data(sample_short_code) == None
    assert db_connector.get_url(sample_validity_days) == None
