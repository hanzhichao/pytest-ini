import os
from configparser import ConfigParser
from string import Template
from collections import ChainMap

import pytest


def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="choose env: test,beta,prod")
    parser.addini('env', help="choose env: test,beta,prod")


class EnhancedConfigParser(ConfigParser):
    def get(self, section, option, *args, **kwargs):
        value = super().get(section, option, *args, **kwargs)
        if '$' in value:
            return Template(value).safe_substitute(value, **os.environ)


@pytest.fixture(scope='session')
def conf(request):
    """
    :return ConfigParser obj for pytest.ini
    """
    config = request.config
    inifile = config.inifile
    conf = EnhancedConfigParser()
    conf.read(inifile)
    return conf


@pytest.fixture(scope='session')
def env_vars(request, conf):
    """
    :return: ChainMap variables for [<env>], [global] section in pytest.ini and system environment variables
    """
    config = request.config
    # 当前所配置的环境
    cur_env = config.getoption('--env') or config.getini('env')
    
    # 当前环境变量，全局变量，系统环境变量
    _env_vars, _global_vars, _sys_env_vars = {}, {}, os.environ
    
    if conf.has_section('global') or config.has_section('GLOBAL'):
        _global_vars.update(conf.items('global') or conf.items('GLOBAL'))
    
    if conf.has_section(cur_env):
        _env_vars.update(conf.items(cur_env))
    return ChainMap(_env_vars, _global_vars, _sys_env_vars)
