# gitlab2mr

A python script to generate a [myrepos](https://myrepos.branchable.com/) config file from a Gitlab
instance.

You don't want to waste your time checking out all your Gitlab repositories but you are too lazy
to maintain a myrepos config manually. Then this tool is for you.

## Installation

gitlab2mr is available via [pypi](https://pypi.org/project/gitlab2mr/):

```
pip install --user gitlab2mr
```

or better

```
pipx install gitlab2mr
```

## Usage

```
gitlab2mr -u <url-of-your-gitlab-instance> -t <private-access-token> -f ".mrconfig.gitlab"
```