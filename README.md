[toc]
# BeatsaberMapsAnalysis

-----------------
+ beatsaber 谱面数据说明&解析
-----------------

## 配置说明
+ config.md

## 数据解析
+ tools
	+ handleZipFile 解压文件并提取整首歌的音频数据
	+ handleAudioFile 提取需要的音频数据并贴标签
	+ handleJsonFile 合并数据到 out 文件内，供模型学习使用
		+ => datasetAll.json
		+ => malody.txt
+ original_beatmaps 原始谱面zip文件