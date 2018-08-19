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
Introduction

These are the steps to build a Run-In-Place (RIP) version of LinuxCNC from source. This is the best way to try out the LinuxCNC development branches as it does not effect any installed version of LinuxCNC. RIP also makes it very easy to rebuild LinuxCNC to include any modifications to the source. If you have modified a file, simply run make in the src directory to compile the changes. Only the modified files will be re-compiled, so it should make fast allowing for rapid iteration of changes.
Install git

If you do not already have git, install it by saying

$ sudo apt-get install git
Building LinuxCNC
Get the source code

Open a terminal where you would like to build LinuxCNC. I use ~/sources, to keep things neat, but you can put it wherever you like. Then clone the LinuxCNC repository by saying

$ git clone https://github.com/LinuxCNC/linuxcnc.git linuxcnc-grotius

Then enter the new directory

$ cd linuxcnc-dev

The default branch is master (2.8~pre). To build another branch you have to switch to it. For example, to build current stable (2.7) you would first fetch (download) and then switch to the 2.7 branch by saying

$ git fetch origin 2.7
$ git checkout 2.7
Configure

Next configure how the code should be compiled. You should configure for uspace when compiling for vanilla and Preempt-RT kernels, if you are running an RTAI kernel than use -r instead.

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

$ make -j4   (-j4 = quadcore, -j2 = dual core processor)

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



