sqlmapchik
==========

sqlmapchik is a cross-platform sqlmap GUI for popular sqlmap tool.
It is primarily aimed to be used on mobile devices (currently Android is supported).


Screenshots
----

![main menu](https://github.com/muodov/sqlmapchik/screens/mainmenu.jpg)
![target](https://github.com/muodov/sqlmapchik/screens/target.jpg)
![mainlog](https://github.com/muodov/sqlmapchik/screens/log.jpg)
![settings](https://github.com/muodov/sqlmapchik/screens/settings.jpg)


Installation (easy)
----

The easiest way to install sqlmapchik on Android device is to [download it from Google Play](http://play.google.com/)
Note that Google Play version may not include the latest available sqlmap version.

Installation (hacky)
----

To run sqlmapchik on the desktop machine or to build the cutting-edge version of APK:

1. git-clone sqlmapchik repository
2. cd to sqlmapchik directory
3. git-clone sqlmap
4. install [kivy](http://kivy.org/#download)
5. you should be able to run sqlmapchik with ```python main.py```
6. to build an APK use [these](http://kivy.org/docs/guide/packaging-android.html) instructions.
   Don't forget to comment the following lines in ```blacklist.txt``` in your python-for-android distribution folder:

   ```
   # unittest/*
   # sqlite3/*
   # lib-dynload/_sqlite3.so
   # lib-dynload/_lsprof.so
   # lib-dynload/future_builtins.so
   ```

Unsupported features
----

Project is currently in beta (I suppose it will always be :).
At this point, not all of sqlmap features are supported. Here is what doesn't work for sure:

* sqlmap API
* profiling
* log colorizing
* beeping :)
* user-defined function injection
* updating

Other features _should_ work. If you face an issue, don't hesitate to report it on Github, by email, Twitter, pidgin mail etc.

Links
----

* sqlmap homepage: http://sqlmap.org
* author's twitter: [@muodov](https://twitter.com/muodov)
