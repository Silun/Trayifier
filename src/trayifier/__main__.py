import sys
import subprocess
import argparse
from os import kill, getpid
from signal import SIGTERM

import pywintypes # Only needs to be imported due to a bug in pywin32
# https://stackoverflow.com/questions/3956178/cant-load-pywin32-library-win32gui
from win32gui import EnumWindows, ShowWindow, SetForegroundWindow
from win32process import GetWindowThreadProcessId
from win32com.client import Dispatch

import PySimpleGUIWx as sg
import trayifier
from pathlib import Path
from base64 import b64encode
from icoextract import IconExtractor

"""TODOzeug
-pyinstaller funktional machen für standalone exe
-readme anpassen
-pypi upload
"""

def find_icon(passedPath):
    """Look for an icon file next to the executable and of the same name.
    If none exists, extract one from the executable, and fall back to the standard icon."""
    icon = passedPath.with_suffix('.ico')
    if icon.exists():
        with open(icon, "rb") as image_file:
            icon = b64encode(image_file.read())
    else:
        try:
            ext_icon = IconExtractor(passedPath).get_icon()
            icon = b64encode(ext_icon.getvalue())
        except:
            icon = sg.DEFAULT_BASE64_ICON
    return icon


def start_program(target, visibility):
    """Starts the program with all of its windows hidden or shown based on initial global value."""
    rawtarget = r'{}'.format(target)
    SW_HIDE = visibility
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    p = subprocess.Popen(rawtarget, startupinfo=info)
    return p


def determine_filepath(args):
    """Determine the program executable to trayify by checking for arguments and,
    if none found, a single exe in the same folder."""
    program = None
    if args.filename:
        program = Path(args.filename)
        assert program.exists(), "The specified filename cannot be found."
        
        if program.is_file():
            return program
        elif program.is_dir():
            local_executables = []
            for p in program.glob('*.exe'):
                local_executables.append(p)
            try:
                local_executables.remove(Path(sys.executable))
            except:
                pass
            assert len(local_executables) == 1, "A filepath was specified but there is more than one executable in the working directory. Please specify what exactly you want to trayify."
            return local_executables[0]
        else:
            sys.exit("The specified filename cannot be found.")

    else:
        local_executables = []
        for p in Path.cwd().glob('*.exe'):
            local_executables.append(p)
        try:
            local_executables.remove(Path(sys.executable))
        except:
            pass

        assert len(local_executables) == 1, "No filepath was specified and there is more than one other executable in the working directory. Please specify what exactly you want to trayify."
        return local_executables[0]


def find_window_for_pid(pid):
    """Find all windows associated with the passed PID by iterating through all windows and comparing the associated PIDs."""
    result = []
    def callback(hwnd, _):
        nonlocal result
        ctid, cpid = GetWindowThreadProcessId(hwnd)
        if cpid == pid:
            result.append(hwnd)
    EnumWindows(callback, None)
    return result


def change_visibility(hwndlist, bool):
    """Change the window visibility of the passed list of HWND window handles and push into foreground.
    The function SetForegroundWindow() is buggy in Windows, it can lead to occasional crashes - there are
    added shell commands which are intended to alleviate this issue."""
    for hwnd in hwndlist:
        ShowWindow(hwnd, bool)
        if bool:
            # Send keys to work around an issue in the Windows API.
            try:
                shell.SendKeys('%')
                SetForegroundWindow(hwnd)
                shell.SendKeys('%')
            except Exception as e:
                print("Exception occured on setting window focus. This is a bug in the Windows API.")
                print(e)
    return bool

def start_trayify(args):
    """Starts the program to be trayified, sets up the tray icon and starts the main loop."""
    # Global shell for bug circumvention. It will not do anything worthwhile, it just needs to be there
    global shell

    # Set parameters, start trayified program and remember its PID and visibility
    program_to_trayify = determine_filepath(args)

    if args.visible == None:
        window_is_visible = trayifier._cfg["defaults"]["visibility"]
    else:
        window_is_visible = args.visible

    program_handle = start_program(program_to_trayify, window_is_visible)
    print(f"Starting {program_to_trayify.name} with PID {program_handle.pid}. The window is {(lambda x: 'NOT ' if x == False else '')(window_is_visible)}visible by default. The tray process has PID {getpid()}.")

    # Define tray menu, icon and shell
    menu_def = ['UNUSED', ['Toggle', 'Exit']]
    tray = sg.SystemTray(menu=menu_def, data_base64=find_icon(program_to_trayify))
    shell = Dispatch("WScript.Shell")

    # Main loop
    while True:
        event = tray.read()
        print(event)
        if event == 'Exit':
            # On Exit, attempt to gracefully terminate trayified process and end Trayify
            try:
                kill(program_handle.pid, SIGTERM)
                print(f"Killing {program_to_trayify.name} with PID {program_handle.pid} via SIGTERM ({SIGTERM}).")
            finally:
                break
        elif event in ['Toggle', '__DOUBLE_CLICKED__']:
            # On toggle, find all windows associated with pid at the time, then change visibility
            program_hwndlist = find_window_for_pid(program_handle.pid)
            window_is_visible = change_visibility(
                program_hwndlist, not window_is_visible)
        if program_handle.poll() != None:
            sys.exit(f"The trayified process with PID {program_handle.pid} has ended. Exiting.")


def main():
    parser = argparse.ArgumentParser(prog = 'trayify',
                                    description = "A small windows utility to hide any application's " \
                                        "window and create a tray icon for it. Mostly it is meant to tack " \
                                        "on a tray icon and minimize-to-tray function to software that doesn't " \
                                        "come with that option.",
                                    epilog = 'In order to get debug information printed to the console, use trayifydbg instead of trayify.')
    parser.add_argument("-v", "--version", action='version', version=f'trayifier {trayifier.__version__}')
    parser.add_argument('-f', '--filename', required=False, help="if no filepath is specified, trayify will look for a single executable in the current working directory")
    parser.add_argument('--visible', action=argparse.BooleanOptionalAction,
                        default=None, help="override the default initial window visibility")
    # parser.add_argument('--verbose', action='store_true', help="TBI outputs extra logging information")
    args = parser.parse_args()

    start_trayify(args)

def trayify_from_script(filepath: Path = None, visibility: bool = True):
    "A small windows utility to hide any application's " \
    "window and create a tray icon for it. Mostly it is meant to tack " \
    "on a tray icon and minimize-to-tray function to software that doesn't " \
    "come with that option. Point the filepath argument to a file or a folder containing exactly one executable. " \
    "If no filepath is provided, the current working directory will be used instead. " \
    "Use the visibility argument to override the default visibility on program launch."
    args = argparse.Namespace(
        filename = filepath,
        visible = visibility
    )

    start_trayify(args)

if __name__ == "__main__":
    pass