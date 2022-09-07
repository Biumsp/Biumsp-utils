import builtins
from pydoc import pipepager
from textwrap import TextWrapper
from biumsputils.colorcodes import Colorcodes
from biumsputils.decorators import can_fail_silently

class Print():
    '''
        Printing function that auto-indents before 
        printing, with custom indent and max width. 
        By default it behaves like the builtin print().
        It also enables color coding.
    '''
    indent = False
    step = '    '
    level = 0
    max_width = 130
    color = Colorcodes()

    def __init__(self):
        '''
            When you create a new instance, all attributes are resetted
                so it's a good idea to create only one instance, shared
                between all your modules, and to do so after you imported
                all the utilities from biumsputils. 
                This way, the instances created by the utilities will already
                exist when you define your print function, and won't override
                your settings.
        '''
        Print.level = 0
        Print.indent = False
        Print.step = '    '
        Print.max_width = 130
        self.queue = []

    def spaces_step(self):
        Print.step = '    '
    
    def lines_step(self):
        Print.step = '│   '

    def custom_step(self, step: str):
        assert isinstance(step, str), 'step must be a string'
        Print.step = step

    def auto_indent(self):
        Print.indent = True

    def no_indent(self):
        Print.indent = False

    def up(self):
        if Print.indent: Print.level += 1
    
    def down(self):
        if Print.indent and Print.level > 0: Print.level -= 1

    def add(self, *args):
        self.queue.append(args)

    def _color(self, message, color):
        # Return unchanged if color is None (logger's default)
        if not color: return message

        try:
            color = Print.color.__getattribute__(color)
            reset = Print.color.reset
        except AttributeError as error:
            raise error(f'color {color} is not available')
        except Exception as error:
            raise error

        return color + message + reset

    
    def empty(self):
        for q in self.queue:
            self.__call__(q)
            
    
    @can_fail_silently(default=True, callback=builtins.print)
    def __call__(self, *args, color=None, sep=' ', **kwargs):

        message = sep.join(args)

        # Add coloring
        if color:
            message = self._color(message, color)

        if '\n' in message: messages = message.split('\n')
        else: messages = [message]

        if len(messages) > 30 and not Print.indent:
            pipepager('\n'.join(messages), "less -R")

        for message in messages:
            if Print.indent:
                wrapper = TextWrapper(
                    initial_indent=Print.step*Print.level,
                    subsequent_indent=Print.step*Print.level + '├─ ',
                    width=Print.max_width)

                message = wrapper.fill(message)

                # Replace the last "new-line" symbol
                message = message[::-1].replace(' ─├', ' ─└',1)[::-1]

            builtins.print(message, sep=sep, **kwargs)


print = Print()
