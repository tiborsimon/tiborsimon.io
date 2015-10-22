from pelican import signals

from bs4 import BeautifulSoup

def page_generator_finalized(generator):
	for page in generator.pages:
		process_item(page)

def article_generator_finalized(generator):
	for article in generator.articles:
		process_item(article)

def process_item(item):
	soup = BeautifulSoup(item._content, 'html.parser')
	fig_counter = 1
	for img in soup.find_all('img'):
		figure = soup.new_tag('div')
		figure['class'] = 'text-center'
		figure['style'] = 'width: 100%; height: auto;'
		img.wrap(figure)
		img['class'] = 'img-responsive img-thumbnail'
		caption = soup.new_tag('figcaption')
		figure.append(caption)
		caption.append(soup.new_tag('small'))
		caption.small.append(soup.new_tag('i'))
		caption.small.i.string = '<b>Fig {}</b>: {}'.format(fig_counter, img['alt'])
		fig_counter += 1
		item._content = soup.prettify(formatter=None)

def register():
    signals.article_generator_finalized.connect(article_generator_finalized)
    # signals.page_generator_finalized.connect(page_generator_finalized)
    pass