---
title: BusPirate setup for OSX
tags: tools, embedded, device
date: 2015-09-13
collection: articles
layout: article.html
summary: As I have switched to mac in the past days, I want to set up my BusPirate to be able to communicate with other circuits.
---


On my windows machine I used __Putty__
for this purpose. In mac there is __Zterm__ as an alternative, but I wanted to
use the terminal. __Screen__ is the perfect alternative for this job. The
workflow is the following:

### 1. Find out the serial number of your BusPirate

To be able to communicate your BusPirate you have to know it's serial number.
List the connected devices before you connect your Buspirate with the following
command: `$ ls /dev`

This command will list all the connected devices. Save them somewhere, and then
connect your BusPirate and list the devices again. Find the one that is only
present when you connect your BusPirate to your machine.

There you go, mine was: `tty.usbserial-AD01W63E`

### 2. Connect to your device

Use __screen__ to connect to your BusPirate:

`$ screen /dev/tty.usbserial-AD01W63E 115200 8N1`

The BusPirate console should appear on your terminal. To exit the session press
<kbd>control</kbd>+<kbd>a</kbd> then <kbd>k</kbd> and after the prompt press
<kbd>y</kbd> to kill the screen.

__Screen__ could be weird at first, but there are tons of shortcuts that will
help you. [Screen manual for osx](http://ss64.com/osx/screen.html).

### 3. Make your life easier

Create an alias for the connection by writing into your _~/.bash_profile_
file.

`alias buspirate='screen /dev/tty.usbserial-AD01W63E 115200 8N1'`

Source the modified file or restart the terminal, and type in `buspirate`, and
the BusPirate terminal should open.
