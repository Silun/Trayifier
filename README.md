# Trayifier
A small windows utility to hide any application's window and create a tray icon for it. Mostly it is meant to tack on a tray icon and minimize-to-tray function to software that doesn't come with that option.

## Installation
Trayifier is strictly a _windows_ utility.  ~~It may be installed via pip: `pip install trayifier`~~

You may also download the compiled executable [here.](https://github.com/Silun/Trayifier/releases/latest/download/Trayify.exe )

## How to Run Trayifier
There are multiple ways to run Trayifier:
- ~~Install Trayifier via pip and execute it via `trayify -f path\to\exe`,~~ either via the terminal or via a script or shortcut. This will also work via `trayify -f path\to\directory\with\one\exe` if there is _exactly one_ executable in that directory other than Trayifier itself.
- Run `trayify` without specifying an executable, Trayifier will check if there is a _single executable_ other than itself in the current working directory and just run that.
- Put the compiled executable into a directory that contains _exactly one_ executable other than Trayifier itself, and run it without any additional arguments. Trayifier will then automatically choose that other executable to run.

If you want the tray icon to be something specific, create an `.ico` file of the same name as the executable you want to run and place it in the same directory, for example: `Run-me.exe` for the executable and `Run-me.ico` for its icon file, located right next to each other. If no icon file is present or it can't be read, Trayifier will attempt to extract an icon from the executable file itself, and if that fails, the standard Python icon will be used instead.

## Behaviour of Trayifier
Trayifier will run the target application and create a tray icon for it. Either double-clicking the icon or right-clicking and then choosing `Toggle` will hide and bring the window up again, respectively. When `Exit` is chosen from the menu, Trayifier will attempt to close the application via a `SIGTERM` signal.

## Known Issues
- It is not currently possible to pass arguments to the trayified application.

## Possible Future Improvements
- Add a mode to bring up a mechanism to choose an already open window to add a tray icon to.
- Detect when the window is getting minimized and offer actual minimize-to-tray functionality.
