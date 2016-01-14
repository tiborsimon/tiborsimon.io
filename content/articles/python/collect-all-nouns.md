Title: Collect all nouns in hungarian
Subtitle: Or in any other language that have a web based database
Tags: web, hack, soup
Date: 2015-10-24
Img: img/thumb-449x286-7.jpg

I had to create a searchable noun list in hungarian without any publicly available word list that I
can easily download.<!-- PELICAN_END_SUMMARY --> Hopefully, there is a <a href="https://hu.wiktionary.org/wiki/Kategória:magyar_főnevek" target="_blank">hungarian wiki dictionary</a>
that contains all words in hungarian, and it has a noun filter. It can show the nouns breaked.
Instead of manually copying the pages content for the available 200 pages, I fired up my two favorite
python library: _BeautifulSoup4_ and _Requests_.

The nouns on the wiki page were arranged into a table, so I had to extract the words from the `<li></li>`
tags from the html file, downloaded via a web request using the _Requests_ library and created a soup
from it with _BeautifulSoup4_.

The whole process was arranged into an infinite while loop. It will run until a valid next page link
 can be found. Not the best solution, but hey, it was just a scipt :) Inside this while loop, there is a
 loop that will collect the words into a list. The delimiter for this inner loop was a common
 word (magyar szótár), that was present on every page after the last listed noun.

<div class="gist" data-gist-id="8a52c046df3a5cae0c59" data-gist-show-spinner="true"></div>

During the process, I printed out every next link the script was found, so I had a feedback where the script
was in the alphabet. As you can see, the last log was an exception printout, indicating that the script could
not parse the next link from the html file.

<div class="gist" data-gist-id="70942e98a88c74ee9dc3" data-gist-show-spinner="true"></div>
