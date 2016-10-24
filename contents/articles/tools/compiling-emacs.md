---
title: Compiling Emacs on CentOS
tags: centos, emacs, compile, make, configure, github
date: 2016-07-15
collection: articles
layout: article.html
snippet: Let's compile Emacs 24.5 for my CentOS based virtual machine that has an older version of it.
---

As I started to use Emacs as my primary text editor (I was a vimmer in the past), I noticed that my common config I created on my OSX machine for Emacs 24.5 doesn't work on one of my Vagrant based virtual machines running CentOS. If I tried to bring up the Helm buffer menu, it brings up an error that the _nesting exceeds `max-lisp-eval-depth'_.

I figured out that the problem was that CentOS only has Emacs 23.1 available via yum, so I needed to compile it from the sources:

First of all, I have downloaded the emacs repository mirror from GitHub, and I checked out to the `emacs-24.5` tag:

``` bash
git clone https://github.com/emacs-mirror/emacs.git
cd emacs
git checkout emacs-24.5
```

Then I run `autogen.sh` which has created the `configure` script.

``` bash
./autogen.sh
```

I run the created `configure` script. As it could have been expected, there was some errors, so I installed the missing packages on demand:

``` bash
./configure
[error] no makeinfo
sudo yum install texinfo

./configure
[error] no x
sudo yum install libX11-devel

./configure
[error] no aw3d
sudo yum install Xaw3d-devel

./configure
[error] no libpng libjpg libgif/libungif libtiff
sudo yum install libjpeg-devel libpng-devel libungif-devel libtiff-devel

./configure
[error] no tputs
sudo yum install ncurses-devel

Where should the build process find the source code?    .
  What compiler should emacs be built with?               gcc -std=gnu99 -g3 -O2
  Should Emacs use the GNU version of malloc?             yes
      (Using Doug Lea's new malloc from the GNU C Library.)
  Should Emacs use a relocating allocator for buffers?    no
  Should Emacs use mmap(2) for buffer allocation?         no
  What window system should Emacs use?                    x11
  What toolkit should Emacs use?                          LUCID
  Where do we find X Windows header files?                Standard dirs
  Where do we find X Windows libraries?                   Standard dirs
  Does Emacs use -lXaw3d?                                 yes
  Does Emacs use -lXpm?                                   yes
  Does Emacs use -ljpeg?                                  yes
  Does Emacs use -ltiff?                                  yes
  Does Emacs use a gif library?                           yes -lgif
  Does Emacs use a png library?                           yes -lpng15 -lz -lm
  Does Emacs use -lrsvg-2?                                no
  Does Emacs use imagemagick?                             no
  Does Emacs support sound?                               yes
  Does Emacs use -lgpm?                                   no
  Does Emacs use -ldbus?                                  no
  Does Emacs use -lgconf?                                 no
  Does Emacs use GSettings?                               no
  Does Emacs use a file notification library?             yes -lglibc (inotify)
  Does Emacs use access control lists?                    no
  Does Emacs use -lselinux?                               no
  Does Emacs use -lgnutls?                                no
  Does Emacs use -lxml2?                                  no
  Does Emacs use -lfreetype?                              no
  Does Emacs use -lm17n-flt?                              no
  Does Emacs use -lotf?                                   no
  Does Emacs use -lxft?                                   no
  Does Emacs directly use zlib?                           yes
  Does Emacs use toolkit scroll bars?                     yes
```

Finally as the `configure` script finished, I compiled the whole software package:

``` bash
make
sudo make install
```

After that, I had a fully functioning Emacs installation, that worked flawlesly with my configuration.

# Summary

You can compile Emacs from sources with the following commands:

``` bash
git clone https://github.com/emacs-mirror/emacs.git
cd emacs
git checkout emacs-24.5
sudo yum install texinfo libX11-devel Xaw3d-devel libjpeg-devel libpng-devel libungif-devel libtiff-devel ncurses-devel
./autogen.sh
./configure
make
sudo make install
```

