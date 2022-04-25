

def test_env_variable_in_ini(conf):
    print(conf.get('email', 'user'))

