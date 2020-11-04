#!/bin/bash
# 查找目录及子目录的图片文件(jpg,gif,png)，将大于某值的图片进行压缩处理
# Config
folderPath=$1   # 图片目录路径

maxSize='200'    # 图片尺寸允许值
maxWidth=600   # 图片最大宽度
maxHeight=500  # 图片最大高度
quality=60      # 图片质量


# 压缩处理
# Param $folderPath 图片目录
function compress(){

    folderPath=$1

    if [ -d "$folderPath" ]; then

        for file in $(find "$folderPath" \( -name "*.jpg" -or -name "*.jpeg" -or -name "*.gif" -or -name "*.png" \) -type f -size +"$maxSize" ); do

            echo $file

            # 调用imagemagick resize图片
            $(convert -resize "$maxWidth"x"$maxHeight" "$file" -quality "$quality" -colorspace sRGB "$file")

        done

    else
        echo "$folderPath 不存在"
    fi
}

# 执行compress
compress "$folderPath"

exit 0
