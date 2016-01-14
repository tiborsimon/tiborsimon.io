Title: Mandatory + arbitrary order
Subtitle: Simple to say but longer to write
Tags: regexp, permutation
Date: 2015-10-29
Img: img/thumb-449x286-7.jpg

What regular expression pattern would you use if you want to match a word with mandatory characters in it but in
arbitrary order?<!-- PELICAN_END_SUMMARY -->

You cannot use character set like `[abc]` because this pattern does not garanties the mandatoryness, even if you write the
exact number of it `[abc]{3}`. It will match three `a` characters too. You cannot force the regular expression engine to
handle arbitrary order with the mandatory constraint. You have to do it yourself with permutation.

You have to tell the regexp engine that you want allow all the possible permutation of a character list, with optional
charachters between them. You can do it with options.

For example, if you want to match words that has `a` and `b` in them in arbitrary order, you can write: `((.*a.*b.*)|(.*b.*a.*))`.
Not so horrible, is it. But. We are talking about permutation. If you want to add 3 characters, the pattern length will increase:

```
((.*a.*b.*c.*)|(.*a.*c.*b.*)|(.*b.*a.*c.*)|(.*b.*c.*a.*)|(.*c.*a.*b.*)|(.*c.*b.*a.*))
```

For 4 characters, it reaches the 409 charachters length:
```
((.*a.*b.*c.*d.*)|(.*a.*b.*d.*c.*)|(.*a.*c.*b.*d.*)|(.*a.*c.*d.*b.*)|(.*a.*d.*b.*c.*)|(.*a.*d.*c.*b.*)|(.*b.*a.*c.*d.*)|(.*b.*a.*d.*c.*)|(.*b.*c.*a.*d.*)|(.*b.*c.*d.*a.*)|(.*b.*d.*a.*c.*)|(.*b.*d.*c.*a.*)|(.*c.*a.*b.*d.*)|(.*c.*a.*d.*b.*)|(.*c.*b.*a.*d.*)|(.*c.*b.*d.*a.*)|(.*c.*d.*a.*b.*)|(.*c.*d.*b.*a.*)|(.*d.*a.*b.*c.*)|(.*d.*a.*c.*b.*)|(.*d.*b.*a.*c.*)|(.*d.*b.*c.*a.*)|(.*d.*c.*a.*b.*)|(.*d.*c.*b.*a.*))
```

### Generator in python

You can write a generator for this regexp pattern easily in python:

<div class="gist" data-gist-id="8cf9e3d6c8ce2ca36ce8" data-gist-show-spinner="true"></div>
