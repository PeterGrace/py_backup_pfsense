"""The primary module for this skeleton application."""
import click
import requests
import re
import sys
import sh

def create_backup_file(username,password,router_ssl,filepath):
    retxt = 'var csrfMagicToken = "(.+?)";var csrfMagicName = "(.+?)";'

    s = requests.Session()
    r = s.get('https://%s/index.php' % (router_ssl,), verify=False)
    m = re.search(retxt, r.text)
    if not m:
        print "Couldn't get login token."
        sys.exit(0)

    login_data = {
        m.group(2): m.group(1),
        'usernamefld': username,
        'passwordfld': password,
        'login': 'Login',
    }

    r = s.post('https://%s/index.php' % (router_ssl,), verify=False, data=login_data)
    if r.text.find('Enter username and password to login.') != -1:
        print "Wasn't able to login."
        sys.exit(0)

    backup_data = {
        'backuparea':'',
        'donotbackuprrd':'on',
        'Submit':'Download configuration',
    }
    r = s.post('https://%s/diag_backup.php' % (router_ssl,), verify=False, data=backup_data)

    f = open(filepath, 'wb')
    f.write(r.text)
    f.close()

def commit_config_to_git(filepath):
    git = sh.git.bake(_cwd=os.path.split(filepath)[0])
    git.commit('-am', 'latest backup by py_backup_pfsense')
    git.push()
    

@click.command()
@click.argument('username',envvar='PBP_USER')
@click.argument('password',envvar='PBP_PASS')
@click.argument('router_ssl',envvar='PBP_ROUTER')
@click.argument('filepath',envvar='PBP_FILEPATH')
def main(username,password,router_ssl,filepath):
    '''Skeleton App made by pymkcli'''
    create_backup_file(username,password,router_ssl,filepath)
    commit_config_to_git()

if __name__ == '__main__':
    main()
