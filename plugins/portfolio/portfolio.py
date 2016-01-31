from pelican import signals
import os
from bs4 import BeautifulSoup
import json
from pprint import pprint
from dateutil.parser import parse


PORTFOLIO_TEMPLATE = '''
<section id="portfolio" class="section section-portfolio">
  <div class="animate-up">
    <h2 class="section-title">Portfolio</h2>

    <div class="filter">
      <div class="filter-inner">
        <div class="filter-btn-group">
          <button data-filter="*">All</button>
          {navigation}
        </div>
        <div class="filter-bar">
          <span class="filter-bar-line"></span>
        </div>
      </div>
    </div>

    <div class="grid">
      <div class="grid-sizer"></div>
      {grid}
    </div>
  </div>
</section>'''


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


def render_categories(portfolios):
  categories = [portfolio['category'].lower() for portfolio in portfolios]
  ret = ''
  for c in categories:
    ret += '<button data-filter=".{0}">{1}</button>\n'.format(c, c.capitalize())
  return ret


EMBED_IMG = '''
<img class="inline-img" src="{image_src}" alt="{image_alt}"/>'''

EMBED_VIDEO = '''
<div class="inline-embed">
  {embed_code}
</div>'''

def render_box_embed(box):
  if 'image' in box.keys():
    box_embed = EMBED_IMG.format(image_src=box['image']['url'], image_alt=box['image']['alt'])
  elif 'embed' in box.keys():
    box_embed = EMBED_VIDEO.format(embed_code=box['embed'])
  else:
    print('Invalid slide type! Aborting..')
    return None
  return box_embed


INLINE_BOX = '''
<div id="portfolio{portfolio_number}-inline{inline_id}" class="fancybox-inline-box">
  {embed}
  <div class="inline-cont">
    <div class="inline-text">
      <h2 class="inline-title">{title}</h2>
      <p>{description}</p>
    </div>
  </div>
</div>'''

INLINE_BOX_LINK = '''
<a class="portfolioFancybox hidden" data-fancybox-group="portfolioFancybox{portfolio_number}" href="#portfolio{portfolio_number}-inline{inline_id}"></a>'''

def render_inline_boxes(portfolios, portfolio):
  inline_boxes = ''
  inline_box_links = ''
  offset = False
  for box in portfolio['slides']:
    box_embed = render_box_embed(box)

    inline_box = INLINE_BOX.format(
      embed=box_embed,
      title=box['title'],
      description=box['content'],
      portfolio_number=portfolios.index(portfolio),
      inline_id=portfolio['slides'].index(box)
    )

    inline_box_link = ''

    if offset:
      inline_box_link = INLINE_BOX_LINK.format(
        portfolio_number=portfolios.index(portfolio),
        inline_id=portfolio['slides'].index(box)
      )

    inline_boxes += inline_box
    inline_box_links += inline_box_link

    offset = True

  return (inline_boxes, inline_box_links)


PORTFOLIO_ITEM = '''
<div class="grid-item {size} {category}">
  <div class="grid-box">
    <figure class="portfolio-figure">
      <img src="{thumbnail_src}" alt="{thumbnail_alt}"/>
      <figcaption class="portfolio-caption">
        <div class="portfolio-caption-inner">
          <h3 class="portfolio-title">{title}</h3>
          <h4 class="portfolio-cat">{category_display}</h4>

          <div class="btn-group">
            <a class="btn-link" href="{button_url}" target="_blank"><i class="icon icon-link"></i></a>
            <a class="portfolioFancybox btn-zoom" data-fancybox-group="portfolioFancybox{portfolio_number}" href="#portfolio{portfolio_number}-inline0"><i class="icon icon-eye"></i></a>

            {inline_box_links}

          </div>
        </div>
      </figcaption>
    </figure>
    {inline_boxes}
  </div>
</div>'''

def render_portfolio_items(portfolios):
  ret = ''
  for portfolio in portfolios:
    (inline_boxes, inline_box_links) = render_inline_boxes(portfolios, portfolio)

    ret += PORTFOLIO_ITEM.format(
      size=portfolio['size'],
      category=portfolio['category'].lower(),
      thumbnail_src=portfolio['thumbnail']['url'],
      thumbnail_alt=portfolio['thumbnail']['alt'],
      title=portfolio['title'],
      category_display=portfolio['category'].capitalize(),
      button_url=portfolio['link'],
      portfolio_number=portfolios.index(portfolio),
      inline_box_links=inline_box_links,
      inline_boxes=inline_boxes
    )
  return ret


def render_portfolio(div, portfolios):
  categories = render_categories(portfolios)
  portfolio_items = render_portfolio_items(portfolios)
  div.string = PORTFOLIO_TEMPLATE.format(navigation=categories, grid=portfolio_items)


def generate_portfolio(pelican):
  portfolios = load_portfolios()

  path = pelican.settings['OUTPUT_PATH'] + '/index.html'
  soup = BeautifulSoup(open(path), 'html.parser')

  for portfolio_div in soup.find_all('div', id='portfolio'):
      render_portfolio(portfolio_div, portfolios)

  with open(path, 'w') as f:
    f.write(soup.prettify(formatter=None))


def register():
  signals.finalized.connect(generate_portfolio)
