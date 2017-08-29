import pytest

from devrim.devrim import Devrim
from devrim.dispatchers import BaseDispatcher

@pytest.fixture
def default_devrim():
    devrim = Devrim()
    return devrim

def test_default_dispatcher_should_be_robin_round(default_devrim):
    default_devrim._load_configs()
    if not isinstance(default_devrim.dispatcher, BaseDispatcher):
        raise AssertionError('Default dispatcher should be Robin Round')

def test_default_dispatcher_should_be_robin_hood_algorithm():
    pass
    # devrim = Devrim()
    # devrim.run()