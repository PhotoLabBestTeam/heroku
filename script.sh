#!/usr/bin/env bash
img_url=$(curl -v -X POST "http://upload-hack.photolab.me/upload.php" -F file1=@./$1 -F no_resize=1)
out_url=$(curl -v -X POST "http://api-hack.photolab.me/template_process.php" -F image_url[1]=${img_url} -F template_name="E7136FD5-4D98-9354-0184-B940EBAC0ACB")
echo $out_url > out.txt
curl $out_url > "static/middle.jpg"
curr_dir="static/middle.jpg"

python post_processing/main.py $curr_dir "./result.jpg"

#echo "static/result.jpg" > out.txt

mask_url=$(curl -v -X POST "http://upload-hack.photolab.me/upload.php" -F file1=@./result.jpg -F no_resize=1)

new_img=$(curl -v -X POST "http://api-hack.photolab.me/photolab_process.php" -F image_url[1]=${out_url}, image_url[1]=${mask_url} -F template_name="A5A9EDED-DD45-49F4-957A-EA81145ED0C5")

echo $new_img > out.txt