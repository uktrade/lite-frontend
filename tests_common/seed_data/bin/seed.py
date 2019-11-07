import os

from .. import main


def _get_env():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_file = os.path.join(base_dir, '.env')

    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                key_value_pair = line.split('=')
                if len(key_value_pair) == 2:
                    os.environ[key_value_pair[0].strip()] = key_value_pair[1].strip()

    return os.environ


def _get_exporter_info(env):
    exporter_user_email = env['TEST_EXPORTER_SSO_EMAIL']
    exporter_user_password = env['TEST_EXPORTER_SSO_PASSWORD']
    exporter_user__name = env['TEST_EXPORTER_SSO_NAME']
    exporter_user_first_name, exporter_user_last_name = exporter_user__name.split(' ')

    return {
        'email': exporter_user_email,
        'password': exporter_user_password,
        'first_name': exporter_user_first_name,
        'last_name': exporter_user_last_name
    }


def _get_internal_info(env):
    gov_user_email = env['TEST_SSO_EMAIL']
    gov_user_password = env['TEST_SSO_PASSWORD']
    gov_user_name = env['TEST_SSO_NAME']
    gov_user_first_name, gov_user_last_name = gov_user_name.split(' ')

    return {
        'email': gov_user_email,
        'name': gov_user_name,
        'first_name': gov_user_first_name,
        'last_name': gov_user_last_name,
        'password': gov_user_password
    }


def _get_seed_data_config(exporter_info, internal_info):
    api_url = env['API_URL']

    return {
        'api_url': api_url,
        'exporter': exporter_info,
        'gov': internal_info
    }


if __name__ == '__main__':
    env = _get_env()
    exporter_info = _get_exporter_info(env)
    internal_info = _get_internal_info(env)
    seed_data_config = _get_seed_data_config(exporter_info, internal_info)

    seed_data = main.SeedData(seed_data_config)
