#!/usr/bin/env python

import subprocess
import sys

"""Functionality to determine to query the state of a local git repository."""

def git_clean():
    """Return True if all changes have been committed.

    http://stackoverflow.com/questions/2657935/checking-for-a-dirty-index-or-untracked-files-with-git
    """

    # Check for staged but uncomitted changes
    x = subprocess.check_output(['git', 'diff-index', '--cached','HEAD'])
    if x:
        sys.stderr.write("Uncommitted files: %s" % x)
        return False

    # Check for modifications in the working directory
    x = subprocess.check_output(['git', 'diff-files'])
    if x:
        sys.stderr.write("Unstaged files: %s" % x)
        return False

    # Check for untracked files
    x = subprocess.check_output(['git', 'ls-files', '--others'])
    if x:
        sys.stderr.write("Untracked files: %s" % x)
        return False

    return True

def git_current_revision():
    """Return the current git revision.

    Raise an error if the repository is not clean.
    """
    assert git_clean()
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])

if __name__ == '__main__':
    print git_current_revision(),

