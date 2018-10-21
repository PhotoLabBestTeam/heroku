#!/usr/bin/env bash
img_url=$(curl -v -X POST "http://upload-hack.photolab.me/upload.php" -F file1=@./$1 -F no_resize=1)
curl -v -X POST "http://api-hack.photolab.me/template_process.php" -F image_url[1]=$img_url -F template_name="E7136FD5-4D98-9354-0184-B940EBAC0ACB" > out.txt