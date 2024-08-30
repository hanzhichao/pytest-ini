import configparser
import json
import os
from configparser import ConfigParser
from string import Template
from collections import ChainMap

import pytest


def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="choose env: test,beta,prod")
    parser.addini('env', help="choose env: test,beta,prod")


class CaseSensitiveConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

    @staticmethod
    def ensure_value(value: str):
        """转为value为各种类型"""
        if value is None:
            return value

        # 转为整形
        if value.isdigit():
            return int(value)

        # 转为True、False或None
        if value.lower() in ['true', 'on']:
            return True

        if value.lower() in ['false', 'off']:
            return False

        if value.lower() in ['~', 'none', 'null']:
            return None

        # 尝试转为浮点型
        try:
            return float(value)
        except ValueError:
            pass

        # 尝试解码JSON
        if value.lstrip().startswith('[') or value.lstrip().startswith('{'):
            try:
                return json.loads(value)
            except (TypeError, json.decoder.JSONDecodeError):
                pass

        # 替换${变量}为系统环境变量值
        if '$' in value:
            return Template(value).safe_substitute(**dict(os.environ))

        # 处理相对路径
        # if isinstance(value, str) and value.startswith('.'):
        #     pass

        return value

    def get(self, section, option, *args, **kwargs):
        try:
            value = super().get(section, option, *args, **kwargs)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None
        return self.ensure_value(value)


@pytest.fixture(scope='session')
def ini(request):
    """
    :return CaseSensitiveConfigParser obj for pytest.ini
    """
    inifile = request.config.inifile
    ini = CaseSensitiveConfigParser(allow_no_value=True)
    request.config.ini = ini
    ini.read(inifile, encoding='utf-8')
    return ini


@pytest.fixture(scope='session')
def env_vars(request, ini):
    """
    :return: ChainMap variables for [<env>], [global] section in pytest.ini and system environment variables
    """
    config = request.config
    # 当前所配置的环境
    cur_env = config.getoption('--env') or config.getini('env')
    # 支持 env = ${USER}
    if cur_env and cur_env.startswith('$'):
        cur_env = os.environ[cur_env.strip('${}')]

    # 当前环境变量，全局变量，系统环境变量
    _env_vars, _global_vars, _sys_env_vars = {}, {}, os.environ

    if ini.has_section('global'):
        _global_vars = {option: ini.get('global', option) for option in ini.options('global')}

    if ini.has_section(cur_env):
        _env_vars = {option: ini.get(cur_env, option) for option in ini.options(cur_env)}

    return ChainMap(_env_vars, _global_vars, _sys_env_vars)
