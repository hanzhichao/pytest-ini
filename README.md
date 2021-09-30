# pytest-ini

复用pytest.ini分环境存储变量

这里考虑借用pytest.ini来完成配置，由于pytest.ini实际只使用了一个[pytest]段，我们可以增加其他段的配置，比如

增加全局变量[global]段
增加不同环境的[test]、[beta]、[prod]段
如下

```ini
# pytest.ini
[pytest]
addopts = -qs  
env = prod

[global]
a = 1
b = 2
[test]
a=2
[beta]
a=3
[prod]
a=4
```
