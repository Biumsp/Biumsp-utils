import functools, inspect
from print_indent import Print


# Logger used by some decorators
class Logger():
    '''
        A basic logging system, used by the debugger decorator:
            it uses a custom print function that allows indentation
    '''
    OFF = -1
    DEBUG = 2
    INFO  = 1

    def __init__(self):
        self.state = Logger.OFF
        self.print = Print()

    def set_state_debug(self):
        self.state = Logger.DEBUG

    def set_state_info(self):
        self.state = Logger.INFO

    def set_state_off(self):
        self.state = Logger.OFF                   

    def debug(self, message: str, color=None):
        if self.state >= Logger.DEBUG:
            self.print(message, color)
    
    def info(self, message, color=None):
        if self.state >= Logger.INFO:
            self.print(message, color)


# Deugger decorator
def debugger(logger, cls=__name__):
    '''
        Logs when entering in a function and when exiting
            when the level is set to debug, it also prints
            the input arguments and the return value
    '''

    def funk_debugger(funk):

        @functools.wraps(funk)
        def wrapper_debugger(*args, **kwargs):
            
            try:
                # Clean input arguments for printing -----------

                largs = [str(arg) for arg in args]
                lkwargs = {k: str(v) for k,v in kwargs.items()}

                for i, a in enumerate(largs):
                    a = a.replace('\n', '\\n')
                    largs[i] = a

                for k, v in lkwargs.items():
                    v = v[:-1] if v.endswith('\n') else v
                    lkwargs[k] = v

                largs = ", ".join(largs)

                # Logging --------------------------------------

                logger.info(f'Entering <{cls}.{funk.__name__}>', color='green')
                logger.debug(
                    'Input: {} {}'.format(
                    largs, 
                    lkwargs if lkwargs else ''
                    ), color='orange'
                )

                try: print.up()
                except: pass

                # Calling the function -------------------------

                output = funk(*args, **kwargs)

                # Cleaning the output --------------------------

                out = [str(arg) for arg in output] if output else []

                for i, a in enumerate(out):
                    a = a.replace('\n', '\\n')
                    out[i] = a

                out = ", ".join(out)

                # Logging --------------------------------------

                logger.debug(f'Output: {out}', color='orange')
                
                return output    

            finally:
                try: print.down()
                except: pass
                logger.info(f'Exiting <{cls}.{funk.__name__}>', color='green')
                
        return wrapper_debugger
    return funk_debugger


def decorate_class(cls, decorator, dunder=False):
    '''
        Applies the decorator to all methods of a class
    '''

    members = inspect.getmembers(
        cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x))

    for name, funk in members:
        if dunder or not (name.startswith('__') and name.endswith('__')):
            setattr(cls, name, decorator(funk))

    return cls


def decorate_module(module, decorator, decorate_classes=True, dunder=False):
    '''
        Applies the decorator to all functions of a module:
            if decorate_classes=True, it also decorates
            all methods of all classes of the module
    '''

    for name in dir(module):
        obj = getattr(module, name)

        if inspect.isfunction(obj):
            setattr(module, name, decorator(obj))
        elif inspect.isclass(obj) and decorate_classes:
            setattr(module, name, decorate_class(obj, decorator, dunder))

    return module


def can_fail_silently(default=False, callback=None):
    '''
    Adds the option "fail_silently" to the function:
        if fail_silently=True, any exception in the function
        will be catched and a 'failed' will be returned
    '''

    def funk_can_fail_silently(funk):

        @functools.wraps(funk)
        def wrapper_can_fail_silently(*args, fail_silently=default, **kwargs):

            try: return funk(*args, **kwargs)
            except Exception as e:
                try: 
                    return callback(*args, **kwargs)
                except: 
                    if fail_silently: return 'failed'
                    else: raise e

        return wrapper_can_fail_silently
    return funk_can_fail_silently

