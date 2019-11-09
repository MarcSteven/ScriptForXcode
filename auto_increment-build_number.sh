#!/bin/sh

#  auto_increment_build_number.sh
#  MemoryChain
#
#  Created by Marc Zhao on 2018/8/19.
#  Copyright © 2018年 Memory Chain technology(China) co,LTD. All rights reserved.

if [$CONFIGURATON == Release]; then
echo "Bumping build number..."
plist = ${(PROJECT_DIR)}/${INFOPLIST_FILE}

# increment the build number (for instance from 115 to 116)
buildNumber = $(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" "${plist}")
if[["${builNumber}" == ""]]; then
echo "$plist 中没有build版本号."
exit 2

fi

buildNumber = $(expr $buildNumber + 1)
/usr/libexec/Plistbuddy -c "Set CFBundleVersion $buildNumber" "${plist}"
echo "Build版本号升至：$buildNumber."

else
echo $CONFIGURATION "Build版本号没有变化."
fi
