from fabric.api import env

from contextlib import contextmanager
from bashyucksyntax.utils import print_login
from os import getcwd, sep
from os.path import basename

__all__ = ('run', 'sudo', 'local', 'cd', 'rsync_project', 'put')

print ""
print "#! /bin/sh"

class Success(object):
    failed = False
    succeeded = True

env.print_login = True

@print_login
def sudo(command, shell=True, user=None, pty=False, quiet=False):
    "fake sudo command that only prints the sudo command"
    if user:
        print "sudo -u {0} {1}".format(user, command)
    else:
        print "sudo {0}".format(command)

    return Success

@print_login
def run(command, shell=True, pty=False, quiet=False):
    "Fake run command that only prints the command"
    print command
    return Success

def local(command, capture=True):
    "Fake local command that only print the command"
    print command
    return Success

@print_login
@contextmanager
def cd(path):
    "Fake cd context manager that only prints the cd command"
    if env.get('cwd'):
        new_cwd = env.cwd + '/' + path
    else:
        new_cwd = path
    env.cwd = new_cwd
    print "cd {cwd}".format(**env)
    yield


@contextmanager
def lcd(path):
    "Fake cd context manager that only prints the cd command"
    if env.get('lcwd'):
        new_cwd = env.lcwd + '/' + path
    else:
        new_cwd = path
    env.lcwd = new_cwd
    print "cd {lcwd}".format(**env)
    yield


def rsync_project(remote_dir, local_dir=None, exclude=(), delete=False, extra_opts=''):
    if not hasattr(exclude, '__iter__'):
        exclude = (exclude,)
    exclude_opts = ' --exclude "{0}"'.format(len(exclude))
    exclusions = tuple([str(s).replace('"', '\\\\"') for s in exclude])
    options_map = {
        "delete"  : '--delete' if delete else '',
        "exclude" : exclude_opts % exclusions,
        "extra"   : extra_opts
    }
    options = "{delete}{exclude} -pthrvz {extra}".format(**options_map)
    if local_dir is None:
        local_dir = '../' + getcwd().split(sep)[-1]
    cmd = "rsync {0} {1} {2}@{3}:{4}".format(options, local_dir, env.user,
        env.host, remote_dir)
    print cmd

def puts(message):
    print "echo %s" % message

def put(local_path, remote_path='', mode=None, use_sudo=False):
    "Fake put function that only prints the scp command"
    if use_sudo:
        print "scp {0} {1}@{2}:".format(local_path, env.user, env.host_string)
        print 'ssh root@%s "mv %s %s"' % (env.host_string, basename(local_path), remote_path)
    else:
        print "scp {0} {1}@{2}:{3}".format(local_path, env.user, env.host_string, remote_path)
    return [basename(local_path)]


def get(path, local_path='.'):
    print "wget %s -P %s" % (path, local_path)


@print_login
def open_shell(command):
    print command

@print_login
@contextmanager
def path(path, behavior='append'):
    if behavior == 'append':
        print "PATH=$PATH:%s" % path
    elif behavior == 'prepend':
        print "PATH=%s:$PATH" % path
    elif behavior == 'replace':
        print "PATH=%s" % path

    yield

# mokey patch fabric and fablib to use the dummy operations
import fabric.operations
import fabric.api
import fabric.context_managers
import fabric.contrib.project
import fabric.utils

# utils
# abort, warn, puts, fastprint
fabric.api.puts = puts
fabric.utils.puts = puts

# operations
# require, prompt, put, get, run, sudo, local,
#    reboot, open_shell
fabric.api.sudo = sudo
fabric.api.put = put
fabric.api.get= get
fabric.api.run = run
fabric.api.local = local
fabric.api.open_shell = open_shell
fabric.operations.sudo = sudo
fabric.operations.put = put
fabric.operations.get = get
fabric.operations.run = run
fabric.operations.local = local
fabric.operations.open_shell = open_shell

# context_managers
#cd, hide, settings, show, path, prefix,
#    lcd, quiet, warn_only, remote_tunnel, shell_env
fabric.api.cd = cd
fabric.api.lcd = lcd
fabric.api.path = path
fabric.context_managers.cd = cd
fabric.context_managers.lcd = lcd
fabric.context_managers.path = path

# contrib
fabric.contrib.project.rsync_project = rsync_project
