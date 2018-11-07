#!/usr/bin/env bash
template=$(curl -v -X POST "http://api-hack.photolab.me/template_upload.php" -F resources=@./$2)
out_url=$(curl -v -X POST "http://api-hack.photolab.me/template_process.php" -F image_url[1]=$1 -F template_name=${template})
echo $out_url