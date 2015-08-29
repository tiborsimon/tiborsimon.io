from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator
import json
import re

data = []

def extract_data(instance):

    data.append({
            'title': instance.title,
            'category': instance.category._name,
            'tags': [tag._name for tag in instance.tags],
            'url': instance.url,
            'date': '{}-{}-{}'.format(instance.date.year, instance.date.month, instance.date.day),
            'summary': re.sub('<.*?>', '', instance.summary)
        })

def run_plugin(generators):
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in generator.articles:
                extract_data(article)
        elif isinstance(generator, PagesGenerator):
            for page in generator.pages:
                extract_data(page)
    with open('content/extras/search.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=4, sort_keys=True))

def register():
    signals.all_generators_finalized.connect(run_plugin)