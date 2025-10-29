---
title: Welcome to NSW Mesh
---

This is the community-maintained knowledge base for everything 'Mesh' in Sydney and throughout New South Wales.

We're experimenters, bushwalkers, emergency‑comms nerds and tinkerers. Jump into [our Discord](https://discord.gg/Du437Usj3K) and say hi, or explore the live tools and articles below.


[//]: # (This is auto generated based on the contents of the docs folder!)
{% assign docs_pages = site.pages | where_exp: "item", "item.dir contains '/docs/'" %}
{% assign docs_pages = docs_pages | where_exp: "item", "item.title" %}
{% assign grouped_pages = docs_pages | group_by: "dir" %}

{% for group in grouped_pages %}
  {% assign folder_name = group.name | remove: "/docs/" | remove: "/" | replace: "-", " " | capitalize %}
  {% if folder_name == "" %}
    {% assign folder_name = "General Articles" %}
  {% endif %}
- {{ folder_name }}
{% for page in group.items %}
    - [{{ page.title | escape }}]({{ page.url | relative_url }})
{% endfor %}
{% endfor %}

- Meshcore Links and Tools (primary system in use in Sydney currently)
    - [Live World Meshcore Map](https://meshcore.co.uk/map.html)
    - [Sydney Meshcore Map](https://nswmesh.github.io/NSW-Sydney-Meshcore-Map).
    - [Meshcore site](https://meshcore.co.uk/index.html).
    - [Meshcore Wiki](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md).
    - [How to get started with Meshcore Video](https://youtu.be/t1qne8uJBAc?si=0vyErpZz1wsbG_hJ).
    - [Meshcore Firmware Web Flasher](https://flasher.meshcore.co.uk/).
    - [Official Meshcore Youtube Channel](https://www.youtube.com/@meshcore-official).
    - [Meshcore Web Client](https://app.meshcore.nz/).
    - [Meshcore Repeater/Roomserver USB Setup web client](https://config.meshcore.dev/).
    - [Meshcore Repeater and Roomserver CLI Reference](https://github.com/meshcore-dev/MeshCore/wiki/Repeater-&-Room-Server-CLI-Reference).
    - [Meshcore web Client By Liam Cottle](https://meshcore.liamcottle.net/#/).
    - [General tips for setting up your T-Deck/T-Deck Pro/T-Pager/T-Watch on Meshcore](https://buymeacoffee.com/ripplebiz/ultra-v7-7-guide-meshcore-users).
    
- Meshtastic Tools and Links (secondary system still in use in Sydney)
    - [Live Map](https://map.nswmesh.au/map)
    - [Node List](https://map.nswmesh.au/nodelist)
    - [Conversations / Weekly Net](https://map.nswmesh.au/net)
    - [Mesh Statistics](https://map.nswmesh.au/stats)
    - [Top Traffic](https://map.nswmesh.au/top)
    - [Sydney Mesh Statistics Dashboard](https://map.nswmesh.au/stats) (Login: guest/guest)
