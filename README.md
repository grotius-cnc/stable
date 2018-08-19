# DISCLAIMER

**THE AUTHORS OF THIS SOFTWARE ACCEPT ABSOLUTELY NO LIABILITY FOR ANY
HARM OR LOSS RESULTING FROM ITS USE.**

**IT IS _EXTREMELY_ UNWISE TO RELY ON SOFTWARE ALONE FOR SAFETY.**

**Any machinery capable of harming persons must have provisions for
completely removing power from all motors, etc, before persons enter
any danger area.**

**All machinery must be designed to comply with local and national
safety codes, and the authors of this software can not, and do not,
take any responsibility for such compliance.**


This software is released under the GPLv2, with some parts under the LGPL.
See the file COPYING for more details.


# The Build Process


Building LinuxCNC From Source
Kurt Jacobson edited this page on May 30 · 10 revisions
Michel Wijnja edited this page on August 19, 2018, multiple revisions
Introduction

These are the steps to build a Run-In-Place (RIP) version of LinuxCNC from source. This is the best way to try out the LinuxCNC development branches as it does not effect any installed version of LinuxCNC. RIP also makes it very easy to rebuild LinuxCNC to include any modifications to the source. If you have modified a file, simply run make in the src directory to compile the changes. Only the modified files will be re-compiled, so it should make fast allowing for rapid iteration of changes.
Install git

If you do not already have git, install it by saying

$ sudo apt-get install git
Building LinuxCNC
Get the source code

Open a terminal where you would like to build LinuxCNC. I use ~/sources, to keep things neat, but you can put it wherever you like. Then clone the LinuxCNC repository by saying

$ git clone https://github.com/michelwijnja/external_offsets_adaptive_feed.git linuxcnc-grotius

Then enter the new directory

$ cd linuxcnc-grotius
$ cd debian
$ ./configure uspace

Install build dependencies

$ cd ..
$ dpkg-checkbuilddeps

Copy/paste each of the build deps then install with
$ sudo apt-get install <dep-name>

Check deps again
$ dpkg-checkbuilddeps

Repeat until all of the dependencies are installed
Configure

$ cd src
$ ./autogen.sh
$ ./configure
Make

$ make -j2   (-j4 = quadcore, -j2 = dual core processor)

Allow access to hardware
$ sudo make setuid
Running LinuxCNC
Setup the RIP environment

Okey now goto the bin folder of your brand new linuxcnc run in place directory 
and select the file "grotius" mark this file as executable, right mouse click and select option execute as program"

$ . ../scripts/. ./rip-environment   Use this command in terminal :  . ./rip-environment 
You need to run this each time you open a new terminal.
Launch LinuxCNC

$ linuxcnc

LinuxCNC will print the version that is running, check that it is what you expected.

When linuxcnc starts up, goto sim/grotius/grotius_no_home.ini
Make desktop shortcut.

For your g-code post processor :

Your g-code file for usage with this linuxcnc version looks like :

G21 (mm)
M3 (start torch)
G01 x0 y0
G01 x100 y100
m5 (stop torch)

A g-code from inkscape can be used directly !!





