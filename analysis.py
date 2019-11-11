#! /bin/python
# cd 到 test 目录执行 python analysis.py BICrashAnalyzeDemo.crash 命令导出foo.crash中可看到符号化的非系统崩溃



# created by Marc Steven in 2016/9/20

import json
import sys
import os
import commands
import time
import re

def main():
    crashPath = sys.argv[1]
    file_object = open(crashPath,'rU')
    outputFile = open('foo.crash',"w")
    result = ''
    findImages = False
    ownImagename = ''
    binaryimage_list = []
    # 备用数据
    hardware = ''
    identifier = ''
    crashReporterKey = ''
    osVersion = ''
    try:
        for line in file_object:
            if findImages == True:
                line = line.strip()
                if not len(line):
                    continue
                if 'EOF' in line:
                    findImages = False
                    continue
                attr_list = line.split()
                binaryimage = BinaryImages(attr_list[0],attr_list[2],attr_list[3],attr_list[4],attr_list[5].strip('<>'),attr_list[6]) 
                binaryimage_list.append(binaryimage)
            if 'Binary Images:' in line:
                findImages = True
            if 'Hardware Model:' in line:
                hardwarelist = line.split(':')
                hardware = hardwarelist[1]
            if 'Incident Identifier:' in line:
                identifierList = line.split(':')
                identifier = identifierList[1]
            if 'CrashReporter Key:' in line:
                reporterList = line.split(':')
                crashReporterKey = reporterList[1]
            if 'OS Version:' in line:
                versionList = line.split(':')
                osVersion = versionList[1]
            if 'Path:' in line:
                pathList = line.split(':')
                ownImagename = os.path.basename(pathList[1]).strip()

    finally:
        print 'Identifier = ' + identifier
        print 'CrashReporter key = ' + crashReporterKey
        print 'hardware = ' + hardware
        print 'osVersion = ' + osVersion
        print 'path name is = ' + ownImagename
        print 'binaryimage_list count = ' + str(len(binaryimage_list))
        findImages = False

    isLastBacktrace = False
    file_object.seek(0, 0)
    try:
        for line in file_object:
            if isLastBacktrace == True:
                isLastBacktrace = False
                trace = line.strip().strip('()')
                trace_list = trace.split()
                index = 0
                for address in trace_list:
                    temp = str(index).ljust(5)
                    analysisResult = anlysisLine(binaryimage_list,address,ownImagename)
                    temp += analysisResult
                    result +=  temp

                    index+=1
            elif findImages:
                result += line
            else :
                infolist = line.split()
                if len(infolist) == 6 and infolist[0].isdigit():
                    temp = infolist[0].ljust(5)
                    analysisResult = anlysisLine(binaryimage_list,infolist[2],ownImagename)
                    temp += analysisResult
                    result +=  temp
                else :
                    result += line
            if 'Last Exception Backtrace:' in line:
                isLastBacktrace = True
            if 'Binary Images:' in line:
                findImages = True
    finally:
        file_object.close()
        outputFile.write(result)
        outputFile.close()

    # print result
def anlysisLine(binaryimage_list,address,ownImagename):
    result = ''
    temp = ''
    for binaryimage in binaryimage_list:
        if binaryimage.betweenAddressInterval(address):
            # print 'find find !!!'
            image_name = binaryimage.imageName
            temp += image_name.ljust(31)
            temp += address
            
            offset = int(address,16) - binaryimage.baseAddress
            # print 'offset = ' + str(offset)
            if binaryimage.arch == 'arm64':
                fileaddress = str(hex(offset  + 0x0000000100000000))
            else :
                fileaddress = str(hex(offset + 0x00004000))
            # print binaryimage.imageName
            if binaryimage.imageName == ownImagename :
                ownresult = owndSYMAnalysis(fileaddress,ownImagename)
                temp += ' ' + ownresult[0] + ' + ' + str(offset) + ' (' + ownresult[1]  + ':' + ownresult[2]  + ')'
                result +=  temp +  ' \n'
            else :
                result +=  temp + ' todo-system-crash + ' + str(offset) + ' \n'
            break
    return result
def owndSYMAnalysis(fileaddress,ownImagename):
    command = 'dwarfdump --lookup ' + fileaddress +' '+ownImagename+'.app.dSYM/Contents/Resources/DWARF/'+ownImagename
    c,d = commands.getstatusoutput(command)
    name = ''
    findSubprogram = False
    fileName = ''
    lineNumber = 's'
    for outputline in d.split('\n'):
        # print outputline
        if 'TAG_subprogram' in outputline:
            findSubprogram = True
        if findSubprogram:
            if 'AT_name' in outputline:
                p = re.compile(r'[(](.*?)[)]', re.S)
                nameList = re.findall(p,outputline)
                name = eval(nameList[0])
                findSubprogram = False
                # print name
        if 'Line table file' in outputline:
            table = outputline.split(':')
            tableFile = table[1].strip()
            infolist = tableFile.split(',')
            info = infolist[0]
            fileNameList = re.findall(r'\'(.*?)\'',info)
            fileName = fileNameList[0]
            lineInfo = info.split('\' ')[1]
            lineNumber = lineInfo.split(' ')[1]
            # print lineNumber
    return [name,fileName,lineNumber]
    
class BinaryImages:
    def __init__(self, baseAddress, endAddress, imageName,arch, uuid, dsymPath):
        self.baseAddress = int(baseAddress,16)
        self.endAddress = int(endAddress,16)
        self.imageName = imageName.strip()
        self.arch = arch
        self.uuid = uuid
        self.dsymPath = dsymPath
        
    def betweenAddressInterval(self, address):
        addressInt = int(address,16)
        return self.baseAddress <= addressInt <= self.endAddress

main()
