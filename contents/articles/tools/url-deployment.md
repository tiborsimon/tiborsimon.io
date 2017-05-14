---
title: Dotfiles with URL deployment
tags: dotfiles, tools, hack, deploy, GitHub, config
date: 2016-03-19
collection: articles
layout: article.html
snippet: You can curl down a file and run it as a setup script. Some tech companies use this approach too.
---

I started to improve my __dotfiles__ system with __one command URL deployment__. In this way I can run a single command on a virgin system to deploy my configuration. This method works on OS X as well as any Linux system.

# How does it work?

I use `curl` to download the __bootstrap__ script which will prepare the machine to be able to clone my dotfiles repo, and then it runs the __deploy__ script.

To download a script stored on __GitHub__ you can use the raw file listing. My __bootstrap__ script can be reached via the <a href="https://raw.githubusercontent.com/tiborsimon/dotfiles/master/bootstrap" target="_blank">https://raw.githubusercontent.com/tiborsimon/dotfiles/master/bootstrap</a> link. Notice, that this is not a convenient link to type..

``` bash
curl https://raw.githubusercontent.com/tiborsimon/dotfiles/master/bootstrap
```

I can take care of this problem by having a custom domain, and creating a redirect, I am using __CloudFlare__ as a nameserver and _ssl_ provider, so I can set up a custom __Page Rule__ to redirect the `tiborsimon.io/dotfiles` to the raw script listing.

@[img](1#CloudFlare custom page rule#550#articles/dotfiles/custom-page-forward-rule.png)

In this way, I can type:

``` bash
curl tiborsimon.io/dotfiles
```

# Downloading and executing the script

The script is available for execution. The next step is to use it.

``` bash
sh <(curl -fsSL tiborsimon.io/dotfiles)
```

We can feed the raw sript to `sh`, `bash` or `zsh`. Curl will download the script in a subshell, then it will return the downloaded script, which we will feed to the `sh` in this example.

The flags make sure, curl not corrupt the script during download:

``` bash
-f, --fail          Fail silently (no output at all) on HTTP errors (H)
-s, --silent        Silent mode (don't output anything)
-S, --show-error    Show error. With -s, make curl show errors when they occur
-L, --location      Follow redirects (H)
```

Make sure you have the latest curl on your system, because older curl versions tend to act weird with the _HTTPS_ protocol, and wont be able to connect.

``` bash
[vagrant@localhost ~]$ bash <(curl -fsSLv https://tiborsimon.io/dotfiles)
* About to connect() to tiborsimon.io port 443 (#0)
*   Trying 104.18.43.82... connected
* Connected to tiborsimon.io (104.18.43.82) port 443 (#0)
* Initializing NSS with certpath: sql:/etc/pki/nssdb
*   CAfile: /etc/pki/tls/certs/ca-bundle.crt
  CApath: none
* NSS error -12286
* Closing connection #0
* SSL connect error
curl: (35) SSL connect error
```

# Summary

We can now use our scripts via URL deployment. You can install __Docker__ in this way for example.

