import bpy
import os
import re
from time import sleep
import subprocess
import sys
from contextlib import contextmanager
import logging

log = logging.getLogger('bpy.ops.import_mesh.bmd.maxH')

IDE = False  # is changed by test launcher


@contextmanager
def stdout_redirected(to=os.devnull):
    '''
    # curtesy of https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python#4675744
    import os

    with stdout_redirected(to=filename):
        print("from Python")
        os.system("echo non-Python applications are also supported")
    '''
    fd = sys.stdout.fileno()

    ##### assert that Python and C stdio write using the same file descriptor
    ####assert libc.fileno(ctypes.c_void_p.in_dll(libc, "stdout")) == fd == 1

    def _redirect_stdout(to):
        sys.stdout.close()  # + implicit flush()
        os.dup2(to.fileno(), fd)  # fd writes to 'to' file
        sys.stdout = os.fdopen(fd, 'w')  # Python writes to fd

    with os.fdopen(os.dup(fd), 'w') as old_stdout:
        with open(to, 'w') as file:
            _redirect_stdout(to=file)
        try:
            yield  # allow code to be run with the redirected stdout
        finally:
            _redirect_stdout(to=old_stdout)  # restore stdout.
                                             # buffering and flags such as
                                             # CLOEXEC may be different


@contextmanager
def active_object(obj):
    act_bk = bpy.context.scene.objects.active
    bpy.context.scene.objects.active = obj
    try:
        yield  # run some code
    finally:
        bpy.context.scene.objects.active = act_bk


def MessageBox(string):
    log.warning(string)
    if IDE:
        input('press any key to continue')
        return
    #drawer = (lambda obj, context: obj.layout.label(string))
    #bpy.context.window_manager.popup_menu(drawer, 'message box', icon='ERROR')
    #sleep(5)


def ReverseArray(inputArray):
    i = 0
    rev = []
    i = len(inputArray)
    while i > 0:
        rev.append(inputArray[i-1])  # corrected!
        i -= 1
    # -- inputArray = rev doesn't work
    return rev


def dict_get_set(dct, key, default):
    if key not in dct.keys():
        dct[key] = default
    return dct[key]


def HiddenDOSCommand(exefile, args, startpath=os.getcwd()):
    # this is the function to edit to adapt the program for non-windows platforms
    # just add an 'elif' to the  if/else block below, in which `exefile` is adapted
    # (from 'path/to/bmdview' to 'path/to/bmdview.exe' in this example)

    if sys.platform[:3].lower() == "win":  # windows: use EXE
        exefile += '.exe'
    else:
        raise RuntimeError('For now, image extraction only works on windows')

    if not os.path.isabs(exefile):
        exefile = os.path.abspath(startpath + exefile)

    if ' ' in exefile:  # whitespace: quotes needed
        exefile = '"' + exefile + '"'

    args = ['"' + com + '"' for com in args]
    # do not change original data, and add quotes on args

    DosCommand(exefile + ' ' + ' '.join(args))


def DosCommand(cmd):
    temp = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    log.info("subprocess output %s", temp)
    # shell output in bytes


def getFilenamePath(path):
    return os.path.split(path)[0] + os.path.sep


def newfile(name):
    if not getFiles(name):  # if it doesn't exist
        open(name, 'ab').close()  # create file


def getFilenameFile(path):
    dir, file = os.path.split(path)
    file = os.path.splitext(file)[0]
    return file
    # return os.path.join(dir, file)


def getFiles(wc_name):
    # assume wild card is in the last part
    path, file = os.path.split(wc_name)
    returnable = []
    if '*' in path:
        raise ValueError('must implement getFiles better')
    try:
        a, dirs, files = next(os.walk(os.path.normpath(path)))
    except StopIteration:
        return returnable
    for com in files:
        rematcher = wc_name.replace('/', '\\').replace('\\', '\\\\').\
                            replace('.', '\\.').\
                            replace('*', '.*').\
                            replace('(', '\\(').\
                            replace(')', '\\)')
        if re.fullmatch(rematcher, path.replace('/', '\\')+ '\\' + com):
            returnable.append(os.path.join(path, com))
    return returnable
