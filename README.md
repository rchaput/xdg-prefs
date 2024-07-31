# XDG-Prefs
> Remy Chaput <rchaput.pro@gmail.com>

On GNU/Linux systems, each file has an associated MIME Type (or Media Type)
that represents the kind of content (for example, *image/jpeg*).
Your system uses a database to list your preferences for default applications
(for example, to use *eog* as default application for *image/jpeg*).

*XDG-Prefs* uses the [XDG Specifications][xdg-spec] to read and modify this
database, allowing you to change your preferred default applications for
each MIME type. The [XDG Specifications][xdg-spec] is the reference 
specification for MIME types and default applications, meaning that the
preferences you will set in *XDG-Prefs* will be recognized by all other
XDG-compliant softwares (such as `xdg-open`, which is typically used when
you double-click on a file).

Usually, Desktop Environments (such as *Gnome*, or *KDE*) provide some kind of
tool to manage these preferences ; this software works on every Window Manager
(including those that are not Desktop Environments, such as *i3wm*).

*Note*: *XDG-Prefs* is not associated with the 
[Freedesktop Organization][freedesktop], and is not an official software of the 
[XDG Specifications][xdg-spec]. 

## Getting started

You may install *XDG-Prefs* by using `pip install git+https://github.com/rchaput/xdg-prefs`
(or `pip install --user git+https://github.com/rchaput/xdg-prefs` if you prefer 
installing for the current user only).
Please note that you must use Python3.6 or later (you might need to replace
`pip` with `pip3` on some distributions, such as Debian).

Alternatively, you can clone this project on your computer and run
 `python setup.py install`. This is recommended if you want to contribute.
Again, you will need to use Python3.6 or later (you might need to replace
`python` with `python3` on some distributions, such as Debian).

This will install the required files and create a `xdg-prefs` executable.

## How to use

Launch `xdg-prefs` (for example from the command line). On the interface you
will see 3 panels (each associated to a tab):
1. **Associations**: allows you to see the current default application for each
MIME Type.
Simply click on the list, on the left of a given MIME Type to see the list
of possible applications. Click on one of them to set it as the default
application.
2. **List MIME Types**: allows you to see the list of known MIME types on your
computer, and to search for specifics MIME types. Even MIME types which do
not have an associated default application are listed here.
3. **List Applications**: allows you to see the list of known applications on
your computer (that is, those with a *.desktop* file). You can see the list
of MIME types each application is able to handle, and a description of the
application.

*XDG-Prefs* will print logs on the bottom of the interface, especially when
you set a new default application.

## Features

* Python implementation of multiples XDG Specifications.  
Directly reads the files that compose each of the following databases:
  * [Shared MIME Database][mime-spec] (list of all MIME types)
  * [Desktop Entry][apps-spec] (list of applications)
  * [MIME Applications Associations][xdg-spec] (preferences for default
  applications)
* Qt5 interface
  * allows to see and filter list of MIME types
  * allows to see and filter list of applications
  * allows to see and change the default application associated to each MIME type
* Works with every window manager

## Dependencies

This project only depends on
* Python3.6 (should work with later versions)
* PySide6 (Qt6 for Python)
* configparser (Python standard library to read config files)
* Uses code from https://github.com/wor/desktop_file_parser
(in order to parse [Desktop files][apps-spec])

## Contributing

This is an Open-Source projects, your contributions are very welcome.

If you have an idea for a new feature, an optimization or if you notice a bug,
feel free to [open an issue][issues].

You are also welcome to contribute to the code directly, in this case please
refer to the [Contributing guidelines][contrib].

## Related projects

Here's a list of other projects related to the [XDG Specifications][xdg-spec]
and/or the setting of default applications on GNU/Linux:

* [PyXDG](https://www.freedesktop.org/wiki/Software/pyxdg/)
* [xdg-utils](https://www.freedesktop.org/wiki/Software/xdg-utils/), including:
  * [xdg-mime](http://portland.freedesktop.org/doc/xdg-mime.html)
  * [xdg-open](http://portland.freedesktop.org/doc/xdg-open.html)
* gnome-default-applications-properties

## Licensing

This project is licensed under the [Apache License][license].

Basically, this means that you are allowed to modify and distribute this
project, but you must include the [License][license] file and state the
changes you've made (please refer to the [License][license] file or the
https://choosealicense.com/licenses/apache-2.0/ website for the full
list of permissions, conditions and limitations).

[issues]:issues/new
[releases]:releases/
[xdg-spec]:https://www.freedesktop.org/wiki/Specifications/mime-apps-spec/
[freedesktop]:https://www.freedesktop.org/wiki/
[mime-spec]:https://www.freedesktop.org/wiki/Specifications/shared-mime-info-spec/
[apps-spec]:https://www.freedesktop.org/wiki/Specifications/desktop-entry-spec/
[contrib]:./CONTRIBUTING
[license]:./LICENSE
