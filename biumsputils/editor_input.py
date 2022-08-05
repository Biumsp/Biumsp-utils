import os, tempfile, subprocess
from biumsputils.fatal_error import fatal_error

def editor_input(initial_message=''):

    EDITOR = os.environ.get('EDITOR','vim')
    initial_message = initial_message.encode()

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        tf.flush()
        subprocess.call([EDITOR, tf.name])

        tf.seek(0)
        message = tf.read()

    message = message.decode("utf-8")
    message = message.splitlines()
    message = [l for l in message if not l.startswith('#')]
    message = '\n'.join(message)

    if not message.replace('\n','').replace(' ', ''):
        fatal_error('message cannot be empty')
    
    return message

