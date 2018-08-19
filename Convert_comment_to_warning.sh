#!/bin/sh

#  Convert_comment_to_warning.sh
#  Memory chain#
#  Created by Marc Zhao on 2018/8/18.
#  Copyright © 2018年 Marc Zhao. All rights reserved.

KEYWORDS = "TODO:|FIXME:|\?\?\?:\!\!\!:"
find "${SRCROOT}" \( -name "*.h" - or -name "*.m"\) -print0 | xargs -0 egrep
--with-filename --line-number --only-matching "($KEYWORDS).*\$" | perl -p -e
"s/($KEYWORDS)/warning:\$1/"
