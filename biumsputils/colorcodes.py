import subprocess

class Colorcodes(object):
    """
    Provides ANSI terminal color codes which are gathered via the ``tput``
    utility. That way, they are portable. If there occurs any error with
    ``tput``, all codes are initialized as an empty string.
    The provides fields are listed below.
    Control:
    - bold
    - reset
    Colors:
    - blue
    - green
    - orange
    - red
    :license: MIT
    """
    def __init__(self):
        try:
            self.bold = subprocess.check_output("tput bold".split()).decode("utf-8")
            self.reset = subprocess.check_output("tput sgr0".split()).decode("utf-8")

            self.blue = subprocess.check_output("tput setaf 4".split()).decode("utf-8")
            self.green = subprocess.check_output("tput setaf 2".split()).decode("utf-8")
            self.orange = subprocess.check_output("tput setaf 3".split()).decode("utf-8")
            self.red = subprocess.check_output("tput setaf 1".split()).decode("utf-8")

        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.reset = ""

            self.blue = ""
            self.green = ""
            self.orange = ""
            self.red = ""
