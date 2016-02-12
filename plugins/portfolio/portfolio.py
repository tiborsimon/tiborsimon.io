from pelican import signals
import os
from bs4 import BeautifulSoup
import json
from pprint import pprint
from dateutil.parser import parse
import random


PELICAN = None


def load_portfolios():
  portfolio_path = './content/portfolio'
  dirs = os.listdir(portfolio_path)
  portfolios = []
  for d in dirs:
    p = os.path.join(portfolio_path, d)
    with open(p) as f:
      portfolio = json.load(f)
      portfolio['d'] = parse(portfolio['date'])
      portfolios.append(portfolio)

  portfolios.sort(key=lambda p:p['d'], reverse=True)
  return portfolios


PORTFOLIO_ITEM = '''
<div class="4u 12u(mobile)">
  <section class="highlight">
    <a href="{link}" target="_blank" class="image featured"><img src="{image}" alt="{alt}" /></a>
    <h3><a href="{link}" target="_blank">{title}</a></h3>
    <p>{description}</p>
  </section>
</div>'''

def render_portfolio_items(portfolios):
  ret = ''
  for portfolio in portfolios:

    try:
      image = portfolio['thumbnail']['url']
    except:
      image = PELICAN.settings['SITEURL'] + '/images/pic{:02}.jpg'.format(random.randrange(2,8))

    ret += PORTFOLIO_ITEM.format(
      link=portfolio['link'],
      image=image,
      alt='{} thumbnail'.format(portfolio['title']),
      title=portfolio['title'],
      date=portfolio['date'],
      description=portfolio['content']
    )
  return ret


PORTFOLIO_TEMPLATE = '''
<div class="row 150%">
  {portfolio_items}
</div>'''


def render_portfolio(portfolios):
  portfolio_items = render_portfolio_items(portfolios)
  return PORTFOLIO_TEMPLATE.format(portfolio_items=portfolio_items)


def generate_main_portfolios(pelican, portfolios):
  path = pelican.settings['OUTPUT_PATH'] + '/index.html'
  soup = BeautifulSoup(open(path), 'html.parser')

  for portfolio_div in soup.find_all('div', id='highlights'):
      portfolio_div.string = render_portfolio(portfolios)

  with open(path, 'w') as f:
    f.write(soup.prettify(formatter=None))


def generate_portfolio(pelican):
  global PELICAN
  PELICAN = pelican
  portfolios = load_portfolios()
  generate_main_portfolios(pelican, portfolios)


def register():
  signals.finalized.connect(generate_portfolio)
