Title: Get half of the list in Pelican
Subtitle: Finding out the possibilities programmatically
Tags: pelican, jinja2, lists, hack
Date: 2016-02-14

As I was creating my site, I wanted to split a list of articles in half to display them in two columns. There are two options to do this: with Jinja2 built in filters, or a custom Jinja2 filter.<!-- PELICAN_END_SUMMARY -->

I wanted to display a list of articles in a two columns. If there are even number of articles, the two columns will have the same number articles. If there are odd number of articles, the first column will contain more articles then the second. This behavior can be achieved with a ceil-like function, which returns the smallest integer greater than or equal to a given number.



# Using built in Jinja2 filters

In the first solution we are using only the built in Jinja filters. Because of the lack of mathematical functions in the built in filters, we need to hack the only available rounding filter ( `round`) to be able to use it as a `ceil` like function.

The steps are the followings:

1. Get the half of the article list's length
1. Add a small number from the ]0,1[ intervallum
1. Use the round filter
1. Cast the result to _integer_

```
{% set article_middle_index = articles|length / 2 %}
{% set article_middle_index = article_middle_index + 0.2 %}
{% set article_middle_index = article_middle_index|round %}
{% set article_middle_index = article_middle_index|int %}
```

Since `{{ 0.5|round }}` is `0.0` according to Jinja2, we need to add a small number to the halfed number, to achieve the ceil-like behavior.

# Writing a custom Jinja filter

We can also write a custom Jinja filter that calculates the middle index of a list, by appending a small function definition and a special dictionary that tells Pelican to use the function definition as a Jinja filter to the `pelicanconf.py` file:


```
def list_half_index(content, *args):
    return ceil(len(content))

JINJA_FILTERS = {
    'list_half_index': list_half_index,
}
```

In the Pelican template files, we can use our custom filter as follows:

```
{% set article_middle_index = articles|middle_index %}
```

# Using the middle index

We have now the middle index of an article list, so we can use it to split the list to half:


```
<div class="row">
  <div class="6u 6u(tablet) 12u(mobile)">
    {% for article in articles[:article_middle_index] %}
      {% include 'includes/article-card.html' %}
    {% endfor %}
  </div>

  <div class="6u 6u(tablet) 12u(mobile)">
    {% for article in articles[article_middle_index:] %}
      {% include 'includes/article-card.html' %}
    {% endfor %}
  </div>
</div>
```

We ended up having two coloms of articles that are generated from a single list.
