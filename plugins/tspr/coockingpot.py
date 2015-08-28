from pelican import signals
from bs4 import BeautifulSoup
from hurry.filesize import size

from .tspr import Store

Store.project_file = 'tspr.json'


def add_worklog_project_list(instance):
    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')
        for tspr_div in soup.find_all('div', class_='tspr-worklog'):
            add_panel_group(soup, tspr_div)
        instance._content = soup.prettify()


def add_panel_group(soup, tspr_div):
    panel_group = soup.new_tag('div')
    panel_group['class'] = 'panel-group'
    panel_group['id'] = 'tspr-accordion'
    panel_group['role'] = 'tablist'
    panel_group['aria-multiselectable'] = 'true'
    tspr_div.append(panel_group)
    store = Store.load()
    for project in store.projects:
        add_panel(panel_group, project, soup)


def add_panel(panel_group, project, soup):
    panel = soup.new_tag('div')
    panel['class'] = 'panel panel-default'
    add_panel_heading(panel, project, soup)
    add_panel_collapse(panel, project, soup)
    panel_group.append(panel)


def add_panel_collapse(panel, project, soup):
    panel_collapse = soup.new_tag('div')
    panel_collapse['class'] = 'panel-collapse collapse'
    panel_collapse['role'] = 'tabpanel'
    panel_collapse['id'] = 'TSPR{:06}-collapse'.format(project['id'])
    panel_collapse['aria-labelledy'] = 'TSPR{:06}-heading'.format(project['id'])
    add_panel_body(panel_collapse, project, soup)
    panel.append(panel_collapse)


def add_panel_body(panel_collapse, project, soup):
    panel_body = soup.new_tag('div')
    panel_body['class'] = 'panel-body'
    panel_collapse.append(panel_body)

    if project['state'] == 'private':
        panel_body.string = 'Private project..'
    else:
        panel_body.append(soup.new_tag('strong'))
        panel_body.strong.string = project['title']
        panel_body.append(soup.new_tag('p'))
        panel_body.p.string = project['description']
        add_tag_field(panel_body, project, soup)

    if project['state'] == 'released':
        add_buttons(panel_body, project, soup)


def add_buttons(panel_body, project, soup):
    button_p = soup.new_tag('p')
    panel_body.append(button_p)

    button_div = soup.new_tag('div')
    button_div['class'] = 'btn-group btn-group-xs'
    button_div['role'] = 'group'
    button_p.append(button_div)

    # Article button
    temp_button = soup.new_tag('a')
    temp_button['role'] = 'button'
    temp_button['style'] = 'min-width: 24px'
    temp_button['class'] = 'btn btn-default'
    temp_button['data-toggle'] = 'tooltip'
    temp_button['data-container'] = 'body'
    temp_button['data-placement'] = 'top'
    temp_button['title'] = 'Corresponding article'
    temp_button.append(soup.new_tag('i'))
    #temp_button.append('Discuss')
    temp_button.i['class'] = 'fa fa-bookmark'
    temp_button['href'] = project['article']
    button_div.append(temp_button)

    # Comments button
    temp_button = soup.new_tag('a')
    temp_button['role'] = 'button'
    temp_button['style'] = 'min-width: 24px'
    temp_button['class'] = 'btn btn-default'
    temp_button['data-toggle'] = 'tooltip'
    temp_button['data-container'] = 'body'
    temp_button['data-placement'] = 'top'
    temp_button['title'] = 'Discussion'
    temp_button.append(soup.new_tag('i'))
    #temp_button.append('Discuss')
    temp_button.i['class'] = 'fa fa-comments'
    temp_button['href'] = project['discussion']
    button_div.append(temp_button)

    # Repo button
    temp_button = soup.new_tag('a')
    temp_button['role'] = 'button'
    temp_button['style'] = 'min-width: 24px'
    temp_button['class'] = 'btn btn-default'
    temp_button['data-toggle'] = 'tooltip'
    temp_button['data-container'] = 'body'
    temp_button['data-placement'] = 'top'
    temp_button['title'] = 'GitHub repository'
    temp_button.append(soup.new_tag('i'))
    #temp_button.append('GitHub')
    temp_button.i['class'] = 'fa fa-github-alt'
    temp_button['href'] = project['repo-url']
    temp_button['target'] = '_blank'
    button_div.append(temp_button)

    # Repo button
    temp_button = soup.new_tag('a')
    temp_button['role'] = 'button'
    temp_button['style'] = 'min-width: 24px'
    temp_button['class'] = 'btn btn-default'
    temp_button['data-toggle'] = 'tooltip'
    temp_button['data-container'] = 'body'
    temp_button['data-placement'] = 'top'
    temp_button['title'] = 'Latest release'
    temp_button.append(soup.new_tag('i'))
    #temp_button.append('GitHub')
    temp_button.i['class'] = 'fa fa-briefcase'
    temp_button['href'] = project['repo-url'] + '/releases/latest'
    temp_button['target'] = '_blank'
    button_div.append(temp_button)

    # Download button
    temp_button = soup.new_tag('a')
    temp_button['role'] = 'button'
    temp_button['class'] = 'btn btn-default dropdown-toggle'
    temp_button['data-toggle'] = 'dropdown'
    temp_button['aria-haspopup'] = 'true'
    temp_button['aria-expanded'] = 'false'
    #temp_button['title'] = 'Dowload the latest {} version'.format(project['version'])
    temp_button.append(soup.new_tag('i'))
    #temp_button.append('Download')
    temp_button.i['class'] = 'fa fa-download'
    temp_button.append(soup.new_tag('span'))
    temp_button.span['class'] = 'caret'
    temp_button.span['style'] = 'margin-left: 4px'
    temp_button['href'] = '#'
    button_div.append(temp_button)

    add_button_dropdown(button_div, project, soup)


