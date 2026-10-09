name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pip build-essential git python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good libunwind-dev libssl-dev libffi-dev libltdl-dev autoconf automake libtool pkg-config cmake unzip

      - name: Install buildozer
        run: |
          pip install buildozer cython==0.29.36

      - name: Accept Android SDK licenses
        run: |
          mkdir -p /home/runner/.buildozer/android/platform/android-sdk/licenses
          echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > /home/runner/.buildozer/android/platform/android-sdk/licenses/android-sdk-license
          echo "84831b9409646a918e30573bab4c9c91346d8abd" > /home/runner/.buildozer/android/platform/android-sdk/licenses/android-sdk-preview-license

      - name: Build APK
        run: |
          yes | buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: hisobkunak-apk
          path: bin/*.apk
