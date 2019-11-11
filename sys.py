#! /bin/python
#created by Marc Steven in 2016/10/20
import json
import sys
import os
import commands
import time

def main():
    print('============ start ===========')
    if len(sys.argv) < 3:
        sys.exit(400)
    crashPath = sys.argv[1]
    print('====> crashPath = %s' % crashPath)
    dysmPath = sys.argv[2]
    print('====> dysmPath = %s' % dysmPath)
    c,d = commands.getstatusoutput('export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer; /Applications/Xcode.app/Contents/SharedFrameworks/DVTFoundation.framework/Versions/A/Resources/symbolicatecrash -v ' + crashPath + ' ' + dysmPath + ' / > output.crash')
    if c == 0:
        print('\r======> success')
    else :
        print('\r======> fail')

def progress_test():
    bar_length=20
    for percent in xrange(0, 100):
        hashes = '#' * int(percent/100.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
        sys.stdout.flush()
        time.sleep(0.05)


main()
