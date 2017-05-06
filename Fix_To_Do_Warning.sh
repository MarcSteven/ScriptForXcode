#!/bin/sh

#  Fix_To_Do_Warning.sh
#  
#
#  Created by Marc Zhao on 2017/5/6.
#
TAGS="TODO:|FIXME:
find "${SRCROOT}" \( -type f -name "*.m" | - name ".swift"\) -print0 | xargs -0 egrep --with-filename --line-number --only-matching "($TAGS).*\$" | perl -p -e "s/($TAGS)/ warning: \$1/"
