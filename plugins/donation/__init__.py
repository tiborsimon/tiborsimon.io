from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator
from bs4 import BeautifulSoup
import os


BUTTON_TEMPLATE = '''
<!-- Button trigger modal -->
<div class="well">
<p class="text-center lead">{}</p>
<button type="button" class="btn btn-primary btn-block btn-lg" data-toggle="modal" data-target="#donation-modal">Donate</button>
</div>
'''

MODAL_TEMPLATE = '''
<!-- Modal -->
<div class="modal fade" id="donation-modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
  <div class="modal-dialog modal-sm" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true"><i class="fa fa-times"></i></span></button>
        <h4 class="modal-title" id="myModalLabel">Donation</h4>
      </div>
      <div class="modal-body">
        <div style="text-align: center; font-size: 700%"><i class="fa fa-heart-o"></i></div>
        <p>Thank you very much that you have decided to support my work with a small amount of donation!</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default btn-xs" data-dismiss="modal">I changed my mind..</button>
      </div>
    </div>
  </div>
</div>
'''

def render_donation(pelican):
    print('Rendering donations..')
    for dirpath, _, filenames in os.walk(pelican.settings['OUTPUT_PATH']):
        for name in filenames:
            if name.endswith('html'):
                filepath = os.path.join(dirpath, name)
                soup = BeautifulSoup(open(filepath), 'html.parser')
                for m in soup.find_all('div', class_='modals'):
                    modal_div = m
                for donation_div in soup.find_all('div', class_='donation'):
                    text = donation_div.string
                    donation_div.string = BUTTON_TEMPLATE.format(text)
                    modal_div.append(MODAL_TEMPLATE)
                    with open(filepath, 'w') as f:
                        f.write(soup.prettify(formatter=None))


def register():
    signals.finalized.connect(render_donation)


