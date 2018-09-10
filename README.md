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

# This linuxcnc version is specially designed for parport and mesa driven plasma machine's.

This software is released under the GPLv2, with some parts under the LGPL.
See the file COPYING for more details.

Building LinuxCNC From Source
Kurt Jacobson edited this page on May 30 · 10 revisions
Michel Wijnja edited this page on August 19, 2018, multiple revisions
Introduction

These are the steps to build a Run-In-Place (RIP) version of LinuxCNC from source. This is the best way to try out the LinuxCNC development branches as it does not effect any installed version of LinuxCNC. RIP also makes it very easy to rebuild LinuxCNC to include any modifications to the source. If you have modified a file, simply run make in the src directory to compile the changes. Only the modified files will be re-compiled, so it should make fast allowing for rapid iteration of changes.
Install git

My advise is, install first the 64 bit linuxcnc debian software.
Burn an iso cd. Download the iso here :
http://www.linuxcnc.org/testing-stretch-rtpreempt/
choose the 1.2 or 1.3 gb version, and you are on.

Advise : first update the new installation with synaptic package manager before installing & compiling the 
custom linuxcnc installation. Have fun !!

When installed and updated, search this and remove this with synaptic package manager :
## openssh-server

After brand new install and update's start up a terminal.

$ = only for info. You type in terminal : sudo apt-get install git

P.s. If you want to have root privileges in file explorer you type : sudo thunar

## $ sudo apt-get install git
Building LinuxCNC
Get the source code

Open a terminal where you would like to build LinuxCNC. I use ~/sources, to keep things neat, but you can put it wherever you like. Then clone the LinuxCNC repository by saying

## git clone https://github.com/michelwijnja/external_offsets_adaptive_feed.git linuxcnc-grotius

Then enter the new directory

## cd linuxcnc-grotius
## cd debian
## ./configure uspace

Install build dependencies

## cd ..
## dpkg-checkbuilddeps

Copy/paste each of the build deps then install with
## sudo apt-get install <dep-name>

Check deps again
## dpkg-checkbuilddeps

Repeat until all of the dependencies are installed
Configure

## cd src
## ./autogen.sh
## ./configure
## make -j2   (-j4 = quadcore, -j2 = dual core processor)

Allow access to hardware
## sudo make setuid
Running LinuxCNC
Setup the RIP environment

Okey now goto the bin folder of your brand new linuxcnc run in place directory 
and select the file "grotius.py" 
Rename the file to "grotius" and mark this file as executable, right mouse click and select option execute as program"

Directory ../scripts/. ./rip-environment   
## . ./rip-environment 

You need to run this each time you open a new terminal.
Launch LinuxCNC

## linuxcnc

LinuxCNC will print the version that is running, check that it is what you expected.

When linuxcnc starts up, goto sim/grotius/grotius_no_home.ini
Make desktop shortcut.

For your g-code post processor :

Your g-code file for usage with this linuxcnc version looks like :

# G21 (Units: Metric)
# G40 G90 G64P0.01
# F1 S1
# M52 P1
# M3 (start torch)
# M5 (stop torch)

A g-code from inkscape can be used directly !!
The adaptive feed and the round corners will be added the next github update, then this comment and g-code example
will be modified.

Install xlsxwriter with synaptic package manager, see linuxcnc system menu, this module must be installed 
for loading and writing the plasma excel file based tool lists.

Search the file "grotius" located in the bin directory. Enable this file for execute as program, right mouseclick
and check option's.

To quick enable the machine press F2 (machine on, e-stop reset), F3 (Home all), F1 (Machine off) Esc (Quit linuxcnc)
Keyboard moving axis is working. Keyboard arrows are x and y axis. Page up and down is z axis. Home and End is a axis.
Have Funn !!

To enable the glade-gtk2 editor :

http://www.linuxcnc.org/dists/wheezy/base/

for 32 bit :

http://www.linuxcnc.org/dists/wheezy/base/binary-i386/libgladeui-1-11_3.8.0-0ubuntu6_i386.deb

http://www.linuxcnc.org/dists/wheezy/base/binary-i386/glade-gtk2_3.8.0-0ubuntu6_i386.deb

http://www.linuxcnc.org/dists/wheezy/base/binary-i386/glade-gnome_3.8.0-0ubuntu6_i386.deb

for 64 bit :

http://www.linuxcnc.org/dists/wheezy/base/binary-amd64/libgladeui-1-11_3.8.0-0ubuntu6_amd64.deb

http://www.linuxcnc.org/dists/wheezy/base/binary-amd64/glade-gtk2_3.8.0-0ubuntu6_amd64.deb

http://www.linuxcnc.org/dists/wheezy/base/binary-amd64/glade-gnome_3.8.0-0ubuntu6_amd64.deb

Download and instal the files in terminal like :
sudo dpkg -i libgladeui-1-11_3.8.0-0ubuntu6_amd64.deb
Or install with Synaptic Package Manager





