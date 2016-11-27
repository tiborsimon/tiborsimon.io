---
title: TDD for microcontrollers
tags: embedded, tdd, pic
date: 2016-07-28
collection: articles
layout: article.html
draft: true
snippet: There is one thing that really bothers me in casual embedded software development. That is the lack of unit testing and the test driven development workflow. 
---

It is not taught in schools and in universities, but test driven development is one of the most important skill developers should know about. It provide easier development and confident, that the newly added feature don't beak the existing. _Test driven development is applicable only for object oriented programming languages._ You can hear this false argument everywhere. This is a misconception. You can test drive any procedural or functional language with ease with the appropriate testing framework you can write for yourself! And since embedded systems are programmed mostly in procedural languages (mainly in C), they can be thest driven as well.

However, I _couldn't find_ any embedded platform yet that comes with tdd ready resources that allows the casual developer to use test driven development with ease. There are gigantic header architectures and contraptions, that supposed to help the development, but in the reality they are not. Most of the developers think, that the provided header file system is the only way to develop on a given platform. I can tell you, this is not the case.

This article will use __Microchip's PIC__ microcontrollers and resources to demonstrate this new approach, but it can apply to any other platforms.

# The problem with existing resources

Just to be clear, there is nothing wrong with the provided header and definition system until you want to test drive your entire code. I take the resource files shipped with the __XC8__ PIC copiler as an example.




My TDD ready code.

``` bash
Memory Summary:
    Program space        used    12h (    18) of  2000h words   (  0.2%)
    Data space           used     3h (     3) of   400h bytes   (  0.3%)
    EEPROM space         None available
    Data stack space     used     0h (     0) of   3F0h bytes   (  0.0%)
    Configuration bits   used     2h (     2) of     2h words   (100.0%)
    ID Location space    used     0h (     0) of     4h bytes   (  0.0%)
```

Existing resources.

``` bash
Memory Summary:
    Program space        used     Ah (    10) of  2000h words   (  0.1%)
    Data space           used     2h (     2) of   400h bytes   (  0.2%)
    EEPROM space         None available
    Data stack space     used     0h (     0) of   3F0h bytes   (  0.0%)
    Configuration bits   used     2h (     2) of     2h words   (100.0%)
    ID Location space    used     0h (     0) of     4h bytes   (  0.0%)
```

