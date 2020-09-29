import ctypes
import sys

def icon_taskbar() -> None:
    """
    Tells windows,that the program running is using Python as a host,
    so that its taskbar icon can be displayed, see: https://bit.ly/3fv9kr7
    """

    if sys.platform == "win32":
        myappid = "abcd"  # arbitrary string

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
