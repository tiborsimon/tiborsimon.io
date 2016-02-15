Title: Fuzzy search and sort algorithm
Subtitle: How to produce all relevant search results
Tags: fuzzy, search, sorting
Date: 2015-10-25
Img: img/thumb-449x286-7.jpg
Summary: What do you do, if your users may not know exactly what they are looking for while typing into a search field. You can try to provide all relevant matches based on the typed in characters. Time to search in a fuzzy way.


A good example for this is Sublime Text's search mechanism. You start to type in your query, and apart from
the exact matches you will get the matches containing the letters you gave but not in the exact order. In this
way you will find what you are looking for with a good chance even if you don't know the exact name.

The problem has two parts: __searching__ and __sorting__. It is not enough to provide all the relevant results that matched to
the search query, but you have to sort the result in the relevance order.

### Searching

The first part is the easier part. You only have to generate a clever regular expression from the
given search query.

You need to make sure, that between the given query's characters there might be another characters.
This can be achieved by inserting `.*` tokens:

`foo` -> `.*f.*o.*o.*`

You may also want to capture each provided search characters in order to know it's positions for later use.
The regexp engine can provide the positions for the matched groups.

`.*f.*o.*o.*` -> `.*(f).*(o).*(o).*`

But be aware. This capturing may result you an unexpected result when you want to use the provided group
positions by the regexp engine. Consider the following scenario: you want to find matches for 'x'. The
search query will be transformed into `.*(x).*`. Everything seems to be good, until your database contains
 a key that has more than one `x` characters in it. The regexp engine will match this key, but it will
capture the last `x` character in the key[^1]. If your sorting mechanism is based on the captured group
positions, this will be misleading for you.

To solve this issue, you have to force the regexp engine to match every character but to next captured character in the pattern.
You need to generate a more complex regular expression:

`.*(f).*(o).*(o).*` -> `[^f]*(f)[^o]*(o)[^o]*(o).*`

This is the final regular expression we are going to use in this article. We can now produce the match
results, it's time to sort them.

### Sorting

As I mentioned earlier, we are going to use the captured group's positions to sort the matched results.
The sorting algorithm will weight every match result, and based on that weight, the soring can be executed.

The weighting is based on the distance between the captured groups in a weighted manner. The distance between the first
characters is punished by more weight that the distance between the last characters. In this way if you know partly the first few characters
you want to search, this weighting method will provide the results matched in the first characters first. The lightest the matched result, the
more relevant it is, so it will be present earlier in the provided search result.

You can implement this behavior by iterating through the captured groups position list from back to front, calculating the distance between the matches and
multiplying them by a weighting factor. After each iteration you increase this weighting factor. And that's is.

### Summary

We have reviewed the fuzzy search and sort algorithm. You can find the usage example and the implementation in the following code snippets:

<div class="gist" data-gist-id="084a637ed3ce08042b76" data-gist-file="fuzzy_demo.py" data-gist-show-spinner="true"></div>

The previous example had the following internal data structure.

<div class="gist" data-gist-id="084a637ed3ce08042b76" data-gist-file="internal_printout.txt" data-gist-show-spinner="true"></div>

And here is the implementation available as a gist.

<div class="gist" data-gist-id="084a637ed3ce08042b76" data-gist-file="fuzzy_search.py" data-gist-show-spinner="true"></div>


[^1]: At least that was the case using the regexp engine shipped with Python 3.4 on OSX.
