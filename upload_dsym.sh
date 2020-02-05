function printIndroduction {
    echo "Bugly符号表上传工具IOS版 -- dSYM Tool for IOS"
    echo "适用平台 -- Applicable platform: Linux"
    echo "Copyright 2018 calm. All rights reserved."
    echo ""
}

function uploadDsym {
    
    files=`find . -name "*.dSYM"`
    for fileName in $files; do				

        #echo "fileName $fileName"
        # Appid be6f311993
        # Appkey 2ffe1993-0929-4d2e-81cc-a2c34f891993
        # package com.calm.app
        # version(build) 2.2.0(0.4.9)
        java -jar buglySymboliOS.jar -i "$fileName"  -u -id "$appid" -key "$appkey" -package "$bundleId" -version "$version"

    done
}

# main
printIndroduction

#输入app 信息
echo -n "enter the App id: "
read appid 

echo -n "enter the App key: "
read appkey 

echo -n "enter the App bundleId: "
read bundleId 

echo -n "enter the App version: "
read version

echo -n "enter the dsymPath:  "
read path

cd "$path"

# Check the Java Environment
CheckJavaVersion=$(java -version 2>&1)
echo "$CheckJavaVersion" | grep -q "Java(TM)"
if [ $? -ne 0 ]
then
    echo "----"
    echo "系统中未安装Java或者未配置Java环境，请检查！-- Please check if your system has installed Java or configured environment for Java!"
    echo "Java官网 -- Java Web Site：www.java.com"
    exit 1
fi

# Check the jar
#ShellDir=$(cd `dirname $0`; pwd)
pathName=$(cd `dirname $0`; pwd)
JarName="buglySymboliOS.jar"
JarPath="$pathName/$JarName"
if [ ! -f "$JarPath" ]; then
    echo "----"
    echo "未找到\"$JarName\"！-- Can not find \"$JarName\"!"
    echo "请将\"$JarName\"复制到\"$pathName\"中！"
    echo " -- Please copy \"$JarName\" to \"$pathName\"!"
    exit 2
fi 

# call the function to extract upload
uploadDsym $*
