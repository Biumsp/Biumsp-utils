class ValidationError(Exception): pass

def validate(condition: bool, message: str):
    if not condition: raise ValidationError(message)


def requires(arg, *args):
    '''If you have arg, you need at least one of the args'''

    if not bool(arg):
        return True
    
    return any(bool(a) for a in args)


def excludes(arg, *args):
    '''If you have arg, you cannot have ant of the args'''

    if not bool(arg):
        return True

    return none(*args)


def none(*args):
    '''No one is true'''
    return sum(bool(x) for x in args) == 0
