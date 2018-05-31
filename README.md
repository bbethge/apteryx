# Apteryx
Apteryx is meant to be a graphical package manager based on APT.
It is inspired by [Aptitude][], but specifically a workflow with
Aptitude in which you search the flat package list using the Limit
Display command, then manually select recommended packages before
installation.  Variations, like browsing by category or installing
recommended packages automatically, should be supported, but it
will hopefully end up simpler than Aptitude.

[aptitude]: https://alioth.debian.org/projects/aptitude/

## Prerequisites
You need these Debian packages installed:
* python3
* python3-apt
* python3-gi
* gir1.2-gtk-3.0

To modify the code or translations, you may need:
* python3-babel
