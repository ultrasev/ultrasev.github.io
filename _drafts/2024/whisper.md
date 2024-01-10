---
layout:     post
title:      OpenAI whisper 使用指南
date:       2024-01-08
tags: [openai, whisper]
categories: 
- llm
---

当我们聊 whisper 时，我们可能在聊两个概念，一是 whisper 开源模型，二是 whisper 付费语音转写服务。这两个概念都是 OpenAI 的产品，前者是开源的，用户可以自己的机器上部署应用，后者是商业化的，可以通过 OpenAI 的 API 来使用，价格是 0.006 美元/每分钟 。




<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202401/lx-openai_20240110_1013.png" width=789pt>
    <figcaption style="text-align:center"> 当我们聊 whisper 时，我们在聊什么 </figcaption>
</figure>


# whisper 开源模型

[whisper](https://github.com/openai/whisper) 开源模型是 OpenAI 在 2022 年 9 月开源的一个模型，训练数据高达 68 万小时的音频，其中中文的语音识别数据有 23446 小时。 Whisper 是一个多语言、多任务模型，除了支持英语语音转录外，还支持包含中文、日语、韩语、西班牙语等其他 96 种语言的语音转录。此外，whisper 还支持语言识别、语音合成、翻译等多种任务。

Whisper 总共有5种不同大小的模型，其中4种有专一的英文模型，也即是下面的模型列表中除了 `large` 版本，其他模型都有对应的英文模型，在速度与准确性做了平衡。 

|大小 |参数|VRAM 大小 |相对最大模型的速度|
|:---:|:---:|:---:|:---:|
|tiny|39M|~1GB|~32x|
|base|74M|~1GB|~16x|
|small|244M|~2GB|~6x|
|medium|769M|~5GB|~2x|
|large|1550B|~10GB|~1|

`large` 是有 `v1`, `v2`, `v3` 三个版本的，默认使用的是 `v3`。

```python
_MODELS = {
    "tiny.en": "https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
    "tiny": "https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
    # ... 6 more models
    "large-v1": "https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large-v1.pt",
    "large-v2": "https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt",
    "large-v3": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
    "large": "https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdeefa8caeb59b3f1b81dadb/large-v3.pt",
}
```

## 速度 
在个人的 M2 Max 上使用 `small` 版本模型， 一条 3 分钟的音频转写耗时 20 秒左右，平均 1 分钟音频要 7 秒钟， 速度只能说一般。 按上面模型列表里面估算的速度比，如果使用最小的 `tiny` 版本， 1 分钟音频应该在 1.5 秒左右能转写完。 

作为对比，官方付费版本的whisper转写10分钟的音频，差不多是37秒，这包含了音频上传的时间，平均下来1分钟音频要3.7秒钟。

顺便说一下whisper 的价格，目前（2024-01）是1分钟音频四毛钱，也就是一个小时的音频，差不多2.4元人民币。这个价格相对来说还是有点贵的，国内像阿里、腾讯的价格，差不多是在1小时一块钱左右，如果走商务合作，这个价格还能更低，能做到0.2元/小时。


## 模型结构
典型的 sequence-to-sequence 模型，包含 encoder 和 decoder 两个部分。训练时多任务同时训练的，预测结果上：`|task taye or language|transcribe or translate|begin time or no timestamp|`。

第一个识别语言类型，如果没有语音内容，则是`nospeeach`，表示任务是 voice activity detection，模型结束，如果有内容，且语言假如是`EN`，第二个识别任务类型，`transcribe` 或者 `translate`。第三个预测是否识别时间戳，因为转录是需要加时间戳的，翻译不需要，后者对应的predict token是`no timestamp`。然后后面的就是转录或者翻译的内容了。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202401/whisper-structure_20240108_0927.png" width=789pt>
    <figcaption style="text-align:center"> whisper model </figcaption>
</figure>


## 使用示例

### 语言识别

```python
import whisper

model = whisper.load_model("base")
# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")
```

### 语音识别
使用 `base` 模型识别本地名称为 `audio.mp3` 的音频文件。
```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])
```

<style>
  .video-container {
    display: flex;
    justify-content: center;
    padding: 20px 10px;
  }

  iframe {
    width: 560px;
    height: 315px;
  }
</style>

关于怎么使用 whisper 来搭建私有语音转写服务，笔者 YouTube 视频里有简要的介绍，可以参考：
<div class="video-container">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/lIO61R9GAOs?si=Xk-OK-CpjLxwVcMA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen style="border-radius: 12px;"></iframe>
</div>


# whisper 付费产品
看一下官方文档上说的应该是 `large-v2` 版本的模型，中文的字错率差不多是 10.9%。这个水平在中文语音识别领域应该是算是还可以，差不多是一句话20个字里面有两个字错了，考虑到错误还包含儿化音、语气词，这个错误率还算能接受。 

官方的 `openai` 库把 `whisper` 封闭进去了， 使用也非常方便。 以下示例来源于官方文档：

```python
from openai import OpenAI
client = OpenAI()

audio_file= open("/path/to/file/audio.mp3", "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
```

官方文档 [https://platform.openai.com/docs/guides/speech-to-text](https://platform.openai.com/docs/guides/speech-to-text) 还介绍了语言支持、如何加提示（prompt）、提高可靠性。


# 参考 
- OpenAI 官方 whisper blog [https://openai.com/research/whisper/](https://openai.com/research/whisper/)
- 论文 [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356), arXiv:2212.04356
- Google colab 示例: [https://colab.research.google.com/github/openai/whisper/blob/master/notebooks/LibriSpeech.ipynb](https://colab.research.google.com/github/openai/whisper/blob/master/notebooks/LibriSpeech.ipynb)
