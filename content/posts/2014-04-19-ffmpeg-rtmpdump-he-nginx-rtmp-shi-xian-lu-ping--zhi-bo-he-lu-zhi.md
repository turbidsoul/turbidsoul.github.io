Title: ffmpeg,rtmpdump和nginx rtmp实现录屏，直播和录制
Category: RTMP
Tags: ffmpeg, rtmp, rtmpdump, nginx

公司最近在做视频直播的项目，我这里分配到对直播的视频进行录制，录制的方式是通过rtmpdump对rtmp的视频流进行录制

## 前置的知识 ##

* [ffmpeg](http://ffmpeg.org/ffmpeg.html): 用于实现把录屏工具发出的视频和音频流，转换成我们需要的格式，然后发送到rtmp中转服务器上。
* [rtmpdump](http://rtmpdump.mplayerhq.hu/): 用于实现视频的录制，从rtmp的中转服务器接受到视频流，并把视频流保存成flv文件
* [nginx-rtmp-module](https://github.com/arut/nginx-rtmp-module):  用户rtmp中转服务，虽然他可以做很多功能，但是我这里只是使用了这一个
* [screen capture](https://github.com/rdp/screen-capture-recorder-to-video-windows-free): windows下的开源屏幕录制工具

首先，我们安装ffmpeg, rtmpdump和nginx-rtmp-module:

这里我使用的[ffmpeg](http://ffmpeg.zeranoe.com/builds/)和[rtmpdump](http://rtmpdump.mplayerhq.hu/download/rtmpdump-2.4-git-010913-windows.zip)都是windows版的，虽然和linux下的有所区别，但是在这里并没有使用到这些区别。

nginx是在windows下的虚拟机中的linux下编译的，因为windows编译这玩意是在太麻烦了，我实在不想编译第二次。

## ffmpeg 的简单使用 ##

首先我们需要查看以下我们的自己上的设备信息，使用下面的命令:

```
ffmpeg -list_devices true -f dshow -i dummy
```
输出如下结果：
```rconsole
ffmpeg version N-63013-g4cdea92 Copyright (c) 2000-2014 the FFmpeg developers
  built on May  6 2014 22:09:20 with gcc 4.8.2 (GCC)
  configuration: --enable-gpl --enable-version3 --disable-w32threads --enable-avisynth --enable-bzlib --enable-fontconfig --enable-frei0r --enable-gnutls --enable-iconv --enable-libass --enable-libbluray --enable-libcaca --enable-libfreetype --enable-libgsm --enable-libilbc --enable-libmodplug --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libopus --enable-librtmp --enable-libschroedinger --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvo-aacenc --enable-libvo-amrwbenc --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libx264 --enable-libx265 --enable-libxavs --enable-libxvid --enable-decklink --enable-zlib
  libavutil      52. 81.100 / 52. 81.100
  libavcodec     55. 60.103 / 55. 60.103
  libavformat    55. 37.102 / 55. 37.102
  libavdevice    55. 13.101 / 55. 13.101
  libavfilter     4.  5.100 /  4.  5.100
  libswscale      2.  6.100 /  2.  6.100
  libswresample   0. 18.100 /  0. 18.100
  libpostproc    52.  3.100 / 52.  3.100
[dshow @ 00000000029f0e20] DirectShow video devices
[dshow @ 00000000029f0e20]  "screen-capture-recorder"
[dshow @ 00000000029f0e20] DirectShow audio devices
[dshow @ 00000000029f0e20]  "FrontMic (Realtek High Definiti"
[dshow @ 00000000029f0e20]  "virtual-audio-capturer"
[dshow @ 00000000029f0e20]  "Realtek Digital Input (Realtek "
dummy: Immediate exit requested
```

DirectShow video devices下面的是视频设备，DirectShow audio devices是音频设备，ffmpeg录制就需要从这些设备上得到视频和音频的流.

下面我们看以下ffmpeg如果从这些设备中录制视频。

```
ffmpeg -f dshow -i video="screen-capture-recorder":audio="FrontMic (Realtek High Definiti" -f flv test.flv
```

这杨就可以把录屏和通过麦克风说话的声音都录下来，保存成flv，当然这里也可以使用更加丰富的参数来调整视频，使视频更清醒，声音也更响亮，不过这些都不在本文的讨论范围，所以就不在这里多少，有兴趣的华可以去[http://ffmpeg.org/documentation.html](http://ffmpeg.org/documentation.html)上详细的查看。

