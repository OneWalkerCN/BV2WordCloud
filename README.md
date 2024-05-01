# BV2WordCloud
## 简介
通过b站视频BV查询弹幕，生成弹幕词云

## 使用
+ 在根目录新建“customDict.txt”,放置自定义词组（一个词一行），避免有些专项词组被切分。
+ 找一个字体文件，重命名为Font,放置在根目录下。
+ 在main函数调用`bv_2_wordcloud()`,参数为视频BV号。
+ 完成生成会自动展示图云以及保存到根目录`/Pics`目录下。

## 示例

![CommentCloud_BV1QH4y1N7FH_1714556518 620157](https://github.com/OneWalkerCN/BV2WordCloud/assets/39230719/9bbf064d-8d16-44db-aa34-74d2199795a1)
