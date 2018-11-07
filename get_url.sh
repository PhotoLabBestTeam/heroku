#!/usr/bin/env bash

echo $(curl -v -X POST "http://upload-hack.photolab.me/upload.php" -F file1=@./$1 -F no_resize=1)