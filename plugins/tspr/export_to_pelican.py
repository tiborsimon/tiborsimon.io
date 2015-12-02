from pelican import signals
from bs4 import BeautifulSoup
from hurry.filesize import size
import os
from pprint import pprint

from tiborsimonio import Store

Store.project_file = 'tspr.json'
store = Store.load()

def execute(generator):
    print('Exporting to pelican..')
    # pprint(generator.context.__class__)
    # pprint((generator.context))
    # pprint(store.projects)
    generator.context['projects'] = store.projects



def register():
    signals.page_generator_finalized.connect(execute)