# pytest-ini
复用pytest.ini并增加环境配置

## 特性
- 支持分环境配置，如[test]、[stage]、[prod]
- 支持[global]全局变量配置
- 支持获取系统环境变量
- 支持在pytest.ini中引用系统环境变量，如`user = ${USER}`
- 支持在pytest.ini自定义配置各种配置段，如[email]，而无需添加自定义配置项
- 支持变量优先级 当前环境变量 > 全局变量 > 系统变量
- option大小写敏感
- option支持int、float、True、False、None、JSON类型及空值
- 支持原有的%(变量)s插值引用

## 安装方式
```shell
pip install pytest-ini
```

## 提供的Fixutes
- ini：ConfigParser配置对象，可以使用ini.get(section, option)来获取指定配置段指定变量值
- env_vars: 环境变量集合，ChainMap类型，包含当前指定环境的环境变量、配置的全局变量、系统环境变量

## 提供的参数及配置
- 提供`--env`参数，用于指定当前环境
- 提供`env`配置项，用于指定当前环境

## 使用方式
### 指定环境并读取环境配置
pytest.ini文件配置
```ini
[pytest]
env = prod

[email]
smtp_host = smtp.sina.com
smtp_user = test_results@sina.com
smtp_pwd = ${SMTP_PWD}

[global]
user = user001

[test]
user = test001

[prod]
user = ${USER}
is_male = true
age = 18
score = 87.5
hobbies = ["sing", "dance"]

base_url = https://httpbin.org
url = %(base_url)s/get?token=%(token)s
token =
```
使用示例如下：
```python
import os

def test_get_vars_from_pytest_ini(env_vars):
    # 获取当前环境变量'user'值
    user = env_vars.get('user')
    # 直接获取系统环境变量'USER'值
    user2 = env_vars.get('USER')
    
    assert user == os.getenv('USER')
    assert user2 == os.getenv('USER')
    
```
### 支持各种类型
- int: 如果值是个数字，则转为int
- float: 如果值可以转为float，则转为float
- True: 如果值转为小写为['true', 'on']其中之一，则值为True
- False: 如果值转为小写为['false', 'off']其中之一，则值为False
- None: 如果无该option或值转为小写为['~', 'null', 'none']其中之一，则值为None
- JSON字符串: 如果值以'['或'{'开头，则尝试转为JSON对应的列表或字典
- 空值: 如果只有`option = `没有值，则值为空字符串

使用示例如下：
```python
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
```
### 支持原生插值及[DEFAULT]默认值
支持ConfigParser原生的插值方式`%(变量名)s`，来引用当前section中的变量，也支持`%(Section:变量名)s`来引用其他段中的变量
同时也支持原有的[DEFAULT]默认配置
使用示例如下：
```python
def test_interpolate(env_vars):
    url = env_vars.get('url')
    token = env_vars.get('token')
    
    print(url, token)
    assert url == 'https://httpbin.org/get?token='
    assert token == ''
```

### 自定义其他配置段
设置系统环境变量
```shell
export SMTP_PWD=abcdefg
```
使用示例如下：
```shell
def test_get_options_from_pytest_ini(ini):
    smtp_host = ini.get('email', 'smtp_host')
    smtp_user = ini.get('email', 'smtp_user')
    smtp_pwd = ini.get('email', 'smtp_pwd')
    print(smtp_host, smtp_user, smtp_pwd)
```
其他fixture也可以引用`ini`这个fixture来读取pytest.ini中的任意值。

