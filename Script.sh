#!/bin/sh

#  Script.sh
#  
#
#  Created by Marc Zhao on 2017/5/7.
#
RAMDISK = "ramdisk"
SIZE = 1024 #size in MB for ramdisk
diskutill erasevolume HFS+ $RAMDISK 'hdiutill attach - nomount ram://$[SIZE *2048]'
