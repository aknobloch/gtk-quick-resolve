# GTK Quick Resolve
This application creates a GTK tray icon to quickly run scripts in Ubuntu.   

The tray icon and menu looks like this:    
![Example Image](https://i.imgur.com/zxN6SL2.png)

## Running on Startup
To start the tray icon on system startup, find the "Startup Application Preferences" and add a new entry. The command to use will be `python /path/to/gtk-quick-resolve/main.py &`. After saving, the tray icon should be present on startup.
