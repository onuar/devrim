from devrim._internals import _log
from devrim.dispatchers import RoundRobinDispatcher, WeightedRoundRobin

def test_round_robin_config_should_be_a_list():
    config_json = {
        'nodes':[
            'localhost:5001',
            'localhost:5002',
            'localhost:5003'
        ]
    }
    robin = RoundRobinDispatcher(json_data = config_json)
    assert isinstance(robin.nodes, list)

def test_round_robin_init_nodes_should_override_json_data_nodes():
    config_json = {
        'nodes':[
            'localhost:5001',
            'localhost:5002',
            'localhost:5003'
        ]
    }
    init_nodes = [
        'localhost:5001'
    ]
    robin = RoundRobinDispatcher(json_data = config_json, nodes = init_nodes)
    assert len(robin.nodes) == 1

def test_round_robin_should_always_give_next_one():
    config_json = {
        'nodes':[
            'localhost:5001',
            'localhost:5002',
            'localhost:5003'
        ]
    }
    robin = RoundRobinDispatcher(json_data = config_json)
    first = robin.get_next_one()
    assert first == 'localhost:5001'
    second = robin.get_next_one()
    assert second == 'localhost:5002'
    third = robin.get_next_one()
    assert third == 'localhost:5003'
    return_to_first = robin.get_next_one()
    assert return_to_first == 'localhost:5001'

def test_weighted_robin_config_should_be_a_json_object_list():
    config_json = {
        'nodes':[
            {'node':'localhost:5001', 'weight': 5},
            {'node':'localhost:5002', 'weight': 1},
            {'node':'localhost:5003', 'weight': 2}
        ]
    }
    weighted = WeightedRoundRobin(json_data = config_json)
    assert isinstance(weighted.nodes, object)

def test_weighted_robin_should_parse_with_weight_score():
    config_json = {
        'nodes':[
            {'node':'localhost:5001', 'weight': 5},
            {'node':'localhost:5002', 'weight': 1},
            {'node':'localhost:5003', 'weight': 2}
        ]
    }
    weighted = WeightedRoundRobin(json_data = config_json)
    assert weighted.nodes[0]['weight'] == 5
    assert weighted.nodes[1]['weight'] == 1
    assert weighted.nodes[2]['weight'] == 2

def assertion_weighted_robin_func(node_name, expecting):
    assert node_name == expecting


def test_weighted_robin_should_give_by_weight():
    config_json = {
        'nodes':[
            {'node':'localhost:5001', 'weight': 3},
            {'node':'localhost:5002', 'weight': 1},
            {'node':'localhost:5003', 'weight': 2}
        ]
    }
    weighted = WeightedRoundRobin(json_data = config_json)
    list(map(lambda node: assertion_weighted_robin_func(node, 'localhost:5001'), list(map(lambda x: weighted.get_next_one(), list(range(3))))))
    fourth_one = weighted.get_next_one()
    assert fourth_one == 'localhost:5002'
    list(map(lambda node: assertion_weighted_robin_func(node, 'localhost:5003'), list(map(lambda x: weighted.get_next_one(), list(range(2))))))
    list(map(lambda node: assertion_weighted_robin_func(node, 'localhost:5001'), list(map(lambda x: weighted.get_next_one(), list(range(3))))))