# Trayify
A small windows utility to hide any application's window and create a tray icon for it. Mostly it is meant to tack on a tray icon and minimize-to-tray function to software that doesn't come with that option.

## Installation
Trayify is strictly a _windows_ utility.  It may be installed via pip: `pip install trayify`

You may also download the compiled executable [here.](https://github.com/Silun/Trayify/releases/latest/download/Trayify.exe )

## How to Run Trayify
There are multiple ways to run Trayify:
- Put the compiled executable into a directory that contains _exactly one_ executable other than Trayify itself, and run it without any additional arguments. Trayify will then automatically choose that other executable to run.
- Run Trayify and pass exactly one argument, which should be the path to the executable which you want to use Trayify on.<br/>Example: `\Path\to\Trayify.exe \Path\to\other\exe`

If you want the tray icon to be something specific, create an `.ico` file of the same name as the executable you want to run in the same directory, for example: `Run-me.exe` for the executable and `Run-me.ico` for its icon file, located right next to each other. If no icon file is present or it can't be read, the standard Python icon will be used instead.

## Behaviour of Trayify
Trayify will run the target application with and create a tray icon in its place. Either double-clicking or right-clicking the icon and then choosing `Toggle` will hide and bring the window up again, respectively. When `Exit` is chosen from the menu, Trayify will attempt to close the application via a `SIGTERM` signal.

## Known Issues
- It is not currently possible to pass arguments to the trayified application.
- It is not currently possible to trayify anything other than an `.exe` file.
- Trayify does not yet close on its own if the trayified process ends.

## Possible Future Improvements
- Currently, Trayify does not attempt to check the target executable itself for icons. For the sake of simplicity, it would be preferable to just extract the first icon and use that for the tray. If I find a simple way to do this, it will probably get added.
- Register trayify as a global command that can be run from anywhere.
- When run without an argument, bring up a mechanism to choose an already open window to add a tray icon to.
- Make trayify live inside its own virtual environment.
- Detect when the window is getting minimized and offer actual minimize-to-tray functionality.
