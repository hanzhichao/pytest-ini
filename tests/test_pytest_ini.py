import os


def test_get_vars_from_pytest_ini(env_vars):
    # 获取当前环境变量'user'值
    user = env_vars.get('user')
    # 直接获取系统环境变量'USER'值
    user2 = env_vars.get('USER')
    
    assert user == os.getenv('USER')
    assert user2 == os.getenv('USER')


def test_get_options_from_pytest_ini(ini):
    smtp_host = ini.get('email', 'smtp_host')
    smtp_user = ini.get('email', 'smtp_user')
    smtp_pwd = ini.get('email', 'smtp_pwd')
    
    print(smtp_host, smtp_user, smtp_pwd)


def test_ensure_value(env_vars):
    name = env_vars.get('name')
    is_male = env_vars.get('is_male')
    age = env_vars.get('age')
    score = env_vars.get('score')
    hobbies = env_vars.get('hobbies')
    print(name, is_male, age, score, hobbies)
    
    assert name is None
    assert is_male is True
    assert age == 18
    assert score == 87.5
    assert hobbies == ['sing', 'dance']


def test_interpolate(env_vars):
    url = env_vars.get('url')
    token = env_vars.get('token')
    
    print(url, token)
    assert url == 'https://httpbin.org/get?token='
    assert token == ''
    


