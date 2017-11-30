from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/thorsoft/superlists.git'


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + '/superlists/secret_key.py'

    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'

    if not exists(virtualenv_folder + '/bin/pip3.6'):
        run(f'virtualenv --python=python3.6 {virtualenv_folder}')

    run(f'{virtualenv_folder}/bin/pip3.6 install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python3.6 manage.py collectstatic --noinput')

def _update_database(source_folder):
    run(f'cd {source_folder} && ../virtualenv/bin/python3.6 manage.py migrate --noinput')


def _create_nginx_conf(source_folder, site_name, user_name):
    nginx_template_file = source_folder + '/deploy_tools/nginx.template.conf'
    nginx_tmp_conf_file = source_folder + f'/deploy_tools/{site_name}_new'
    run(f'cp {nginx_template_file} {nginx_tmp_conf_file}')

    sed(nginx_tmp_conf_file, "SITENAME", f'{site_name}')
    sed(nginx_tmp_conf_file, "USER", f'{user_name}')

    nginx_conf_file = f'/etc/nginx/sites-available/{site_name}_new'
    run(f'sudo cp {nginx_tmp_conf_file} {nginx_conf_file}')


def _create_gunicorn_conf(source_folder, site_name, user):
    gunicorn_template_file = source_folder + '/deploy_tools/gunicorn-systemd.template.conf'
    gunicorn_tmp_conf_file = source_folder + f'/deploy_tools/{site_name}.conf_new'
    run(f'cp {gunicorn_template_file} {gunicorn_tmp_conf_file}')

    sed(gunicorn_tmp_conf_file, "SITENAME", f'{site_name}')
    sed(gunicorn_tmp_conf_file, "USER", f'{user}')

    gunicorn_conf_file = f'/lib/systemd/system/gunicorn-{site_name}_new'
    run(f'sudo cp {gunicorn_tmp_conf_file} {gunicorn_conf_file}')


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _create_nginx_conf(source_folder, env.host, env.user)
    _create_gunicorn_conf(source_folder, env.host, env.user)


