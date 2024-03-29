---
layout: page
title: About
permalink: /about/
icon: heart
type: page
---

我是 ultrasev，一个喜欢研究技术、热爱影视的人。本博客主要记录并分享我在学习过程中的一些笔记与思考，主要内容有：

* `AI`
* `编程`
* `效率方法及工具` 
* `科学上网`

以下是笔者维护的一些信息聚合站点，内容每日更新：
- [AI 资讯(ai.ultrasev.com)](https://ai.ultrasev.com)：通过 RSS 采集微信公众号、资讯网站、技术博客后，过滤并提炼出的 AI 动向、热门技术及工具等相关文章。过滤模型基于 GPT-3.5，主要过滤掉一些低质量、广告、标题党内容。
- [高分影视集结(film.ultrasev.com)](https://film.ultrasev.com)：分享最近的高分影视资源。
- [短链接服务(dlj.one)](https://dlj.one)：基于 Cloudflare workers + R2 的短链接生成服务，短链接永久有效（大佬手下留情，勿滥用），笔者在博客中高频使用。

有任何问题或建议，欢迎在 Twitter 及 YouTube 上联系我。

- <i style="color: #1da1f2; font-size: 1.2em;" class="fa-brands fa-twitter" aria-hidden="true"></i>  [@ultrasev_](https://twitter.com/ultrasev_)
- <i style="color: #ff0000; font-size: 1.2em;" class="fa-brands fa-youtube" aria-hidden="true"></i> [@ultrasev](https://www.youtube.com/channel/UCt0Op8mQvqwjp18B8vNPjzg)


<!-- 自 2023 年 07 月 14 日起，本站已运行 <span id="days"></span> 天，截至 {{ site.time | date: "%Y 年 %m 月 %d 日" }}，写了博文 {{ site.posts.size }} 篇，{% assign count = 0 %}{% for post in site.posts %}{% assign single_count = post.content | strip_html | strip_newlines | remove: ' ' | size %}{% assign count = count | plus: single_count %}{% endfor %}{% if count > 10000 %}{{ count | divided_by: 10000 }} 万 {{ count | modulo: 10000 }}{% else %}{{ count }}{% endif %} 字。  -->


<!-- 若您觉得本博客所创造的内容对您有所帮助，可考虑略表心意，支持一下。

{% include reward.html %} -->

{% include comments.html %}

<script>
var days = 0, daysMax = Math.floor((Date.now() / 1000 - {{ "2016-07-07" | date: "%s" }}) / (60 * 60 * 24));
(function daysCount(){
    if(days > daysMax){
        document.getElementById('days').innerHTML = daysMax;
        return;
    } else {
        document.getElementById('days').innerHTML = days;
        days += 10;
        setTimeout(daysCount, 1); 
    }
})();
</script>
