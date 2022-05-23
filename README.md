# tools_you_never_needed
Scripts for automating command-line tools to do interesting things.

If a module from the 'site-packages' directory is needed, it can either be
placed in your python path or in the same directory as the script to be run.

There are various dependencies for things sometimes.  If it doesn't work, you
might need: sox, abcm2ps, abcmidi, ghostscript, imagemagick, or something else.

Various 3rd-party python modules, too: termcolor, gtk, pyperclip, maybe some
others.

I wouldn't expect any of this to work on anything but Linux.  ScriptRunner uses
the 'editor' and 'x-terminal-emulator' commands, so I wouldn't expect it to
work on anything other than a Debian-based OS (Debian, Mint, Ubuntu....)
