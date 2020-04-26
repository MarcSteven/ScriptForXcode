#!/bin/bash

COLOR_ERR="[1;31m"Error Tips
COLOR_SUCC="[0; 32m"# Success Tips
COLOR_QS="[1;37m"Problem Color
COLOR_AW="[0; 37m"
COLOR_END="[1;34m"# color Terminator

# Project Name Finding Project
function searchProjectName () {
  # Depth of maxdepth to find folders
  find . -maxdepth 1 -name "*.xcodeproj"
}

function oclintForProject () {
    # Pre-test the existence of required installation packages
    if which xcodebuild 2>/dev/null; then
        echo 'xcodebuild exist'
    else
        Echo' '
    fi

    if which oclint 2>/dev/null; then
        echo 'oclint exist'
    else
        Echo'(e) You're done, playing oclint but not installing it, what kind of thing are you going to do?
        Echo'(iv) Following the blog: https://github.com/Fantastic LBP/knowledge-kit/blob/master/Part I%20iOS/1.63.md Installation Environment (iv'
    fi
    if which xcpretty 2>/dev/null; then
        echo 'xcpretty exist'
    else
        gem install xcpretty
    fi


    # Specified encoding
    export LANG="zh_CN.UTF-8"
    export LC_COLLATE="zh_CN.UTF-8"
    export LC_CTYPE="zh_CN.UTF-8"
    export LC_MESSAGES="zh_CN.UTF-8"
    export LC_MONETARY="zh_CN.UTF-8"
    export LC_NUMERIC="zh_CN.UTF-8"
    export LC_TIME="zh_CN.UTF-8"
    The installation location of export xcpretty=/usr/local/bin/xcpretty# xcpretty can be found at the terminal with which xcpretty

    searchFunctionName=`searchProjectName`
    path=${searchFunctionName}
    # String replacement function. // Represents global substitution / represents the first result substitution that matches. 
    path=${path//.\//}  # ./BridgeLabiPhone.xcodeproj -> BridgeLabiPhone.xcodeproj
    path=${path//.xcodeproj/} # BridgeLabiPhone.xcodeproj -> BridgeLabiPhone
    
    Myworkspace=$path". xcworkspace" workspace name
    Myscheme=$path scheme name

    # Clear up last compiled data
    if [ -d ./derivedData ]; then
        Echo-e $COLOR_SUCC'- - - Clear the last compiled data derivedData - -'$COLOR_SUCC
        rm -rf ./derivedData
    fi

    # xcodebuild clean
    xcodebuild -scheme $myscheme -workspace $myworkspace clean


    ## Generate compiled data
    xcodebuild -scheme $myscheme -workspace $myworkspace -configuration Debug | xcpretty -r json-compilation-database -o compile_commands.json

    if [ -f ./compile_commands.json ]; then
        Echo-e $COLOR_SUCC'Compiled Data Generated Complete __________________
    else
        Echo-e $COLOR_ERR'Compiled Data Generation Failure ________________ ERR
        return -1
    fi

    # Generating Report
    oclint-json-compilation-database -e Pods -- -report-type html -o oclintReport.html \
    -rc LONG_LINE=200 \
    -disable-rule ShortVariableName \
    -disable-rule ObjCAssignIvarOutsideAccessors \
    -disable-rule AssignIvarOutsideAccessors \
    -max-priority-1=100000 \
    -max-priority-2=100000 \
    -max-priority-3=100000

    if [ -f ./oclintReport.html ]; then
        rm compile_commands.json
        Echo-e $COLOR_SUCC'Completed analysis'$COLOR_SUCC
    else 
        Echo-e $COLOR_ERR'Analysis Failure'$COLOR_ERR
        return -1
    fi
    Echo-e $COLOR_AW'will automatically open the link's analysis result for the uncle'$COLOR_AW'
    # The result of opening oclint with Safari browser
    open -a "/Applications/Safari.app" oclintReport.html
}

oclintForProject
