# Trayify
A small windows utility to hide and create a tray icon for any application's window. Mostly it is meant to tack on a tray icon to software that doesn't come with one.

## Installation
Trayify is strictly a _windows_ utility. You may download the compiled executable or use the script inside a Python environment.

In the latter case, install the required modules like so:

`pip install -r requirements.txt`

## How to Run Trayify
There are two ways to run Trayify:
- Put the script or compiled executable into a directory that contains exactly one executable other than Trayify itself, and run it without any additional arguments.
- Run Trayify and pass exactly one argument, which should be the path to the executable which you want to use Trayify on.<br/>Example: `\Path\to\Trayify.exe \Path\to\other\exe`

If you want the tray icon to be something specific, create an `.ico` file of the same name as the executable you want to run in the same directory, for example: `Run-me.exe` for the executable and `Run-me.ico` for its icon file, located right next to each other. If no icon file is present or it can't be read, the standard Python icon will be used instead.

## Behaviour of Trayify
Trayify will run the target application with its window hidden, and create a tray icon in its place. Either double-clicking or right-clicking the icon and then choosing `Toggle` will bring up and hide the window, respectively. When `Exit` is chosen from the menu, Trayify will attempt to close the application via a `SIGTERM` signal.

## Known Issues
It is not currently possible to pass arguments to the trayified application.

## Possible Future Improvements
Currently, Trayify does not attempt to check the target executable itself for icons. For the sake of simplicity, it would be preferable to just extract the first icon and use that for the tray. If I find a simple way to do this, it will probably get added.
