#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Marc Steven in 2017/10/12

import git
import os
import time
import yaml
import sys
import re
from git import Repo
print os.environ["GIT_BRANCH"]
workspace=os.environ['WORKSPACE']
m = re.search("origin/(.*)", os.environ["GIT_BRANCH"])
if m:
    git_branch = m.group(1)
else:
    sys.exit("COULD NOT LOAD SOURCE BRANCH")
# UPDATE VERSION FILE
with open(workspace + '/deploy_automation/config/int/versions.yaml', 'r') as f:
    versions_yaml = yaml.load(f)
versions_yaml["a.component"] = time.time()
with open(workspace + '/deploy_automation/config/int/versions.yaml', 'w') as f:
    yaml.dump(versions_yaml, f, default_flow_style=False)
# OTHER WAY
git_repo = Repo(workspace + "/deploy_automation")
git_repo.git.status()
git_repo.git.add(workspace + '/deploy_automation/config/int/versions.yaml')
git_repo.git.config('--global', "user.name", "user name")
git_repo.git.config('--global', "user.email", "user@domain.com")
git_repo.git.status()
git_repo.git.commit(m=' DEPLOY SCRIPT Updating versions.yaml for ENV jamestest2 and Service test')
git_repo.git.push('--set-upstream', 'origin', git_branch)
