[toc]

# beatsaber 配置说明

## 总结构
+ 一首歌曲及其谱面会统一放在一个文件夹下面，多首歌曲对应多个不同的文件夹，类似如下的结构：
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/allFiles.png)
	+ 每个文件夹下面主要有4类型文件：
	+ **Info文件**
		+ 这个文件的文件名一定是“Info”，包含文件夹内这首歌的基础信息，读取的音乐文件，使用的封面图、以及不同模式、难度调用的Difficulty文件是哪个，等等
	+ **Difficulty文件**
		+ 文件名没有具体规则，被同文件夹中的Info文件中指定文件名调用，内容是具体某个难度的灯光设计、谱面
	+ **音乐文件**
		+ .ogg .mp3 
	+ 歌曲封面图
+ 整体结构图
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/inZipFile.png)
## info文件
+ file ./musicFile/info.dat
+ Info文件的常用结构如下
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/info.dat.png)

## difficult文件
+ file: ./musicFile/HardStandard.dat
+  _notes 数据说明
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/notes.png)
+ _events 数据说明
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/event0.png)
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/event1.png)
+ _obstacles 数据说明
	+ ![image](https://github.com/callmechiefdom/BeatsaberMapsAnalysis/blob/main/IMG/obstacles.png)
