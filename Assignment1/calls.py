
from subprocess import *
from os import path

class CallException(Exception): pass

def _catch(func):
    try:
        return func()
    except Exception as e:
        raise CallException(e.args[0])

def ls(directory):
    '''Calls ls -l $directory'''
    return _catch(lambda: check_output(('ls', '-l', directory)).decode("utf-8"))

def absolute_path(path):
    '''returns the absolute path of the argument'''
    return _catch(lambda: check_output(('readlink', '-f', path)).decode("utf-8")[:-1])

def cd(directory):
    '''Checks if $directory is valid and returns absolute path'''
    directory = absolute_path(directory)
    if path.isdir(directory):
        return directory
    raise CallException('%s is not a directory'%directory)

def put(filename, content):
    '''Puts $content into $filename'''
    f = open(filename, 'w+')
    f.write(content)
    f.close()

def get(filename):
    '''Returns the contents of $filename'''
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content


