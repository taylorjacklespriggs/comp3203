
from subprocess import *

def ls(directory):
    '''Calls ls -l $directory'''
    return check_output(('ls', '-l', directory)).decode("utf-8")

def cd(directory):
    '''Checks if $directory is valid and returns absolute path'''
    return check_output(('readlink', '-f', directory)).decode("utf-8")[:-1]

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

