Title: Chart.js with subtabbed tabs
Subtitle: Two level deep tabbed setup
Tags: javascript, chart, bootstrap
Date: 2015-10-30

Chart.js is a bit tricky to use if you have dynamic tabs on your site. How about having multiple tabs 
with multiple tabs in them? Things get serious.<!-- PELICAN_END_SUMMARY --> 

People seem to have problems too by using tabs to show dynamic content on sites. The general solution to this problem is to use a bootstrap built in
callback that is fired when a tab activated to destroy the actual chart and draw the new chart based on
the tab selected. Well, that works fine until you have tabbed content in your tabs as well.

My plan was to create a tabbed page design that has sub tabs in them you can select
with a dropdown menu. So each main tab has its own dropdown menu.

I came up with this solution that will store the last active chart globally as well as the last active 
chart canvas context and data per main tabs. This variables make it possible to remember where the user
have left a tab, and it will be able to resume there.

<iframe width="100%" height="360" src="//jsfiddle.net/0scz7zak/2/embedded/result,js,html,css/" allowfullscreen="allowfullscreen" frameborder="0"></iframe>