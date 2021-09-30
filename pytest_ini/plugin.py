from configparser import ConfigParser

import pytest


def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="choose env: test,beta,prod")
    parser.addini('env', help="choose env: test,beta,prod")


@pytest.fixture(scope='session')
def conf(request):
    """
    :return ConfigParser obj for pytest.ini
    """
    config = request.config
    inifile = config.inifile
    conf = ConfigParser()
    conf.read(inifile)
    return conf
    

@pytest.fixture(scope='session')
def env_vars(request, conf):
    """
    :return: dict type variables for [global] and [<env>] section in pytest.ini
    """
    config = request.config
    cur_env = config.getoption('--env') or config.getini('env')

    variables = {}
    if conf.has_section('global'):
        variables.update(conf.items('global'))
    if conf.has_section(cur_env):
        variables.update(conf.items(cur_env))
    return variables
