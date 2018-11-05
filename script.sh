#!/usr/bin/env bash
img_url=$(curl -v -X POST "http://upload-hack.photolab.me/upload.php" -F file1=@./$1 -F no_resize=1)
template=$(curl -v -X POST "http://api-hack.photolab.me/template_upload.php" -F resources=@./$2)
out_url=$(curl -v -X POST "http://api-hack.photolab.me/template_process.php" -F image_url[1]=${img_url} -F template_name=${template})
echo $out_url