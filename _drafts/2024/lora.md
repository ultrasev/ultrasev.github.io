---
layout:     draft
title:      Low Rank Adpation -- Introduction[1]
date:       2024-03-25
tags: [llm, lora]
categories:
- llm
---


[LoRA](https://arxiv.org/abs/2106.09685) 工作原理是将权重更新矩阵分解为更小的矩阵，并使用它们来训练模型。对比全量参数微调，LoRA:
1. 跟踪权重的变化而不是直接更新权重。
2. 将权重变化矩阵拆分成小矩阵，用小矩阵的乘积来近似原始权重变化。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202403/qlora-dalle_20240326_0905.png" width=789pt>
    <figcaption style="text-align:center"> Source — Image generated using DALLE-3 </figcaption>
</figure>


假设模型参数量为 $d$，全参数微调需要更新 $d$ 个参数。而秩为 $r$ 的 LoRA 只需要更新的参数量为：

$$ 2 \cdot r \times \sqrt{d} $$

从参数百分比上看，LoRA 的参数量是全参数微调的 $2 \cdot r / \sqrt{d}$。因此，模型的参数量越大，LoRA 的优势越明显。如下表所示，当 $d=180B$ 时，秩为 1024 的 LoRA 的参数量仅占全量微调参数量的 $0.483\%$。

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

首先一个好处是**极大地减少存储与内存空间**。比如 GPT-3 175B 模型，全参数微调需要 1.2TB 的 VRAM，而 LoRA 只需要 350GB（r=1024）。

另一个好处是**快速训练与领域适配**：通过简化计算需求，LoRA 加速了大型模型针对新任务的训练和微调。

其他的间接好处有，支持在较小的设备上微调大模型。

论文中给出的合适的 $r$ 值是 ???，这个值xxx
可能的问题：
- 精度会稍微下降，低阶矩阵分解在精度上做出了一定程度的让步。


# Formally
假设 $W_0 \in \mathbb{R}^{d \times d}$ 是模型的参数矩阵，而权重的更新 $\Delta W=U \cdot V^T$ 会被低秩分解为 $U \in \mathbb{R}^{d \times r}$ 和 $V \in \mathbb{R}^{d \times r}$，其中 $ r \ll d$。这样，一次前向传播可表示为： $h = W_0 \cdot x + U \cdot V^T \cdot x$。训练时 $W_0$ 会被冻结，只训练 $U$ 与 $V$。初始化时，$V$ 通过 Gaussian 初始化，而 $U$ 通过 $U = 0$。

<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202403/lora-figure_20240326_0808.png" width=389pt>
    <figcaption style="text-align:center"> LoRA reparametrization. </figcaption>
</figure>

# 变体
## QLoRA
QLoRA 的思想是**把高精度计算技术与低精度存储方法相结合**，在保持模型尺寸较小的同时，仍确保模型的高性能和准确性。


<figure style="text-align: center;">
    <img src="https://image.ddot.cc/202403/qlora_20240326_0843.png" width=689pt>
    <figcaption style="text-align:center"> QLoRA v.s. LoRA </figcaption>
</figure>


## LongLoRA
TODO

# Q & A
1. LoRA 能够使用的原因或者背景是什么？
这就要提到一个概念：The intrinsic rank hypothesis，即模型的低秩结构假设。这个假设认为，可以使用较低维的表示来捕获神经网络的显着变化。它假定 $\Delta W$ 的所有元素并非同等重要，相反，只要一具较小的子集可以有效地“捕获”必要的调整。

从模型的训练角度上讲，大模型存在“容量过大”（over-parametized）的问题，即给定训练数据，模型的参数大于实际需要的参数。这种情况下，模型的参数可能会出现冗余性，鲁棒性和弹性。很多模型都存在低秩结构，[Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning](https://arxiv.org/abs/2012.13255) 认证了只需要优化（RoBERTA）小一部分参数，就能达到全微调 90% 的效果。

LoRA 基于这个假设，通过低秩分解，将权重更新矩阵分解为更小的矩阵，并使用它们来训练模型。


https://www.entrypointai.com/blog/lora-fine-tuning/


# 实验
是在大模型上验证 LoRA 的有效性。但鉴于本地 GPU 性能有限，只能退而求其次，使用小模型验证 LoRA 的有效性。模型就选择经典的 BERT 模型，任务选择文本分类，数据集选择 IMDB。

Huggingface 开源[peft](https://github.com/huggingface/peft) 库，可以方便地在 PyTorch 中使用 LoRA。

代码可参考 [Github: LoRA]()


# 参考
- [1] [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [2] [Github: LoRA](https://github.com/microsoft/LoRA)
