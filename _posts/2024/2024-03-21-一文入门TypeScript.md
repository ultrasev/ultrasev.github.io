---
layout: post
title: 一文入门TypeScript
date: 2024-03-21
tags: typescript ts
categories: coding
author: ultrasev
---
* content
{:toc}


前几天把良心云 cloudflare 的一个 [worker](gateway.ddot.cc) 用 js 重写了一下，然后还引入了后端的层次框架，有种突然入门 js 的感觉。平时笔者coding主要使用 Python，尽管Python是弱类型语言，但是在 Python 3.5 之后引入了类型提示，笔者在coding的过程中还是会尽量使用类型提示，这样可以让代码更加清晰，也方便IDE的自动补全。




但使用js后，发现js的似乎并不支持类型提示，这让笔者有些不适应，然后就决定了解一下 TypeScript。作为一个ts纯新手，这个文章主要是记录一下笔者学习ts的过程，以及笔者认为的比较重要的一些知识点。
