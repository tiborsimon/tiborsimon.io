---
title: Upload ssh key via Github API
tags: GitHub, API, ssh, bash, deploy
date: 2016-03-19
collection: articles
layout: article.html
snippet: In this article I will show you a way to upload your ssh key to GitHub via the GitHub API. This could be useful for you if you don't like the traditional way of uploading ssh keys.
---


Don't you hate the way you used to upload your ssh keys to GitHub? Generate the key. Copy the public key in somehow. You have to use the mouse. You have to click. :D

Anyway. If you are working on a remote machine, for example one you've just spun up with __vagrant__, tricks with the mouse might not an option for you. Of course, you can copy your already generated and used ssh key to your machine, but this is not the best approach.

# Using the GitHub API

Using the [GitHub v3 API](https://developer.github.com/v3/), we are able to upload our ssh keys via a [HTTP request](https://developer.github.com/v3/users/keys/) by [creating a public key](https://developer.github.com/v3/users/keys/#create-a-public-key).

The following code snippets will use the GitHub API call to upload the named public key to the predefined GitHub account. It also handles the possible error cases:

- authentication error
- key is already uploaded
- connection error

You can copy and paste this script to your machine, modify the `GITHUB_USERNAME` variable, and you are ready to go.

This is the exact method what I used in my __dotfiles__ deployment system. To learn more about that, read the [corresponding article](https://tiborsimon.io/tools/dotfiles-with-url-deployment/).

``` 
GITHUB_USERNAME=tiborsimon
SSH_KEY=$HOME/.ssh/id_rsa

if [ ! -f $SSH_KEY ] || [ ! -f $SSH_KEY.pub ]; then
  echo 'Generate your ssh key first!'
  exit
fi

github_result=0
echo 'How do you want to name the key?'
read -e KEY_NAME
until [ $github_result -eq 1 ]; do
  curl --silent -u "$GITHUB_USERNAME" --data "{\"title\":\"$KEY_NAME\",\"key\":\"$(cat $SSH_KEY.pub)\"}" https://api.github.com/user/keys > gh-result
  if grep -q 'key is already in use' gh-result; then
    github_result=1
    echo 'Key is already in use.'
  elif grep -q '"verified": true' gh-result; then
    github_result=1
    echo "Key ($KEY_NAME) has been added successfully."
  elif grep -q 'Bad credentials' gh-result; then
    echo 'Error during login: invalid username or password!'
    echo 'Try again!'
  else
    echo 'A problem occured during the upload!'
    cat gh-result
    echo 'Try again!'
  fi
  rm gh-result
done
```

# Summary

You were presented to a method that allows you to upload ssh keys to your GitHub account via the command line.

