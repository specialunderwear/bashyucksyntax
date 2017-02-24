from fabric.api import env

def print_login(func):
    "A decorator that makes a command print the login command, but only once"

    def wrapper(*args, **kwargs):
        if env.print_login:
            print "ssh {user}@{host_string}".format(**env)
            env.print_login = False
        return func(*args, **kwargs)

    return wrapper
