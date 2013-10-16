---
layout: default
---

<div>
  <ul class="listing main-listing">
  {% capture year %}{{ site.time | date:"%Y"}}{% endcapture %}
  {% for post in site.posts %}
    {% capture y %}{{ post.date | date:"%Y"}}{% endcapture %}
    {% if year != y %}
    {% break %}
    {% endif %}
    <li class="listing-item">
      <time datetime="{{ post.date | date:"%Y-%m-%d" }}">{{ post.date | date:"%Y-%m-%d" }}</time>
      <a href="{{ post.url }}" title="{{ post.title }}">{{ post.title }}</a>
    </li>
  {% endfor %}
  </ul>
</div>
