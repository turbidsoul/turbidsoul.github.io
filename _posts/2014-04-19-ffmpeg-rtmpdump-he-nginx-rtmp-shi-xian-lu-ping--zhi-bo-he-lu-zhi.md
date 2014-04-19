---
layout: post
title: "ffmpeg,rtmpdump和nginx rtmp实现录屏，直播和录制"
description: "ffmpeg,rtmpdump和nginx rtmp实现录屏，直播和录制"
category: RTMP
tags: [ffmpeg, rtmp, rtmpdump, nginx]
published: false
---

公司最近在做视频直播的项目，我这里分配到对直播的视频进行录制，录制的方式是通过rtmpdump对rtmp的视频流进行录制

## 前置的知识 ##

* ffmpeg: [http://ffmpeg.org/ffmpeg.html](http://ffmpeg.org/ffmpeg.html)
