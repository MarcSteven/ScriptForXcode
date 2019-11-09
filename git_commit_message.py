#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Marc Steven in 2016/3/20

import sys, re

#Required parts 
requiredRegex = "[A-Z]{2,}-\\d+"
requiredLength = 15

#Get the commit file
commitMessageFile = open(sys.argv[1]) #The first argument is the file
commitMessage = commitMessageFile.read().strip()

if len(commitMessage) < requiredLength:
    print "Commit message is less than the required 15 characters."
    sys.exit(1)
    
if re.search(requiredRegex, commitMessage) is not None:
    print "A JIRA issue must be linked with a commit"
    sys.exit(1)

print "Commit message is validated"
sys.exit(0)
