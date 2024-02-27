---
layout:     post
title:      电影信息提取哪家强——HuggingChat 7 个模型对比
date:       2024-01-08
tags: [llm, huggingchat]
categories:
- llm
---


作为一个电影爱好者，为了跟踪最新的影视作品信息，笔者经常“流窜”于各个影视导航网站，比如
- [低端影视](https://ddys.art)
- [电影后花园](http://www.dydhhy.com/tag/movie)
- [BTNULL](https://www.btnull.org/)
等等。

笔者最常用的一个站点是[电影后花园](http://www.dydhhy.com/tag/movie)，这位站长是一个很勤奋的人，最新影视作品更新速度很快，几乎每天都会上新很多电影条目。而且每条影视提供信息也很全面，电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等等，应有尽有。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/dydhhy-kido-demo_20240226_1620.png" width=789pt>
    <figcaption style="text-align:center"> 电影后花园《小孩》条目 </figcaption>
</figure>

<!-- 很多网站都会提供比较详细的作品信息，如果能够从这些平台上自动提取电影信息，那么就可以做很多有趣的事情，比如自动化爬虫、电影推荐、电影搜索等。 -->

更重要的是，电影后花园还提供了 [RSS 订阅](http://www.dydhhy.com/rsslatest.xml)，这样就可以通过 RSS 订阅的方式获取最新的电影信息。

作为一个热衷于将繁琐的自动化的人，笔者当然不会放过这个“糊一个影视作品定提醒脚本”的机会。
通过 dydhhy.com 提供的 rss url，笔者做了一个近期高分影视推荐机器人，每天通过 Telegram/Feishu 等平台推送最新的高分电影。也结合 cloudflare workers 做了一个高分电影展示页面 [film.atomicstep.org](https://film.atomicstep.org/)，每天自动更新内容。

糊脚本的过程中遇到了一个小问题，就是 dydhhy 的 RSS 订阅只提供了影视标题和条目链接，而具体信息的提取还是需要先抓取网页，然后处理 html 文本。

笔者采用的第一个办法就是上 `requests` + `BeautifulSoup` + `re`：即用Python的requests库抓取网页，然后用BeautifulSoup处理html，再结合一些正则规则去提取电影信息。

这种方法的优点是：**思路简单，只需要写正则表达式**，缺点是**需要写很多正则表达式**。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/regex-too-much_20240227_1007.png" width=556pt>
</figure>

而且从通用性的角度考虑，不同网站的html结构不一样，即使是同一个网站，不同的页面也可能采用不同的层次结构，所以需要针对不同的页面写不同的解析规则。换一个网站这种方法就需要重新写一套正则。

还好，LLM 这两年发展的风生水起。自从ChatGPT发布以来，笔者的很多文本处理工作都会先用 GPT 去做筛选过滤，再人工处理。
电影信息提取也可以这么做，从HTML网页里解析电影信息本质上是一个**文本信息提取**的问题。这是一个很直观的问题，但不是一个简单的任务，实际上很多 LLM 对这个任务都理解不了。

要完成这个任务，就要求LLM：
1. 理解中文，即用中文语料训练过；
2. 能够理解网页的结构，能够识别出电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等信息，这是一个非常复杂的任务。
3. 指令对齐，能够理解用户的指令，比如以什么样的格式返回电影信息，返回的电影信息是否包含某些字段等等。
4. 有信息提取的能力。有很多模型仅针对 `(Q, A)` 问答对做训练，对于信息提取任务并不擅长。

笔者尝试过的 LLM 中，能勉强胜任工作的有 OpenAI 的 GPT-3.5/GPT-4, Google Gemini, Perplexity.AI API 以及阿里的 QWEN-1.5，这几个基本上是当前业界内对中文支持最强的大模型代表。 GPT、Gemini、QWEN 都能很好的完成任务，但 perpleixty.ai 的模型在中文任务上欠佳，偶尔会生成一些奇怪的结果。综合下来，还是 GPT 效果最好。


难得 Google 最近开源了一个新模型 [Gemma](https://blog.google/technology/developers/gemma-open-models/)，这个模型在一系列基准测试中表现非常优秀，其中 Gemma-7B 在 7B 及以下开源 LLM 中排行第三 [HuggingFace Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)：

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/gemma-7b-llm-leaderboard_20240226_1633.png" width=789pt>
    <figcaption style="text-align:center"> 7B及以下参数开源 LLM 排行榜 </figcaption>
</figure>



Gemma-7B 已经加入到 HuggingChat 可用模型套餐中，跟 Mixtral-7X8B、Llama-2-70B-chat 等模型一起，成立了开源模型的“七雄会”。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/huggingchat-models_20240227_1040.png" width=789pt>
    <figcaption style="text-align:center"> HuggingChat 支持的7个开源模型 </figcaption>
</figure>

于是，笔者就有一个想法，要不就对比一下这七位豪杰在电影信息提取任务上的表现？


<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202402/fight_20240227_1050.png" width=345pt>
</figure>


# 实验
遵循科学的原则，笔者先准备一个测试数据集，然后用这个数据集对七个模型进行测试。

[prompt](https://bit.ly/42Vu5G7)

测试主要考虑以下几点：
1. **指令对齐**：能否按用户要求完成任务。具体的，我们要求 LLM 以 `json` 格式返回影视信息，包含电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等字段。
2. **提取能力**：能否正确识别各字段对应的信息。
3. **幻觉**：结果是否包含额外字段及信息，或者生成一些不相关的信息。

## 打分规则
1. 返回数据中包含合法的 json，加 1 分；
2. 返回的 json 中包含电影名、导演、演员、类型、地区、语言、上映时间、评分、简介等字段，各加 1 分；
3. 每个字段的值都是正确的，加 1 分；
4. 有多余字段，减 1 分；
5. 归一化后的总分，即为最终得分。

## 数据
测试数据集是从电影后花园的抽取到近期(2024/02/25) 100 条影视信息，通过 GPT4 预处理，然后人工校验，修正不准确的内容，最终数据集已经打包上传到 [GitHub].

# 结果
测试结果如下：

综合下来可以看到
- mistral 系列的模型在电影信息提取任务上表现最好，得分最高；
- gemma 次之，得分略低；
