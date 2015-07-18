"""The primary module for this skeleton application."""
import click
import requests
import re
import sys
import sh
import os

def create_backup_file(username, password, router_ssl, filepath):
    '''This function handles an https session with pfsense router, doing auth
       and saving the config to a local file.
    '''
    retxt = 'var csrfMagicToken = "(.+?)";var csrfMagicName = "(.+?)";'

    session = requests.Session()
    request = session.get('https://%s/index.php' % (router_ssl,), verify=False)
    match = re.search(retxt, request.text)
    if not match:
        print "Couldn't get login token."
        sys.exit(0)

    login_data = {
        match.group(2): match.group(1),
        'usernamefld': username,
        'passwordfld': password,
        'login': 'Login',
    }

    request = session.post(
        'https://%s/index.php' % (router_ssl,),
        verify=False,
        data=login_data
        )
    if request.text.find('Enter username and password to login.') != -1:
        print "Wasn't able to login."
        sys.exit(0)

    backup_data = {
        'backuparea':'',
        'donotbackuprrd':'on',
        'Submit':'Download configuration',
    }
    request = session.post(
        'https://%s/diag_backup.php' % (router_ssl,),
        verify=False,
        data=backup_data
        )

    backup_file = open(filepath, 'wb')
    backup_file.write(request.text)
    backup_file.close()

def commit_config_to_git(filepath):
    '''This function handles adding, committing, and pushing the config file to
       the git repository.
    '''
    # pylint: disable=E1101
    (path, filename) = os.path.split(filepath)
    git = sh.git.bake(_cwd=path)
    git.add(filename)
    git.commit('-m', 'latest backup by py_backup_pfsense')
    git.push()

@click.command()
@click.argument('username', envvar='PBP_USER')
@click.argument('password', envvar='PBP_PASS')
@click.argument('router_ssl', envvar='PBP_ROUTER')
@click.argument('filepath', envvar='PBP_FILEPATH')
def main(username, password, router_ssl, filepath):
    '''Main function calls backup function then git function'''
    create_backup_file(username, password, router_ssl, filepath)
    commit_config_to_git(filepath)
