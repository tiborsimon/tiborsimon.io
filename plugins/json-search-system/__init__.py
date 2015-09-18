from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator
import json
import re
from tiborsimonio import Store

Store.project_file = 'tspr.json'
store = Store.load()

data = []

def extract_data(instance):
    if instance.title == 'Projects' or instance.title == 'Daily work log':
        return
    data.append({
            'title': instance.title,
            'category': ' ',
            'tags': [' '+tag._name for tag in instance.tags],
            'url': 'http://tiborsimon.io/'+instance.url,
            'date': '{}-{}-{}'.format(instance.date.year, instance.date.month, instance.date.day),
            'summary': re.sub('<.*?>', '', instance.summary)
        })

def add_projects():
    for project in store.projects:
        if project['state'] != 'private':
            data.append({
                'title': project['title'],
                'category': '<small><span class="label label-default">PR{:06}</span></small>'.format(project['id']) if project['tspr']==0 else '<small><span class="label label-primary">TSPR{:04}</span> <span class="label label-default">PR{:06}</span></small>'.format(project['tspr'], project['id']),
                'tags': ', '.join(project['tags']),
                'url': 'http://tiborsimon.io/projects/#'+'PR{:06}'.format(project['id']) if project['tspr']==0 else 'http://tiborsimon.io/projects/#'+'TSPR{:04}'.format(project['tspr']),
                'date': '-',
                'summary': project['description']
            })


def run_plugin(generators):
    add_projects()
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