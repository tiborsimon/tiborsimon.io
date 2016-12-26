---
title: Fuzzy search and sort algorithm
tags: search, python, regexp
date: 2015-10-25
collection: articles
layout: article.html
snippet: What do you do, if your users may not know exactly what they are looking for while typing into a search field. You can try to provide all relevant matches based on the typed in characters. Time to search in a fuzzy way.
---


A good example for this is Sublime Text's search mechanism. You start to type in your query, and apart from
the exact matches you will get the matches containing the letters you gave but not in the exact order. In this
way you will find what you are looking for with a good chance even if you don't know the exact name.

The problem has two parts: __searching__ and __sorting__. It is not enough to provide all the relevant results that matched to
the search query, but you have to sort the result in the relevance order.

# Searching

The first part is the easier part. You only have to generate a clever regular expression from the
given search query.

You need to make sure, that between the given query's characters there might be another characters.
This can be achieved by inserting `.*` tokens:

``` bash
foo -> .*f.*o.*o.*
```

You may also want to capture each provided search characters in order to know it's positions for later use.
The regexp engine can provide the positions for the matched groups.

``` bash
.*f.*o.*o.* -> .*(f).*(o).*(o).*
```

But be aware. This capturing may result you an unexpected result when you want to use the provided group
positions by the regexp engine. Consider the following scenario: you want to find matches for 'x'. The
search query will be transformed into `.*(x).*`. Everything seems to be good, until your database contains
 a key that has more than one `x` characters in it. The regexp engine will match this key, but it will
capture the last `x` character in the key[^1]. If your sorting mechanism is based on the captured group
positions, this will be misleading for you.

To solve this issue, you have to force the regexp engine to match every character but to next captured character in the pattern.
You need to generate a more complex regular expression:

``` bash
.*(f).*(o).*(o).* -> [^f]*(f)[^o]*(o)[^o]*(o).*
```

This is the final regular expression we are going to use in this article. We can now produce the match
results, it's time to sort them.

# Sorting

As I mentioned earlier, we are going to use the captured group's positions to sort the matched results.
The sorting algorithm will weight every match result, and based on that weight, the soring can be executed.

The weighting is based on the distance between the captured groups in a weighted manner. The distance between the first
characters is punished by more weight that the distance between the last characters. In this way if you know partly the first few characters
you want to search, this weighting method will provide the results matched in the first characters first. The lightest the matched result, the
more relevant it is, so it will be present earlier in the provided search result.

You can implement this behavior by iterating through the captured groups position list from back to front, calculating the distance between the matches and
multiplying them by a weighting factor. After each iteration you increase this weighting factor. And that's is.

# Summary

We have reviewed the fuzzy search and sort algorithm. You can find the usage example and the implementation in the following code snippets:

``` python
import fuzzy
from pprint import pprint

data_list = [
    'efo',
    'efoo',
    'dfsfoo',
    'efiofo',
    'abc',
    'cba',
    'foo',
    'ertfo',
    'fefefofefioiio'
]

result = fuzzy.search(data_list, 'foo')

pprint(result)

# >> ['foo', 'efoo', 'efiofo', 'dfsfoo', 'fefefofefioiio']
```

The previous example had the following internal data structure.

```
[{'spans': ((0, 1), (1, 2), (2, 3)), 'string': 'foo', 'weight': 0},
 {'spans': ((1, 2), (2, 3), (3, 4)), 'string': 'efoo', 'weight': 4},
 {'spans': ((1, 2), (3, 4), (5, 6)), 'string': 'efiofo', 'weight': 7},
 {'spans': ((1, 2), (4, 5), (5, 6)), 'string': 'dfsfoo', 'weight': 8},
 {'spans': ((0, 1), (5, 6), (10, 11)), 'string': 'fefefofefioiio', 'weight': 12}]
```

And here is the implementation available as a gist.

```
import re


def search(raw_list, search_string, ignore_case=True):
    if search_string == '':
        return raw_list
    else:
        search_pattern = _create_search_pattern_from(search_string)
        result = _get_filtered_result_list_structure(raw_list, search_pattern, ignore_case)
        result = _sort_result_list(result)
        return [r['string'] for r in result]


def _create_search_pattern_from(pattern):
    grouped = '[^{}]*'.format(pattern[0])
    for i in range(len(pattern)):
        if i < len(pattern) - 1:
            grouped += '({})[^{}]*'.format(pattern[i], pattern[i + 1])
        else:
            grouped += '({})'.format(pattern[i])
    grouped += '.*'
    return grouped


def _get_filtered_result_list_structure(raw_list, search_pattern, ignore_case):
    if ignore_case:
        p = re.compile(search_pattern, re.IGNORECASE)
    else:
        p = re.compile(search_pattern)
    result = [{'string': link, 'spans': p.search(link).regs[1:]} for link in raw_list if p.match(link)]
    return result


def _calculate_weight_for_match(spans):
    mult = 1
    weight = 0
    for i in reversed(range(len(spans))):
        prev = 0 if i == 0 else spans[i-1][1]
        weight += (spans[i][0] - prev) * mult
        mult *= 2
    return weight


def _sort_result_list(result):
    for r in result:
        r['weight'] = _calculate_weight_for_match(r['spans'])
    result = sorted(result, key=lambda k: k['weight'])
    return result
```

[^1]: At least that was the case using the regexp engine shipped with Python 3.4 on OSX.

