from fabric.context_managers import settings
from fabric.api import env, run

env.key_filename = ["C:\\Users\\yuchenfei\\.ssh\\aliyun_qd"]


def _get_manage_dot_py(host):
    return '~/sites/{}/virtualenv/bin/python ~/sites/{}/source/manage.py'.format(host, host)


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string='yuchenfei@{}'.format(host)):
        run('{} flush --noinput'.format(manage_dot_py))


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string='yuchenfei@{}'.format(host)):
        session_key = run('{} create_session {}'.format(manage_dot_py, email))
        return session_key.strip()