def add_button_dropdown(button_div, project, soup):
    button_dropdown = soup.new_tag('ul')
    button_dropdown['class'] = 'dropdown-menu'
    button_div.append(button_dropdown)

    # Adding assets
    if project['assets']:
        for asset in project['assets']:
            li = soup.new_tag('li')
            li.append(soup.new_tag('a'))
            li.a['href'] = asset['download-url']
            li.a.append(soup.new_tag('i'))
            li.a.i['class'] = 'fa fa-star'
            li.a.append(asset['file-name'])
            li.a.append(soup.new_tag('small'))
            li.a.small.append(' ({}, '.format(size(asset['size'])))
            #li.a.small.append(' Downloaded: ')
            li.a.small.append(soup.new_tag('i'))
            li.a.small.i['class'] = 'fa fa-arrow-down'
            li.a.small.append('{})'.format(asset['download-count']))
            button_dropdown.append(li)
        # Adding a separator
        # separator = soup.new_tag('li')
        # separator['role'] = 'separator'
        # separator['class'] = 'divider'
        # button_dropdown.append(separator)

    # Adding source download
    li = soup.new_tag('li')
    li.append(soup.new_tag('a'))
    li.a['href'] = project['source-link']
    li.a.append(soup.new_tag('i'))
    li.a.i['class'] = 'fa fa-file-archive-o'
    li.a.append(' Source code')
    li.a.append(soup.new_tag('small'))
    li.a.small.append(' ({})'.format(project['version']))
    button_dropdown.append(li)


def add_tag_field(panel_body, project, soup):
    tag_field = soup.new_tag('div')
    for tag in project['tags']:
        tag_span = soup.new_tag('span')
        tag_span['class'] = 'label label-default'
        tag_span['style'] = 'margin-right: 4px'
        tag_span.string = tag
        tag_field.append(tag_span)
    panel_body.append(tag_field)


def add_panel_heading(panel, project, soup):
    panel_heading = soup.new_tag('div')
    panel_heading['class'] = 'panel-heading'
    panel_heading['style'] = 'background-color: white' if project['state'] != 'private' else ''
    panel_heading['role'] = 'tab'
    panel_heading['id'] = 'TSPR{:06}-heading'.format(project['id'])
    panel_heading.string = 'TSPR{:06}'.format(project['id'])
    if project['state'] == 'private':
        panel_heading['class'] += ' disabled'
    panel.append(panel_heading)

    add_badge(panel_heading, project, soup)
    add_details_button(panel_heading, project, soup)


def add_details_button(panel_heading, project, soup):
    button = soup.new_tag('button')
    button.string = 'Details'
    button['type'] = 'button'
    button['class'] = 'btn btn-default btn-lg btn-xs pull-right'
    button['data-toggle'] = 'collapse'
    button['data-parent'] = '#tspr-accordion'
    button['href'] = '#TSPR{:06}-collapse'.format(project['id'])
    button['aria-expanded'] = 'true'
    button['aria-controls'] = 'TSPR{:06}-collapse'.format(project['id'])
    if project['state'] == 'private':
        button['disabled'] = 'disabled'
    panel_heading.append(button)


def add_badge(panel_heading, project, soup):
    badge_abbr = soup.new_tag('abbr')
    badge = soup.new_tag('i')
    badge_abbr.append(badge)
    if project['state'] == 'private':
        badge_abbr['title'] = 'Private project'
        badge['class'] = 'pull-right fa fa-eye-slash'
    elif project['state'] == 'in-progress':
        badge_abbr['title'] = 'Work in progress'
        badge['class'] = 'pull-right fa fa-cogs'
    elif project['state'] == 'released':
        badge_abbr['title'] = 'Released. Latest version: {}'.format(project['version'])
        badge['class'] = 'pull-right fa fa-briefcase'
    badge['style'] = 'margin-left: 10px'
    panel_heading.append(badge_abbr)


def register():
    signals.content_object_init.connect(add_worklog_project_list)
