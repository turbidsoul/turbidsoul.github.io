---
layout: page
title: Turbidsoul's 小黑屋
tagline: 成为优秀的开发人员，可以没有数学技能，但成为卓越的开发人员，不能没有！
---


<script src="//about.me/embed/turbidsoul"></script>

-----------------------------------------------------------------------------------------


最新文章
========

<ul class="posts">
  {% for post in site.posts %}
    <li class="article_list"><span>{{ post.date | date: "%Y-%m-%d") }}</span> &raquo; <a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></li>
    <p>{{post.excerpt}}</p>
    {% if forloop.index >= 10 %}
        {% break %}
    {% endif %}
  {% endfor %}
</ul>


