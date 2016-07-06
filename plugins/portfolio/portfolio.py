from pelican import signals
import os
from bs4 import BeautifulSoup
import json
from pprint import pprint
from dateutil.parser import parse
import random


PELICAN = None


def load_portfolios():
    portfolio_path = './content/portfolio/portfolios.json'
    with open(portfolio_path) as f:
        portfolios = json.load(f)
    for p in portfolios:
        p['d'] = parse(p['date'])
    portfolios.sort(key=lambda p:p['d'], reverse=True)
    return portfolios


PORTFOLIO_ITEM = '''
<!-- Work Item (Lightbox) -->
<li class="work-item mix {category}">
    <a href="{link}" target="{target}" class="{type}">
        <div class="work-img">
            <img src="{image}" alt="{alt}" />
        </div>
        <div class="work-intro">
            <h3 class="work-title">{title}</h3>
            <div class="work-descr">
                {description}<br />
                {date}
            </div>
        </div>
    </a>
</li>
<!-- End Work Item -->'''


def render_portfolio(portfolios):
    ret = ''
    for portfolio in portfolios:
        try:
            image = portfolio['thumbnail']['url']
        except:
            image = PELICAN.settings['SITEURL'] + '/images/pic{:02}.jpg'.format(random.randrange(2,8))

        if portfolio['type'] == 'video':
            t = 'work-lightbox-link mfp-iframe'
            target = "_top"
        elif portfolio['type'] == 'image':
            t = 'work-lightbox-link mfp-image'
            target = "_top"
        else:
            t = 'work-ext-link'
            target = "_blank"
            
        ret += PORTFOLIO_ITEM.format(
            link=portfolio['link'],
            image=image,
            alt='{} thumbnail'.format(portfolio['title']),
            title=portfolio['title'],
            date=portfolio['date'],
            description=portfolio['content'],
            category=' '.join(portfolio['category']),
            type=t,
            target=target
        )
    return ret


def generate_selector(portfolios):
    selectors = []
    for p in portfolios:
        for c in p['category']:
            if c not in selectors:
                selectors.append(c)
    ret = '<a href="#" class="filter active" data-filter="*">All works</a>'
    for s in selectors:
        ret += '<a href="#{0}" class="filter" data-filter=".{0}">{1}</a>'.format(s, s.capitalize())
    return ret

            

def generate_main_portfolios(pelican, portfolios):
    path = pelican.settings['OUTPUT_PATH'] + '/index.html'
    soup = BeautifulSoup(open(path), 'html.parser')

    for portfolio_div in soup.find_all('ul', id='work-grid'):
        portfolio_div.string = render_portfolio(portfolios)

    for selector in soup.find_all('div', {'class': 'works-filter'}):
        selector.string = generate_selector(portfolios)

    with open(path, 'w') as f:
        f.write(soup.prettify(formatter=None))


def generate_portfolio(pelican):
    global PELICAN
    PELICAN = pelican
    portfolios = load_portfolios()
    generate_main_portfolios(pelican, portfolios)
    print('Portfolio generated.')


def register():
    signals.finalized.connect(generate_portfolio)

