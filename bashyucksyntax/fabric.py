from fabric.api import env

if env.dry_run:
    
    from contextlib import contextmanager
    from fablib.utils import print_login
    from os import getcwd, sep
    
    __all__ = ('run', 'sudo', 'local', 'cd', 'rsync_project', 'put')
    
    print ""
    print "#! /bin/sh"
    
    env.print_login = True
        
    @print_login
    def sudo(command, shell=True, user=None, pty=False):
        "fake sudo command that only prints the sudo command"
        if user:
            print "sudo -u {0} {1}".format(user, command)
        else:
            print "sudo {0}".format(command)

    
    @print_login
    def run(command, shell=True, pty=False):
        "Fake run command that only prints the command"
        print command

    
    def local(command, capture=True):
        "Fake local command that only print the command"
        print command

    
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
        
        
    def put(local_path, remote_path, mode=None):
        "Fake put function that only prints the scp command"
        print "scp {0} {1}@{2}:{3}".format(local_path, env.user, env.host_string, remote_path)

    
    # mokey patch fabric and fablib to use the dummy operations
    import fabric.operations
    import fabric.api
    import fabric.context_managers
    import fabric.contrib.project
    import fablib.task
    
    fabric.operations.sudo = sudo
    fabric.api.sudo = sudo
    fablib.task.sudo = sudo
    
    fabric.operations.run = run
    fabric.api.run = run
    fablib.task.run = run
    
    fabric.api.cd = cd
    fablib.task.cd = cd
    fabric.context_managers.cd = cd

    fabric.operations.put = put
    fabric.api.put = put
    fablib.task.put = put
    fablib.task.helpers.put = put

    fabric.contrib.project.rsync_project = rsync_project
    fablib.task.rsync_project = rsync_project
    
    fabric.operations.local = local
    fabric.api.local = local
    fablib.task.local = local
    
    # fabric.operations.
    # fabric.api. 
    # fablib.task.