#!/bin/sh

FILE_NAME="CacosGPiCASE2_Script.zip"

zip -r $FILE_NAME * -x zip.sh -x media/*
scp "$FILE_NAME" root@recalbox:/tmp/