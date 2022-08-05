import functools, inspect


def decorate_class(cls, decorator):
    '''
        Applies the decorator to all methods of a class
    '''

    members = inspect.getmembers(
        cls, lambda x: inspect.isfunction(x) or inspect.ismethod(x))

    for name, funk in members:
        if not (name.startswith('__') and name.endswith('__')):
            setattr(cls, name, decorator(funk))

    return cls


def decorate_module(module, decorator, decorate_classes=True):
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
            setattr(module, name, decorate_class(obj, decorator))

    return module


def lowercase_input(funk):
    
    @functools.wraps(funk)
    def wrapper_lowercase_input(*args, **kwargs):

        nargs = []
        for arg in args:
            if isinstance(arg, str):
                arg = arg.lower()
            
            nargs.append(arg)
        
        nkwargs = {}
        for kwarg, value in kwargs.items():
            if isinstance(value, str):
                value = value.lower()

            nkwargs.update({kwarg: value})
        
        return funk(*nargs, **nkwargs)
    
    return wrapper_lowercase_input


# Deugger decorator
def debugger(logger, cls):
    '''
        Logs when entering in a function and when exiting
            when the level is set to debug, it also prints
            the input arguments and the return value
    '''

    from biumsputils.print import print

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

                logger.debug(f'Entering <{cls}.{funk.__name__}>', color='green')
                logger.io(
                    'Input: {} {}'.format(
                    largs, 
                    lkwargs if lkwargs else ''
                    ), color='orange'
                )

                try: print.up()
                except: pass

                # Calling the function -------------------------

                output = funk(*args, **kwargs)
                return output


            finally:
                try: print.down()
                except: pass

                try: logger.io(f'Output: {str(output)}', color='orange')
                except: pass

                logger.debug(f'Exiting <{cls}.{funk.__name__}>', color='green')

                
        return wrapper_debugger
    return funk_debugger


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

