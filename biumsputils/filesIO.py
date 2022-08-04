from shutil import copyfile
from json import loads as jsonloads
from json import dumps as jsondumps
import os


class InvalidPath(Exception): pass
class RenameError(Exception): pass
class DeleteError(Exception): pass
class MkdirError(Exception): pass
class WriteError(Exception): pass
class ReadError(Exception): pass
class CopyError(Exception): pass


def read(path, loads=False):
    '''Read file safely'''

    try:
        with open(path, 'r') as f:
            r = f.read()
            return jsonloads(r) if loads else r
    except Exception as e:
        raise ReadError(f'unable to read file {path}')


def mkdir(path):
    '''Create directory safely'''

    # Validate input
    if os.path.isdir(path):
        raise InvalidPath(f'directory {path} already exists')

    if os.path.isfile(path):
        raise InvalidPath(f'{path} is a file, not a directory')

    # Make directory
    try: mkdir(path)
    except Exception as e: raise MkdirError(f'cannot create directory {path}')


def write(path, text, dumps=False, override=True):
    '''Write to file safely'''

    # Dump json format
    if dumps: text = jsondumps(text)

    # Validate input
    if not override and os.path.isfile(path):
        raise InvalidPath(f'file {path} already exists')

    # Write tmp file
    tmp_path = path + '.tmp' 
    try:
        with open(tmp_path, 'w') as f:
            f.write(text)
    except Exception as e: raise WriteError(f'unable to write to {tmp_path}')

    # Move tmp file to final file
    rename(tmp_path, path)


def rename(old, new):
    '''Rename files and folders safely'''

    try:
        os.rename(old, new)
    except Exception as e: RenameError(f'unable to move {old} to {new}')


def delete(file):
    ''' Delete files safely'''

    if not os.path.isfile(file):
        raise InvalidPath(f'no file named "{file}" to delete')

    try: os.remove(file)
    except Exception as e: DeleteError(f'cannot remove file {file}')


def copy(old, new):
    '''Copy files safely'''

    try: copyfile(old, new)
    except: CopyError(f'Error: cannot copy {old} to {new}')
