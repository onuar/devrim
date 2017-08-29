import pytest
from devrim.configurators import load
from devrim.models import Configuration

def test_server_hostname_should_be_localhost():
    config = load()
    assert config.hostname == "localhost"

def test_there_should_be_three_nodes():
    config = load()
    assert len(config.nodes) == 3

# def test_port_should_be_integer():
#     with pytest.raises(TypeError) as excinfo:
#         settings = load()
#     assert 'port should be an integer' in str(excinfo.value)

def test_port_should_be_4242():
    config = load()
    assert int(config.port) == 4242

def test_others_should_not_be_overrided_if_hostname_is_given():
    config = load(hostname = "127.0.0.1")
    assert config.hostname == "127.0.0.1"
    assert config.port == 4242
    assert len(config.nodes) == 3

def test_others_should_not_be_overrided_if_port_is_given():
    config = load(port = 4243)
    assert config.port == 4243
    assert config.hostname == "localhost"
    assert len(config.nodes) == 3

def test_others_should_not_be_overrided_if_nodes_is_given():
    nodes = ["localhost:4243"]
    config = load(nodes = nodes)
    assert config.nodes[0] == "localhost:4243"
    assert config.hostname == "localhost"
    assert config.port == 4242