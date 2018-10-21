#!/usr/bin/env bash
img_url=$(curl -v -X POST "http://upload-hack.photolab.me/upload.php" -F file1=@./$1 -F no_resize=1)
out_url=$(curl -v -X POST "http://api-hack.photolab.me/template_process.php" -F image_url[1]=${img_url} -F template_name="E7136FD5-4D98-9354-0184-B940EBAC0ACB")
echo $out_url > out.txt
curl $out_url > "static/middle.jpg"
curr_dir=$(pwd)"/static/middle.jpg"

python post_processing/main.py $curr_dir $(pwd)"/static/result.jpg"

echo $(pwd)"/static/result.jpg" > out.txt