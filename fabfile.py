__author__ = 'peter'


from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists


env.project = 'smyt_test'
env.vw_source = 'source venv/smyt_test/bin/activate'
env.hosts = ['srv@smyt_test.infosreda.ru']
env.directory = '/home/srv/%(project)s' % env
env.shell = '/bin/bash --noprofile -l -c'

env.ve_lines = '\n'.join(['', 'export PIP_RESPECT_VIRTUALENV=true',
                          'export PROJECT_HOME=$HOME/.virtualenvs',
                          env.vw_source, ''])

env.rsync_excludes = ['*.pyc', '*~', 'etc/*', 'fabfile.py', 'sessions', 'media',
                      '.git', 'binary', 'server_new', 'tmp', 'venv']

def pre_deploy():
    local('pip freeze > requirements.txt', capture=False)


def rsync():
    pre_deploy()
    rsync_project('~/%(project)s/' % env, './', exclude=env.rsync_excludes)


def post_rsync():
    with cd(env.directory):
        run('source ~/.virtualenvs/smyt_test/bin/activate;' \
            'pip install -r requirements.txt;')


def deploy():
    rsync()
    post_rsync()


def mkvirtualenv():
    run('mkvirtualenv smyt_test')


def install():
    rsync()
    if not exists('/home/srv/.virtualenvs'):
        run('mkdir ~/.virtualenvs')

    mkvirtualenv()
    post_rsync()

def restart():
    sudo("service nginx restart")

def update():
    rsync()
    restart()
