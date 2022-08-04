import builtins
from textwrap import TextWrapper


class Print():
    '''
        print function that auto-indents before 
        printing, with custom indent and max width. 
        By default it behaves like the builtin print().
        It also enables color coding.
    '''

    def __init__(self):
        self.level = 0
        self.indent = False
        self.step = '    '
        self.max_width = 130
        self.color = Colorcodes()

    def spaces_step(self):
        self.step = '    '
    
    def lines_step(self):
        self.step = '│   '

    def custom_step(self, step: str):
        assert isinstance(step, str), 'step must be a string'
        self.step = step

    def auto_indent(self):
        self.indent = True

    def no_indent(self):
        self.indent = False

    def up(self):
        self.level += 1
    
    def down(self):
        if self.level > 0: self.level -= 1

    def _color(self, message, color):
        # Return unchanged if color is None (logger's default)
        if not color: return message

        try:
            color = self.color.__getattribute__(color)
            reset = self.color.reset
        except AttributeError as error:
            raise error(f'color {color} is not available')
        except Exception as error:
            raise error

        return color + message + reset
    
    @can_fail_silently(default=True, callback=builtins.print)
    def __call__(self, *args, **kwargs):

        sep = kwargs['sep'] if 'sep' in kwargs else ' '
        message = sep.join(args)

        if self.indent:
            wrapper = TextWrapper(
                initial_indent=self.step*self.level,
                subsequent_indent=self.step*self.level + '├─',
                width=self.max_width)

            message = wrapper.fill(message)

            # Replace the last "new-line" symbol
            message = message[::-1].replace('─├', '─└',1)[::-1]

        # Add coloring
        if 'color' in kwargs:
            message = self._color(message, kwargs['color'])
            del kwargs['color']
