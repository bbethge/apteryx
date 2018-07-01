import unittest

from format_package_description import format_package_description


class TestFormatPackageDescription(unittest.TestCase):
    """
        Most of these tests are pasted from the English Ubuntu package index.
    """

    maxDiff = None

    def test_basic(self):
        self.assertEqual(format_package_description("""\
Bash is an sh-compatible command language interpreter that executes
commands read from the standard input or from a file.  Bash also
incorporates useful features from the Korn and C shells (ksh and csh).
.
Bash is ultimately intended to be a conformant implementation of the
IEEE POSIX Shell and Tools specification (IEEE Working Group 1003.2).
.
The Programmable Completion Code, by Ian Macdonald, is now found in
the bash-completion package."""),
            """\
Bash is an sh-compatible command language interpreter that executes commands read from the standard input or from a file.  Bash also incorporates useful features from the Korn and C shells (ksh and csh).
<span size="xx-small">
</span>\
Bash is ultimately intended to be a conformant implementation of the IEEE POSIX Shell and Tools specification (IEEE Working Group 1003.2).
<span size="xx-small">
</span>\
The Programmable Completion Code, by Ian Macdonald, is now found in the bash-completion package.""")

    def test_at(self):
        self.assertEqual(format_package_description("""\
At and batch read shell commands from standard input
storing them as a job to be scheduled for execution in the
future.
.
Use
 at    to run the job at a specified time
 batch to run the job when system load levels permit"""),
            """\
At and batch read shell commands from standard input storing them as a job to be scheduled for execution in the future.
<span size="xx-small">
</span>\
Use
<tt>at    to run the job at a specified time</tt>
<tt>batch to run the job when system load levels permit</tt>""")

    def test_389_dsgw(self):
        self.assertEqual(format_package_description("""\
389 Directory Server Gateway is a collection of 3 web applications
that run on top of the Administration Server used by the Directory
Server.  These 3 applications are:
.
 - phonebook:
   a simple phonebook application geared towards end users, with simple search
   screens and simple self-service management
 - orgchart:
   an organization chart viewer
 - gateway:
   a more advanced search interface that allows admins to create and edit user
   entries, and allows creation of templates for different types of user and
   group entries"""),
            """\
389 Directory Server Gateway is a collection of 3 web applications that run on top of the Administration Server used by the Directory Server.  These 3 applications are:
<span size="xx-small">
</span>\
\t•\tphonebook: a simple phonebook application geared towards end users, with simple search screens and simple self-service management
\t•\torgchart: an organization chart viewer
\t•\tgateway: a more advanced search interface that allows admins to create and edit user entries, and allows creation of templates for different types of user and group entries""")

    def test_debian_goodies(self):
        """
            This package description has dashes that look like bullet
            points.  We need to treat this as preformatted text since it
            would be too hard to detect this kind of formatting.
        """
        self.assertEqual(format_package_description("""\
These programs are designed to integrate with standard shell tools,
extending them to operate on the Debian packaging system.
.
 dglob  - Generate a list of package names which match a pattern
          [dctrl-tools, apt*, apt-file*, perl*]
 dgrep  - Search all files in specified packages for a regex
          [dctrl-tools, apt-file (both via dglob)]
.
These are also included, because they are useful and don't justify
their own packages:
.
 check-enhancements
            - find packages which enhance installed packages [apt,
               dctrl-tools]
 checkrestart
            - Help to find and restart processes which are using old versions
              of upgraded files (such as libraries) [python3, procps, lsof*]
 debget     - Fetch a .deb for a package in APT's database [apt]
 debman     - Easily view man pages from a binary .deb without extracting
              [man, apt* (via debget)]
 debmany    - Select manpages of installed or uninstalled packages [man |
              sensible-utils, whiptail | dialog | zenity, apt*, konqueror*,
              libgnome2-bin*, xdg-utils*]
 dhomepage  - Open homepage of a package in a web browser [dctrl-tools,
              sensible-utils*, www-browser* | x-www-browser*]
 dman       - Fetch manpages from online manpages.debian.org service [curl,
              man, lsb-release*]
 dpigs      - Show which installed packages occupy the most space
              [dctrl-tools]
 find-dbgsym-packages
            - Get list of dbgsym packages from core dump or PID [dctrl-tools,
              elfutils, libipc-system-simple-perl]
 popbugs    - Display a customized release-critical bug list based on
              packages you use (using popularity-contest data) [python3,
              popularity-contest]
 which-pkg-broke
            - find which package might have broken another [python3, apt]
 which-pkg-broke-build
            - find which package might have broken the build of another
              [python3 (via which-pkg-broke), apt]
.
Package name in brackets denote (non-essential) dependencies of the
scripts. Packages names with an asterisk ("*") denote optional
dependencies, all other are hard dependencies."""),
            """\
These programs are designed to integrate with standard shell tools, extending them to operate on the Debian packaging system.
<span size="xx-small">
</span>\
<tt>dglob  - Generate a list of package names which match a pattern</tt>
<tt>         [dctrl-tools, apt*, apt-file*, perl*]</tt>
<tt>dgrep  - Search all files in specified packages for a regex</tt>
<tt>         [dctrl-tools, apt-file (both via dglob)]</tt>
<span size="xx-small">
</span>\
These are also included, because they are useful and don&apos;t justify their own packages:
<span size="xx-small">
</span>\
<tt>check-enhancements</tt>
<tt>           - find packages which enhance installed packages [apt,</tt>
<tt>              dctrl-tools]</tt>
<tt>checkrestart</tt>
<tt>           - Help to find and restart processes which are using old versions</tt>
<tt>             of upgraded files (such as libraries) [python3, procps, lsof*]</tt>
<tt>debget     - Fetch a .deb for a package in APT&apos;s database [apt]</tt>
<tt>debman     - Easily view man pages from a binary .deb without extracting</tt>
<tt>             [man, apt* (via debget)]</tt>
<tt>debmany    - Select manpages of installed or uninstalled packages [man |</tt>
<tt>             sensible-utils, whiptail | dialog | zenity, apt*, konqueror*,</tt>
<tt>             libgnome2-bin*, xdg-utils*]</tt>
<tt>dhomepage  - Open homepage of a package in a web browser [dctrl-tools,</tt>
<tt>             sensible-utils*, www-browser* | x-www-browser*]</tt>
<tt>dman       - Fetch manpages from online manpages.debian.org service [curl,</tt>
<tt>             man, lsb-release*]</tt>
<tt>dpigs      - Show which installed packages occupy the most space</tt>
<tt>             [dctrl-tools]</tt>
<tt>find-dbgsym-packages</tt>
<tt>           - Get list of dbgsym packages from core dump or PID [dctrl-tools,</tt>
<tt>             elfutils, libipc-system-simple-perl]</tt>
<tt>popbugs    - Display a customized release-critical bug list based on</tt>
<tt>             packages you use (using popularity-contest data) [python3,</tt>
<tt>             popularity-contest]</tt>
<tt>which-pkg-broke</tt>
<tt>           - find which package might have broken another [python3, apt]</tt>
<tt>which-pkg-broke-build</tt>
<tt>           - find which package might have broken the build of another</tt>
<tt>             [python3 (via which-pkg-broke), apt]</tt>
<span size="xx-small">
</span>\
Package name in brackets denote (non-essential) dependencies of the scripts. Packages names with an asterisk (&quot;*&quot;) denote optional dependencies, all other are hard dependencies.""")

    def test_libsort_versions_perl(self):
        """
            This package description shows why we can’t detect numbered lists.
            These lines with numbers must be preformatted.
            On second thought, we just need to look for a space after
            the period.
        """
        self.assertEqual(format_package_description("""\
The Sort::Versions module allows easy sorting (via comparisons) of mixed text
and numeric strings, similar to the complex "version numbers" that many
revision control packages and shared library systems use. For an explanation
of the algorithm, it's easiest to look at these examples:
.
 1.1   <  1.2
 1.1a  <  1.2
 1.1   <  1.1.1
 1.1   <  1.1a
 1.1.a <  1.1a
 1     <  a
 a     <  b
 1     <  2
.
 (special handling for leading zeros)
 0002  <  1
 1.06  <  1.5
.
 (a hyphen binds looser than a period)
 1-1 < 1-2
 1-2 < 1.2"""),
            """\
The Sort::Versions module allows easy sorting (via comparisons) of mixed text and numeric strings, similar to the complex &quot;version numbers&quot; that many revision control packages and shared library systems use. For an explanation of the algorithm, it&apos;s easiest to look at these examples:
<span size="xx-small">
</span>\
<tt>1.1   &lt;  1.2</tt>
<tt>1.1a  &lt;  1.2</tt>
<tt>1.1   &lt;  1.1.1</tt>
<tt>1.1   &lt;  1.1a</tt>
<tt>1.1.a &lt;  1.1a</tt>
<tt>1     &lt;  a</tt>
<tt>a     &lt;  b</tt>
<tt>1     &lt;  2</tt>
<span size="xx-small">
</span>\
<tt>(special handling for leading zeros)</tt>
<tt>0002  &lt;  1</tt>
<tt>1.06  &lt;  1.5</tt>
<span size="xx-small">
</span>\
<tt>(a hyphen binds looser than a period)</tt>
<tt>1-1 &lt; 1-2</tt>
<tt>1-2 &lt; 1.2</tt>""")

    def test_code(self):
        """
            This is a package description with a code snippet.  The code really
            needs to be treated as preformatted.
        """
        self.assertEqual(format_package_description("""\
The parsing module is an alternative approach to creating and
executing simple grammars, vs. the traditional lex/yacc approach, or
the use of regular expressions.  The parsing module provides a
library of classes that client code uses to construct the grammar
directly in Python code.
.
Here's an example:
.
 from pyparsing import Word, alphas
 greet = Word(alphas) + "," + Word(alphas) + "!"
 hello = "Hello, World!"
 print hello, "->", greet.parseString(hello)
.
This package contains the Python 2.7 module."""),
            """\
The parsing module is an alternative approach to creating and executing simple grammars, vs. the traditional lex/yacc approach, or the use of regular expressions.  The parsing module provides a library of classes that client code uses to construct the grammar directly in Python code.
<span size="xx-small">
</span>\
Here&apos;s an example:
<span size="xx-small">
</span>\
<tt>from pyparsing import Word, alphas</tt>
<tt>greet = Word(alphas) + &quot;,&quot; + Word(alphas) + &quot;!&quot;</tt>
<tt>hello = &quot;Hello, World!&quot;</tt>
<tt>print hello, &quot;-&gt;&quot;, greet.parseString(hello)</tt>
<span size="xx-small">
</span>\
This package contains the Python 2.7 module.""")

    def test_libmath_nocarry_perl(self):
        """
            This shows an example where a plus sign looks like a bullet but
            isn’t.  We are able to detect this only because there is just one
            plus sign.  A similar description with multiple examples would cause
            problems.
        """
        self.assertEqual(format_package_description("""\
The perl module Math::NoCarry implememnts no carry arithmetic which
doesn't allow you to carry digits to the next column.  For example,
if you add 8 and 4, you normally expect the answer to be 12, but that
1 digit is a carry.  In no carry arithmetic you can't do that, so the
sum of 8 and 4 is just 2.  In effect, this is addition modulo 10 in
each column. The following example discards all of the carry digits:
.
 1234
 + 5678
 ------
 6802
.
For multiplication, the result of pair-wise multiplication
of digits is the modulo 10 value of their normal, everyday
multiplication."""),
            """\
The perl module Math::NoCarry implememnts no carry arithmetic which doesn&apos;t allow you to carry digits to the next column.  For example, if you add 8 and 4, you normally expect the answer to be 12, but that 1 digit is a carry.  In no carry arithmetic you can&apos;t do that, so the sum of 8 and 4 is just 2.  In effect, this is addition modulo 10 in each column. The following example discards all of the carry digits:
<span size="xx-small">
</span>\
<tt>1234</tt>
<tt>+ 5678</tt>
<tt>------</tt>
<tt>6802</tt>
<span size="xx-small">
</span>\
For multiplication, the result of pair-wise multiplication of digits is the modulo 10 value of their normal, everyday multiplication.""")

    def test_sgml_base(self):
        """
            This uses multiple spaces for each level of indentation.  These
            should be collapsed to one tab for each level.
        """
        self.assertEqual(format_package_description("""\
This package creates the SGML infrastructure directories and provides
SGML catalog file support in compliance with the current Debian SGML
Policy draft:
.
  * infrastructure directories:
     - /etc/sgml
     - /usr/share/sgml/{declaration,dtd,entities,misc,stylesheet}
     - /usr/share/local/sgml/{declaration,dtd,entities,misc,stylesheet}
.
  * update-catalog(8): tool for maintaining the root SGML catalog
    file and the package SGML catalog files in the '/etc/sgml' directory."""),
            """\
This package creates the SGML infrastructure directories and provides SGML catalog file support in compliance with the current Debian SGML Policy draft:
<span size="xx-small">
</span>\
\t•\tinfrastructure directories:
\t\t•\t/etc/sgml
\t\t•\t/usr/share/sgml/{declaration,dtd,entities,misc,stylesheet}
\t\t•\t/usr/share/local/sgml/{declaration,dtd,entities,misc,stylesheet}
<span size="xx-small">
</span>\
\t•\tupdate-catalog(8): tool for maintaining the root SGML catalog file and the package SGML catalog files in the &apos;/etc/sgml&apos; directory.""")

    def test_3_level(self):
        self.assertEqual(format_package_description("""\
mpdcron is a daemon that watches a Music Player Daemon instance for idle
states and execs commands triggered by specific states.
.
 * Uses mpd's idle mode.
 * Calls hooks depending on the event.
 * Sets special environment variables to pass data to the hooks.
 * Optional support for modules via GModule.
 * Included modules:
   - notification
     + uses notify-send to send notifications.
     + can detect repeated songs.
   - scrobbler
     + uses curl to submit songs to Last.fm or Libre.fm
   - stats
     + module saves song data to a sqlite database
     + supports loving, killing, rating and tagging songs, artists,
       albums and genres.
     + tracks play count of songs, artist, albums and genres.
     + implements a simple server protocol for remote clients to
       receive data."""),
            """\
mpdcron is a daemon that watches a Music Player Daemon instance for idle states and execs commands triggered by specific states.
<span size="xx-small">
</span>\
\t•\tUses mpd&apos;s idle mode.
\t•\tCalls hooks depending on the event.
\t•\tSets special environment variables to pass data to the hooks.
\t•\tOptional support for modules via GModule.
\t•\tIncluded modules:
\t\t•\tnotification
\t\t\t•\tuses notify-send to send notifications.
\t\t\t•\tcan detect repeated songs.
\t\t•\tscrobbler
\t\t\t•\tuses curl to submit songs to Last.fm or Libre.fm
\t\t•\tstats
\t\t\t•\tmodule saves song data to a sqlite database
\t\t\t•\tsupports loving, killing, rating and tagging songs, artists, albums and genres.
\t\t\t•\ttracks play count of songs, artist, albums and genres.
\t\t\t•\timplements a simple server protocol for remote clients to receive data.""")

    def test_paje_app(self):
        self.assertEqual(format_package_description("""\
Paje is a graphical tool that displays traces produced during the
execution of multithreaded programs. Other programs can also generate
traces for this tool.
.
Key Features
  * Supports multi threaded programs
     o each thread of the analysed program can be individually displayed,
       or multiple threads can be combined, to reduce screen space usage.
  * Interactivity
     o each entity represented on the screen can be interrogated for
       more information,
     o related entities are highlighted as mouse cursor passes over
       some representation"""),
        """\
Paje is a graphical tool that displays traces produced during the execution of multithreaded programs. Other programs can also generate traces for this tool.
<span size="xx-small">
</span>\
Key Features
\t•\tSupports multi threaded programs
\t\t•\teach thread of the analysed program can be individually displayed, or multiple threads can be combined, to reduce screen space usage.
\t•\tInteractivity
\t\t•\teach entity represented on the screen can be interrogated for more information,
\t\t•\trelated entities are highlighted as mouse cursor passes over some representation""")

if __name__ == '__main__':
    unittest.main()
