import pytest
from unittest.mock import patch
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

def config_patcher(json = {}, hostname = None, port = None, dispatcher = None, nodes = None):
    def config_decorator(func):
        def func_wrapper():
            patcher = patch('devrim.configurators._load_file')
            mock = patcher.start()
            mock.return_value = json
            config = load(hostname = hostname, port = port, dispatcher = dispatcher, nodes = nodes)
            patcher.stop()
            func(config)
        return func_wrapper
    return config_decorator

@config_patcher({
        'server':{   
            'hostname':'localhost',
            'port':4242
            },
            'nodes':{
                'localhost:5001'
            }
        })
def test_port_should_be_4242(mocked_config):
    assert int(mocked_config.port) == 4242

@config_patcher({
        'server':{   
            'hostname':'localhost',
            'port':4343
            },
            'nodes':{
                'localhost:5001'
            }
        }, hostname = '127.0.0.1')
def test_others_should_not_be_overrided_if_hostname_is_given(mocked_config):
    assert mocked_config.hostname == "127.0.0.1"
    assert mocked_config.port == 4343
    assert len(mocked_config.nodes) == 1

@config_patcher({
        'server':{   
            'hostname':'localhost',
            'port':4242
            },
            'nodes':{
                'localhost:5001',
                'localhost:5002'
            }
        }, port = 4432)
def test_others_should_not_be_overrided_if_port_is_given(mocked_config):
    assert mocked_config.port == 4432
    assert mocked_config.hostname == "localhost"
    assert len(mocked_config.nodes) == 2

@config_patcher({
        'server':{   
            'hostname':'localhost',
            'port':4242
            },
            'nodes':{
                'localhost:5001',
                'localhost:5002'
            }
        }, nodes = ['localhost:4243'])
def test_others_should_not_be_overrided_if_nodes_is_given(mocked_config):
    assert mocked_config.nodes[0] == "localhost:4243"
    assert mocked_config.hostname == "localhost"
    assert mocked_config.port == 4242