Title: Redirect external links to new tab
Subtitle: Fix Markdown's lack of hyperlink targeting feature with javascript
Tags: pelican, hack, javascript
Date: 2015-05-17
Modified: 

As Pelican can use Markdown to render it's contents, and Markdown doesn't support 
control over the hyperlink target attribute, you were forced to write your 
external links and references manually. Or not? 
<!-- PELICAN_END_SUMMARY --> 
Hopefully, there is a simple javascript hack, that can redirect your external 
links to a new blank tab.

All the credits go to [Austin](http://stackoverflow.com/users/1504966/austin) 
and to his [stackoverflow post](http://stackoverflow.com/a/11597448). I am just 
a happy user of this method :)

<div data-gist-id="78f71b14d1436e867354"></div>

The method just works. Nothing fancy about it, it does what is supposed to do. 
Thank you Austin!
