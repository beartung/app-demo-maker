#!/bin/bash
gradle build; adb install -r build/apk/demo-maker-android-release.apk; adb shell am start -n com.demo.maker/com.demo.maker.Demo
