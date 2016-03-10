# tiborsimon.io-core

This repo contains the compilation environment for my static personal site __tiborsimon.io__.

### Requirements
- python 3.4 or above

### Used technologies
- Python
- Python virtualenv
- Pelican
- Jinja2
- Webpack
- CSS
- Sass
- HTML
- Javascript

To start the compilation, you need to initialize the environment first. Use the appropriate initializer script based on your environment:
```
init-environment-win.bat
init-environment-mac
```

The init script will setup everything you need. When it is finished, it will activate the _virtual environment_ for Pelican what you have to activate by hand if you close the terminal session after the init script.

For this purpose, you can create an alias in your terminal that navigate you to the compilation folder and activate the environment:

```
alias site='cd /path/to/the/compilation/environment && source site-env/bin/activate && clear'
```

### Makefile targets

| target | result |
|:------|:--------|
| `local` | compiles the site for local testing with empty __SITEURL___ | 
| `serve` | starts up a local webserver on the port 8000 |
| `github` | compiles the site for production, commits the site to the production repo, adds it to the super project, and pushes the changes to GitHub. This is the only command that is proprietary for me :) |

### Repo architecture

This repo only contains the compilation environment for the site. It links two further repos, that contains the [content of the site](https://github.com/tiborsimon/tiborsimon.io-content) and the production compiled [site content](https://github.com/tiborsimon/tiborsimon.github.io).

After you cloned this repo, make sure you run this command: 
```
git submodule update --init --recursive
```
