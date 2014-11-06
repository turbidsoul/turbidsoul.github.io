Title: ffmpeg,rtmpdump和nginx rtmp实现录屏，直播和录制
Category: RTMP
Tags: ffmpeg, rtmp, rtmpdump, nginx
Summary: 公司最近在做视频直播的项目，我这里分配到对直播的视频进行录制，录制的方式是通过rtmpdump对rtmp的视频流进行录制

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



首先我们需要查看以下我们的自己上的设备信息，在安装了screen capture recorder之后就可以使用下面的命令:

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
ffmpeg -f dshow -i video="screen-capture-recorder":audio="FrontMic (Realtek High Definiti"  test.avi
```

这杨就可以把录屏和通过麦克风说话的声音都录下来，保存成avii，当然这里也可以使用更加丰富的参数来调整视频，使视频更清醒，声音也更响亮，不过这些都不在本文的讨论范围，所以就不在这里多少，有兴趣的华可以去[http://ffmpeg.org/documentation.html](http://ffmpeg.org/documentation.html)上详细的查看。

当然我们是要使用rtmp协议的，所以这里就需要把视频流发送到rtmp服务端去，如下命令:

```
ffmpeg -f dshow -i video="screen-capture-recorder":audio="FrontMic (Realtek High Definiti"  -f flv rtmp://192.168.56.101/live/test
```

这里只说明一点，如果是发送到rtmp协议的话是需要加上`-f flv`这个参数的，如果不加会报错，这样就算是把录制的视频流发送到了rtmp服务端，当然我这里的nginx服务器要配置好并且启动了，否则还是会报错的。

## nginx rtmp module ##

#### 安装 ####

在编译安装模块的时候需要说明一点，如果在 configure的时候出现了openssl的错误，请安装libssl-dev.

ubuntu下： `sudo apt-get install libssl-dev`

```
./configure --prefix=/usr/local/rtmp-nginx --without-http_rewrite_module
make
make install
```

#### 配置 ####

下面是我的配置:

```nginx
rtmp {
    server {
        listen 1935;

        chunk_size 4096;

        application live {
            live on;
        }
    }
}
http {
    server {
        listen      8080;

        location /stat {
            rtmp_stat all;
            rtmp_stat_stylesheet stat.xsl;
        }

        location /stat.xsl {
            root stat;
        }

        location / {
            root /publisher;
        }
    }
}
```

我们只需要加入一个关于rtmp协议的块和在http协议下加入一个server块，用来配置统计星系等，这就是最简单的配置，这样已经快而已完成我们例子中的功能，如果需要更详细的，请查看[NGINX-based Media Streaming Server](https://github.com/arut/nginx-rtmp-module)。


## RTMPDump ##

**RTMPDump** 是一位匈牙利大神在Adobe未公开RTMP协议的条件下，写出了针对RTMP协议的客户端程序。

在这里rtmpdump的使用是很简单的，当然rtmpdump其实也是有一些问题的，我们先来看看如果使用rtmpdump录制视频流

#### 使用 ####

```
rtmpdump -v -m 0 -r rtmp://192.168.56.101/live/test -o test.flv
```

上面的命令就是录制rtmp协议的视频流的命令，下面简单说明一下：

* -v：是说明视频流是一个直播流
* -m：是超时时间，0表示不超时
* -r：表示rtmp的url

rtmpdump的使用就是如此的简单

#### 问题 ####

我在实际的使用过程中遇到了一个疑问，就是当视频的发送端崩溃或者死机，造成视频流中断，再次发送的时候会发送一个新的视频流，但是rtmpdump无法分辨这个新视频流，他会把这个视频流继续添加在文件后面，保存成一个文件而不是一个新的视频文件。相反对于网络中断而视频的发送端没有中断这种问题是可以处理的，不过中间可能会出现画面定在网络中断的那个时间点上，知道网络再次恢复。

不过这个问题是可以通过程序的方式解决的，在python的库中有一个**[flvlib](https://pypi.python.org/pypi/flvlib/0.1.13)**的库可以处理这类问题,请看下面的代码：

```python
def split_flv(f):
    if isinstance(f, str):
        f = open(f, 'rb')
    flv = tags.FLV(f)
    path, ext = os.path.splitext(f.name)
    output_template = path + "_%d" + ext
    input_flv = open(f.name, 'rb')
    output_flv = None
    split_index = 0;
    filelist = []
    for tag in flv.iter_tags():
        if isinstance(tag, tags.ScriptTag) and tag.timestamp == 0:
            if output_flv:
                output_flv.close()
            output_flv = open(output_template % split_index, 'wb')
            filelist.append(output_flv.name)
            split_index += 1
            output_flv.write(tags.create_flv_header(flv.has_audio, flv.has_video))
            output_flv.write(tags.create_script_tag('onMetaData', tag.variable, tag.timestamp))
        elif isinstance(tag, tags.VideoTag):
            input_flv.seek(tag.offset + 11)
            data = input_flv.read(tag.size)
            newtag = tags.create_flv_tag(9, data, tag.timestamp)
            output_flv.write(newtag)
        elif isinstance(tag, tags.AudioTag):
            input_flv.seek(tag.offset + 11)
            data = input_flv.read(tag.size)
            newtag = tags.create_flv_tag(8, data, tag.timestamp)
            output_flv.write(newtag)
    output_flv.close()
    input_flv.close()
    return filelist



def concat_flv(filelist, src_file):
    tempf = tempfile.TemporaryFile('w+b', delete=False)
    tempf.writelines(["file '%s'\n" % f for f in filelist])
    tempf.close()
    curdir = os.path.dirname(__file__)
    cmd = 'ffmpeg'
    if platform.system() == 'Windows':
        cmd = '"' + os.path.join(curdir, 'rtmpdump/ffmpeg.exe') + '"'
    src_file_name, src_file_ext = os.path.splitext(src_file)
    output_file = src_file_name + "_concat" + src_file_ext
    cmd += ' -f concat -i ' + tempf.name + ' -y -c copy ' + output_file
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.communicate()
    logger.info(output[0])
    return (output_file, None)
```

这两段代码就是先把视频分割开，然后在连接到一起生成一个新文件。

## 总结 ##

这是我解决直播的一个测试方案，因为公司的直播系统还没有起来，所以我采用了这样一中思路模拟直播测试我的录制系统。
