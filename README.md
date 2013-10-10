sqlmapchik
==========

sqlmapchik is a cross-platform sqlmap GUI for popular sqlmap tool.
It is primarily aimed to be used on mobile devices (currently Android is supported).


Screenshots
----

![main menu](https://raw.github.com/muodov/sqlmapchik/master/screens/mainmenu.png)
![target](https://raw.github.com/muodov/sqlmapchik/master/screens/target.png)
![mainlog](https://raw.github.com/muodov/sqlmapchik/master/screens/log.png)
![settings](https://raw.github.com/muodov/sqlmapchik/master/screens/settings.png)


Installation (easy)
----

The easiest way to install sqlmapchik on Android device is to download it from Google Play...when I publish it :). I hope I'll do this by next week.
Note that Google Play version may not include the latest available sqlmap version.

Installation (hacky)
----

To run sqlmapchik on desktop machine or to build a cutting-edge version of APK:

1. git-clone sqlmapchik repository
2. cd to sqlmapchik directory
3. git-clone sqlmap
4. install [kivy](http://kivy.org/#download)
5. you should be able to run sqlmapchik with ```python main.py```

To run sqlmapchik on Android you have two options:

1. build an APK using [these](http://kivy.org/docs/guide/packaging-android.html) instructions. There is a script ```android_build.sh``` that may help.
   Don't forget to comment the following lines in ```blacklist.txt``` in your python-for-android distribution folder:

   ```
   # unittest/*
   # sqlite3/*
   # lib-dynload/_sqlite3.so
   # lib-dynload/_lsprof.so
   # lib-dynload/future_builtins.so
   ```

2. use a nice [Kivy Launcher](https://play.google.com/store/apps/details?id=org.kivy.pygame).
In this case you just need to copy the project directory to /sdcard/kivy/ on your mobile device.

Unsupported features
----

Project is currently in beta (I suppose it will always be as sqlmap is constantly evolving :).
At this point, not all of sqlmap features are supported. Here is what doesn't work for sure:

* sqlmap API
* profiling
* log colorizing
* beeping :)
* user-defined function injection
* updating
* metasploit integration
* multithreading (currently working on it)

Other features _should_ work. If you find an issue (I bet you will:), don't hesitate to report it on Github, by email, Twitter, pidgin mail etc.

Links
----

* sqlmap homepage: http://sqlmap.org
* my twitter: [@muodov](https://twitter.com/muodov)
* And, surely, you can [![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=L5B7EALA4JRU4)
