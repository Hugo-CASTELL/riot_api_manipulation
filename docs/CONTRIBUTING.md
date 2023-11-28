# Contributing guidelines

# How to contribute: Scheme

# Environnement
To develop on this project, you will need:

- [Python 3.9](https://www.python.org/downloads/)

# [For beginner developers] Clone and install adapted tools

## Install Python

First of all, you will need Python to run scripts.

You will need to download and install at least [Python 3.9](https://www.python.org/downloads/release/python-3913/), that you will find [here](https://www.python.org/downloads/release/python-3913/).

> **__Note :__** Python 3.9.13 is the last version with binaries installer

## Install an IDE or a code oriented text editor

### IDE
As a recommendation, [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/download/?section=windows) does a great job for this project (scroll down for community edition).

### Code oriented text editor 
[VSCode](https://code.visualstudio.com/) or any vi variant ([neovim](https://neovim.io/) with [astronvim](https://astronvim.com/) for example) can do the job with right configuration. 

## Install [Git](https://git-scm.com/)

All the steps are listed on the [git download page](https://git-scm.com/downloads).

## Clone the project

Now that everything is setup, open a terminal (or git bash on Windows) and search for a place, using the command cd, to clone the repository.

Then, clone the repo :

```git
git clone https://github.com/Hugo-CASTELL/riot_api_manipulation.git
```

If you are new to git, you must check [how to use git](https://www.youtube.com/results?search_query=how+to+use+git).

# Start developing

## Before starting to code

On the [issue tracker](https://github.com/Hugo-CASTELL/riot_api_manipulation), create or assign yourself to an issue.

Please, ensure to fill in the __right labels__ and respect the __issue template__.

[Create a branch from develop](https://github.com/Hugo-CASTELL/riot_api_manipulation/branches) and start coding !

## Validation and finally merging your work

Be sure that all the units test are passing successfully using [pytest](https://docs.pytest.org/). 

Then commit and push.

And finally you create a new pull request respecting the __pull request template__.