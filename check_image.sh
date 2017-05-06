#!/bin/sh

#  check_image.sh
#  
#
#  Created by Marc Zhao on 2017/4/28.
#

function display_code {
ERROR_LOCATION=$(grep -Ron "\[UIImage imageNamed:\s*@\"$1\"\s*\]" $PROJECT_NAME)
if [[ -z $ERROR_LOCATION ]]; then
ERROR_LOCATION=$(grep -Ron "UIImage(named\:\s*\"$1\"\s*)" $PROJECT_NAME)
fi
ERROR_LOCATION=$(echo $ERROR_LOCATION | cut -d ':' -f 1,2)
echo "$ERROR_LOCATION: error: Missing imageset with name $1"
}

function display_img {
local IMG_LOC=$(find "$PROJECT_NAME" -name "$1.imageset" | sed 's/.xcassets\//.xcassets:.\//')
echo "$IMG_LOC/:: error: No more refs to imageset $1"
}

USED_NAMES=()
#find obj-c [UIImage imageNamed:@""]
USED_NAMES+=($(grep -Ron '\[UIImage imageNamed:\s*@"[^"]*"\s*\]' $PROJECT_NAME | cut -d '"' -f 2 | sort -u))
#find swift UIImage(named "")
USED_NAMES+=($(grep -Ron 'UIImage(named\:\s*"[^"]\{1,\}"\s*)' $PROJECT_NAME | cut -d '"' -f 2 | sort -u))
#find images names in assets
PRESENTED_IMAGES=$(find "$PROJECT_NAME" -name *.imageset | grep -v Pods | /usr/bin/sed -e 's/.*\///' -e 's/\.imageset$//' | sort -u)
EXIT_CODE=0

echo "Missing imageset with name:"
for name in $(comm -23 <(printf '%s' "$USED_NAMES") <(printf '%s' "$PRESENTED_IMAGES")); do
show_code $name
EXIT_CODE=1
done

echo "No more refs to imageset:"
for name in $(comm -13 <(printf '%s' "$USED_NAMES") <(printf '%s' "$PRESENTED_IMAGES")); do
show_img $name
EXIT_CODE=1
done
echo

exit $EXIT_CODE
