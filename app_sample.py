# from tests.test_configurators import basic_conf_should_be_loaded
# print(basic_conf_should_be_loaded())

# from tests.test_devrim import test_devrim_object
# test_devrim_object()

from devrim.devrim import Devrim
devrim_instance = Devrim()
devrim_instance.run()

# from devrim.configurators import load
# config = load(port = 4243)
