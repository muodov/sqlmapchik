#! /bin/bash

currentdir=`pwd`
apkname=sqlmapchik-0.9-debug.apk
rm $apkname
pushd ~/android/python-for-android/dist/default/
rm -rf ./bin/*
./build.py --package org.muodov.sqlmapchik --name sqlmapchik --version 0.9 --dir "$currentdir" --orientation sensor --permission INTERNET --permission WRITE_EXTERNAL_STORAGE debug installd
popd
cp "~/android/python-for-android/dist/default/bin/$apkname" ./
