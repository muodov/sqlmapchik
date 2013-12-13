#! /bin/bash

currentdir=`pwd`
#apkname=sqlmapchik-0.9-debug.apk
#rm $apkname
pushd ~/android/python-for-android/dist/default/
rm -rf ./bin/*
./build.py --window --package com.muodov.sqlmapchiktest --name sqlmapchiktest --version 1.2.2 --compile-pyo --dir "$currentdir" --icon "$currentdir/icon.png" --presplash "$currentdir/icon.png" --orientation sensor --permission INTERNET --permission WRITE_EXTERNAL_STORAGE debug installd
popd
#cp "~/android/python-for-android/dist/default/bin/$apkname" ./
