---
layout:     post
title:      电影信息提取哪家强——HuggingChat 7 个模型对比
date:       2024-01-08
tags: [llm, huggingchat]
categories:
- llm
---


作为一个电影爱好者，笔者经常“流窜”于各个影视导航网站，比如
- [低端影视](https://ddys.art)
- [电影后花园](http://www.dydhhy.com/tag/movie)
- [BTNULL](https://www.btnull.org/)
等等。如果能够从这些平台上自动提取电影信息，那么就可以做很多有趣的事情，比如自动化爬虫、电影推荐、电影搜索等。

笔者最关注的一个影视信息网站是[电影后花园](http://www.dydhhy.com/tag/movie)，站长是一个很有勤奋的人，更新速度很快，几条每天都会更新很多电影条目，最新的电影信息也都是第一时间发布。条目里的电影信息也很全面，电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等等，应有尽有。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/dydhhy-kido-demo_20240226_1620.png" width=789pt>
    <figcaption style="text-align:center"> 电影后花园《小孩》条目 </figcaption>
</figure>

更重要的是，电影后花园还提供了 [RSS 订阅](http://www.dydhhy.com/rsslatest.xml)，这样就可以通过 RSS 订阅的方式获取最新的电影信息。

这样，笔者就通过订阅做了一个近期高分影视推荐机器人，每天通过Telegram/Feishu推送最新的高分电影。也结合 cloudflare workers 做了一个高分电影展示页面，每天自动更新。


这里面有一个问题，电影后花园的RSS订阅只提供了电影条目的标题和链接，没有提供电影的详细信息。所以具体信息的提取需要先抓取网页，然后处理html。

之前采用的办法是用Python的requests库抓取网页，然后用BeautifulSoup处理html，提取电影信息。这种方法的缺点是需要自己写很多正则表达式，而且不同网站的html结构不一样，即使是同一个网站，不同的页面也可能有不同的html结构，所以需要针对不同的页面写不同的解析规则。

自从ChatGPT发布以来，笔者的很多工作都优先用 GPT 去做预处理，电影信息提取也不例外。
从HTML网页里解析电影信息本质上是一个文本信息提取的问题，看似一个简单的任务，但实际不是任意一个LLM就能轻松完成的，界面上目前是充斥着各式各样的LLM。
这要求LLM：
1. 理解中文，即使用中文语料训练过；
2. 能够理解网页的结构，能够识别出电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等信息，这是一个非常复杂的任务。
3. 指令对齐，能够理解用户的指令，比如以什么样的格式返回电影信息，返回的电影信息是否包含某些字段等等。

笔者尝试过使用 OpenAI 的 GPT-3.5/GPT-4, Google Gemini, Perplexity.AI API 以及阿里的 QWEN-1.5，这几个基本上是当前业界内对中文支持最强的大模型代表。 GPT、Gemini、QWEN 都能很好的完成任务，但 perpleixty.ai 的模型在中文任务上欠佳，偶尔会生成一些奇怪的结果。综合下来，还是 GPT 效果最好。


难道 Google 最近开源了新模型 [Gemma](https://blog.google/technology/developers/gemma-open-models/)，其中 Gemma-7B 在 7B 及以下开源 LLM 中排行第三 [HuggingFace Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)：

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/gemma-7b-llm-leaderboard_20240226_1633.png" width=789pt>
    <figcaption style="text-align:center"> 7B及以下参数开源 LLM 排行榜 </figcaption>
</figure>



而且已经加入到 HuggingChat 可用模型套餐中，跟 Mixtral-7X8B、Llama-2-70B-chat 等模型一起，成立了开源模型的“七雄会”。这里就来对比一下这七个模型在电影信息提取任务上的表现。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/gemma-7b-llm-leaderboard_20240226_1633.png" width=789pt>
    <figcaption style="text-align:center"> HuggingChat 支持的模型 </figcaption>
</figure>

# 实验

测试主要考虑以下几点：
1. 能否对齐用户的指令，具体的，我们将以 json 格式返回结果， 返回的信息包含电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等字段。
2. 能否正确识别电影信息，是否包含额外字段及信息。

打分规则：
1. 返回数据中包含合法的 json，加 1 分；
2. 返回的 json 中包含电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等字段，各加 1 分；
3. 每个字段的值都是正确的，加 1 分；
4. 有多余字段，减 1 分；
5. 归一化后的总分，即为最终得分。


测试数据集是电影后花园的 RSS 订阅，共 100 条电影信息。数据集已经打包上传到 [GitHub].

测试结果如下：

综合下来可以看到
- mistral 系列的模型在电影信息提取任务上表现最好，得分最高；
- gemma 次之，得分略低；
