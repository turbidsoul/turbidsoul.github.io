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

nginx是在windows下的虚拟机中的linux下编译的，因为windows编译这玩意是在太麻烦了，我是在不想编译第二次。
