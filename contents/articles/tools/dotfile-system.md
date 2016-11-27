---
title: My dotfile system
tags: dotfiles, tools, linux, config, deploy
date: 2016-04-01
collection: articles
layout: article.html
snippet: I hate to be machine dependent. For me a computer is just a tool to get things done. If one breaks down for various reasons or I switch machine I want to have my tools and setup without any manual configuration.
---

Have you ever felt _crippled on a new machine_ you've just logged in for the first time? Tools missing, and if not, they have weird default configurations. Before you can start to work, you need to move in that machine: download all your needed tools, configure them one by one by hand. You quickly realize this is not the best way you can do..

<div class="divider">Solution one</div>

# Externally saved configuration

You can speed up the initial configuration if you have a previously saved config file set in a machine independent storage, say Dropbox or a USB drive.

These files are generally called __dotfiles__, as command line tools often expect their configuration files to start with a dot indicating the file is hidden for normal use. Dotfiles are generally located in the current user's _home_ directory. When you start using a new machine, you simply  copy your saved config files to your home directory and you are home.

Besides the custom configuration files, you can also save out a list of installable programs and tools that you want to have by default on a machine. Some package manager tools supports installing from files, but if not, you can write a small script that will install your tools one by one. You can create a `packages.txt` file for this purpose:

<div class="code-name">packages.txt</div>

``` bash
git
mc
vim
```

The _one-by-one_ installer script could be something like this:

``` bash
for app in $(cat path/to/your/packages.txt); do
  echo "Installing $app.."
  if $YOUR_PACKAGE_MANAGER install -y $app>temp_log_file 2>&1; then
    echo "$app installed."
  else
    echo "$app installation failed! Error: \n$(cat temp_log_file)"
  fi
  rm -f temp_log_file
done
```

You might need to have administrator privileges to install packages on your machine. You have to replace the path to your _packages.txt_ file and your system's package manager.

## Conclusion

This method is semi-manual, as you have to copy the files, and run the commands yourself. It would be much more elegant if you would have a _one-command deployment_ solution. An another big drawback is the lack of version control (unless you have a local git repo on you USB drive). It is always a good idea to use versioning for __anything__ you do in you machine in case of an accident[^1].


<div class="divider">Solution two</div>

# Hosted and versioned configuration

The next improvement step is to put your config files in a version control system, and host it on the internet. If you want a public configuration, you can't find better place than __GitHub__. However, if you want your config to be in a private place, I can suggest using __BitBucket__, as it offers free private repositories. Eihter versioning provider you choose, you will end up having an easy-to-deploy config system. You can clone your setup on a new machine, and you will have your setup ready to use.

There is only one problem with this approach. If you clone your repository into your home directory, then your entire home directory will became a repository, but this is probably not what you want. You can solve this issue by cloning your repo into a separate directory, and then symlink your dotfiles into the expected place.

This is the exact method I use for my dotfile system. I clone my dotfiles repository into the `~/.dotfiles` directory, and then I run my deploy script, that will symlink the dotfiles one-by-one into their dedicated place. Then I only have to modify the dotfiles located in the `~/dotfiles` directory, and my changes automatically appear in place.

For deployment script, I use [Zach Holman's dotfiles](https://github.com/holman/dotfiles) project that has a separated structure that I further customized to meet my needs.

## Conclusion

Putting your dotfiles into a versioned repository and hosting it online gives you amazing flexibility. You can have your own configuration in any machine in minutes while keeping it on a dedicated place. You only need to clone your repository into a dedicated directory, and run your deployment script.

How about one more improvement that will allow you to not just have your configuration on your new machine, but have your your configuration and identity with only a single command?

<div class="divider">Final solution</div>

# Ultimate deployment

Since I have my custom domain name, I felt like there still more room for improvements. My final solution is for my machine independent setup is my __deploy-over-url__ dotfiles system that will:

- recognizes the current system (os x or linux)
- downloads my entire configuration via a specified protocol (https or ssh)
- creates a new ssh key if I need it
- uploads the created or existing ssh key to GitHub and BitBucket
- deploys my downloaded configuration files
- installs the necessary tools to ready to work
- and it does this through a convenient command line menu system

All I have to do is type in the following command:

``` bash
bash <(curl -fsSL tiborsimon.io/dotfiles)
```

I can choose what protocol do I want to use for downloading the configuration. If I choose __https__ the configuration will download instantly, and the ssh key generation will be skipped, since I only need my user name and password for GitHub to push back the config modification I will make later. If I choose __ssh__ for the download protocol, I will be prompted if to create a new ssh key, and optionally upload it ti GitHub or BitBucket.

## Conclusion

In this way I automated all of the critical stepts I do not want to repeate every time on a new machine.

You can find detailed informations about my URL deployment and automated ssh key upload in my dedicated articles:

- [Dotfiles with URL deployment](https://tiborsimon.io/tools/dotfiles-with-url-deployment/)
- [Upload ssh key via Github API](https://tiborsimon.io/programming/upload-ssh-key-via-github-api/)

If you want to take a look at the system itself, you can go to my [dotfiles GitHub repo](https://github.com/tiborsimon/dotfiles).

[^1]: Oh the irony.. Exactly after I typed this sentence my machine froze while traveling home on a bus.. :D Commit often, people! Espacially when you turned off swap file generation in vim :D

