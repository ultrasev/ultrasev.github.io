---
layout:     draft
title:      Low Rank Adpation -- Introduction[1]
date:       2024-03-25
tags: [llm, lora]
categories:
- llm
---

[LoRA](https://arxiv.org/abs/2106.09685)
idea behind:

对比全参数微调，LoRA 做了两件不同的事情：
1. 跟踪权重的变化而不是直接更新权重。
2. 将权重变化的大矩阵分解为包含“可训练参数”的较小矩阵。


假设模型参数量为 $d$，全参数微调需要更新 $d$ 个参数。而秩为 $r$ 的 LoRA 只需要更新的参数量为：

$$ 2 \cdot r \times \sqrt{d} $$

从参数百分比上看，LoRA 的参数量是全参数微调的 $2 \cdot r / \sqrt{d}$。模型的参数量越大，LoRA 的优势越明显。如下表所示，当 $d=180B$ 时，秩为 1024 的 LoRA 的参数量是全参数微调的 $0.483\%$。

| Rank | 7B     | 13B    | 70B    | 180B   |
|------|--------|--------|--------|--------|
| 1    | 0.002% | 0.002% | 0.001% | 0.000% |
| 2    | 0.005% | 0.004% | 0.002% | 0.001% |
| 4    | 0.010% | 0.007% | 0.003% | 0.002% |
| 8    | 0.019% | 0.014% | 0.006% | 0.004% |
| 16   | 0.038% | 0.028% | 0.012% | 0.008% |
| 512  | 1.224% | 0.898% | 0.387% | 0.241% |
| 1,024| 2.448% | 1.796% | 0.774% | 0.483% |
| 8,192| 19.583%| 14.370%| 6.193% | 3.862% |
| 16,384| 39.165%| 28.739%| 12.385%| 7.723% |

好处是**极大地减少存储与内存空间**。比如 GPT-3 175B 模型，全参数微调需要 1.2TB 的 VRAM，而 LoRA 只需要 350GB（r=1024）。


可能的问题：
- 精度下降，低阶矩阵分解在精度上做出了一定程度的让步。

# Q & A
1. LoRA 能够使用的原因或者背景是什么？

大模型存在“容量过大”（over-parametized）的问题，给定训练数据，模型的参数大于实际需要的参数。这种情况下，模型的参数可能会出现冗余性，鲁棒性和弹性。很多模型都存在低秩结构。


https://www.entrypointai.com/blog/lora-fine-tuning/

# Formally
假设 $W_0 \in \mathbb{R}^{d \times d}$ 是模型的参数矩阵，训练时 $W_0$ 会被冻结，而权重的更新 $\delta W=U \cdot V^T$ 会被低秩分解为 $U \in \mathbb{R}^{d \times r}$ 和 $V \in \mathbb{R}^{d \times r}$。这样，一次前向传播可表示为： $h = W_0 \cdot x + U \cdot V^T \cdot x$。

在初始化是，$V$ 通过 Gaussian 初始化，而 $U$ 通过 $U = 0$。

# 参考
- [1] [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [2] [Github: LoRA](https://github.com/microsoft/LoRA)
