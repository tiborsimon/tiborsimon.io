from pelican import signals
from bs4 import BeautifulSoup
from hurry.filesize import size

from tiborsimonio import Store

Store.project_file = 'tspr.json'
store = Store.load()


def render(instance):
    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, 'html.parser')
        render_worklog_page(soup)
        reder_project_page(soup)
        instance._content = soup.prettify(formatter=None)


def register():
    signals.content_object_init.connect(render)


# =============================================================================
#    W O R K L O G   P R O C E S S O R
def render_worklog_page(soup):
    for tspr_div in soup.find_all('div', class_='pr-worklog'):
        print('TSPR rendering worklog content..')
        add_panel_group(soup, tspr_div)


def add_panel_group(soup, parent):
    panel_group = soup.new_tag('div')
    panel_group['class'] = 'panel-group'
    panel_group['id'] = 'pr-accordion'
    panel_group['role'] = 'tablist'
    panel_group['aria-multiselectable'] = 'true'
    parent.append(panel_group)
    for project in store.projects:
        add_panel(panel_group, project, soup)


def add_panel(parent, project, soup):
    panel = soup.new_tag('div')
    panel['class'] = 'panel panel-default'
    add_panel_heading(panel, project, soup)
    add_panel_collapse(panel, project, soup)
    parent.append(panel)


def add_panel_collapse(parent, project, soup):
    panel_collapse = soup.new_tag('div')
    panel_collapse['class'] = 'panel-collapse collapse'
    panel_collapse['role'] = 'tabpanel'
    panel_collapse['id'] = 'PR{:06}-collapse'.format(project['id'])
    panel_collapse['aria-labelledy'] = 'PR{:06}-heading'.format(project['id'])
    add_panel_body(panel_collapse, project, soup)
    parent.append(panel_collapse)


def add_panel_body(parent, project, soup):
    panel_body = soup.new_tag('div')
    panel_body['class'] = 'panel-body'
    parent.append(panel_body)

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


def add_buttons(parent, project, soup):
    button_p = soup.new_tag('p')
    parent.append(button_p)

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
    temp_button.append(soup.new_tag('i'))
    temp_button.i['class'] = 'fa fa-download'
    temp_button.append(soup.new_tag('span'))
    temp_button.span['class'] = 'caret'
    temp_button.span['style'] = 'margin-left: 4px'
    temp_button['href'] = '#'
    button_div.append(temp_button)

    add_button_dropdown(button_div, project, soup)


def add_button_dropdown(parent, project, soup):
    button_dropdown = soup.new_tag('ul')
    button_dropdown['class'] = 'dropdown-menu'
    parent.append(button_dropdown)

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
            li.a.small.append(soup.new_tag('i'))
            li.a.small.i['class'] = 'fa fa-arrow-down'
            li.a.small.append('{})'.format(asset['download-count']))
            button_dropdown.append(li)

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


def add_tag_field(parent, project, soup):
    tag_field = soup.new_tag('div')
    for tag in project['tags']:
        tag_span = soup.new_tag('span')
        tag_span['class'] = 'label label-default'
        tag_span['style'] = 'margin-right: 4px'
        tag_span.string = tag
        tag_field.append(tag_span)
    parent.append(tag_field)


def add_panel_heading(parent, project, soup):
    panel_heading = soup.new_tag('div')
    panel_heading['class'] = 'panel-heading'
    panel_heading['style'] = 'background-color: white' if project['state'] != 'private' else ''
    panel_heading['role'] = 'tab'
    panel_heading['id'] = 'PR{:06}-heading'.format(project['id'])
    panel_heading.string = 'PR{:06}'.format(project['id'])
    if project['state'] == 'private':
        panel_heading['class'] += ' disabled'
    parent.append(panel_heading)

    add_badge(panel_heading, project, soup)
    add_details_button(panel_heading, project, soup)


def add_details_button(parent, project, soup):
    button = soup.new_tag('button')
    button.string = 'Details'
    button['type'] = 'button'
    button['class'] = 'btn btn-default btn-lg btn-xs pull-right'
    button['data-toggle'] = 'collapse'
    button['data-parent'] = '#pr-accordion'
    button['href'] = '#PR{:06}-collapse'.format(project['id'])
    button['aria-expanded'] = 'true'
    button['aria-controls'] = 'PR{:06}-collapse'.format(project['id'])
    if project['state'] == 'private':
        button['disabled'] = 'disabled'
    parent.append(button)


def add_badge(parent, project, soup):
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
        if project['tspr'] > 0:
            badge_abbr['title'] = 'TSPR{:04} project. Released. Latest version: {}'.format(project['tspr'], project['version'])
            badge['class'] = 'pull-right fa fa-star'    
        else:
            badge_abbr['title'] = 'Released. Latest version: {}'.format(project['version'])
            badge['class'] = 'pull-right fa fa-briefcase'
    badge['style'] = 'margin-left: 10px; width: 12px' 
    parent.append(badge_abbr)


# =============================================================================
#    P R O J E C T   P R O C E S S O R
def reder_project_page(soup):
    render_tspr_projects(soup)
    render_all_project(soup)


def render_all_project(soup):
    for all_projects_div in soup.find_all('div', class_='all-projects'):
        print('TSPR rendering all projects..')
        for project in store.projects:
            project['project-title'] = 'PR{:06}'.format(project['id'])
            add_pr_project(all_projects_div, project, soup)
            add_modal(all_projects_div, project, soup)


def add_pr_project(parent, project, soup):
    list_group_item = create_list_group_item(parent, project, soup)
    add_ribbon(list_group_item, project, soup)
    add_project_icon(list_group_item, project, soup)
    add_project_title(list_group_item, project, soup)


def create_list_group_item(parent, project, soup):
    col_div = soup.new_tag('div')
    col_div['class'] = 'col-xs-6 col-sm-4 col-md-3'
    parent.append(col_div)
    list_group_div = soup.new_tag('div')
    list_group_div['class'] = 'list-group'
    list_group_div['style'] = 'overflow: hidden'
    col_div.append(list_group_div)
    if project['state'] != 'private':
        list_group_item = soup.new_tag('a')
        list_group_item['href'] = '#'
        list_group_item['class'] = 'list-group-item'
        list_group_item['data-toggle'] = 'modal'
        if project['tspr'] > 0:
            list_group_item['data-target'] = '#TSPR{:04}'.format(project['tspr'])
        else:
            list_group_item['data-target'] = '#' + project['project-title']
    else:
        list_group_item = soup.new_tag('div')
        list_group_item['class'] = 'list-group-item disabled'
    list_group_div.append(list_group_item)
    return list_group_item


def add_project_title(parent, project, soup):
    title_h4 = soup.new_tag('h4')
    title_h4['class'] = 'list-group-item-heading text-center'
    parent.append(title_h4)

    title_h4.string = project['project-title']
    title_h5 = soup.new_tag('h5')
    title_h5['class'] = 'list-group-item-heading text-center hidden-xs'
    title_h5['style'] = 'white-space: nowrap'
    parent.append(title_h5)

    title_h5.string = project['title']
    title_h6 = soup.new_tag('h6')
    title_h6['class'] = 'list-group-item-heading text-center visible-xs-block'
    title_h6['style'] = 'white-space: nowrap'
    parent.append(title_h6)

    title_h6.string = project['title']


def add_project_icon(parent, project, soup):
    icon_div = soup.new_tag('div')
    icon_div['class'] = 'text-center'
    icon_div['style'] = 'margin: 10px'
    parent.append(icon_div)
    badge = soup.new_tag('i')
    badge_abbr = soup.new_tag('abbr')
    badge_abbr.append(badge)
    icon_div.append(badge_abbr)
    badge_abbr['style'] = 'border: none !important'
    if project['state'] == 'private':
        badge_abbr['title'] = 'Private project'
        badge['class'] = 'fa fa-2x fa-eye-slash'
    elif project['state'] == 'in-progress':
        badge_abbr['title'] = 'Work in progress'
        badge['class'] = 'fa fa-2x fa-cog fa-spin'
    elif project['state'] == 'released':
        if project['tspr'] > 0:
            badge_abbr['title'] = 'TSPR{:04} project. Released. Latest version: {}'.format(project['tspr'],
                                                                                           project['version'])
            badge['class'] = 'fa fa-2x fa-star'
        else:
            badge_abbr['title'] = 'Released. Latest version: {}'.format(project['version'])
            badge['class'] = 'fa fa-2x fa-briefcase'


def add_ribbon(parent, project, soup):
    if project['state'] == 'released':
        ribbon = soup.new_tag('div')
        ribbon['class'] = 'project-version-ribbon'
        if project['tspr'] > 0:
            ribbon['class'] = 'project-version-ribbon tspr'
        ribbon.string = project['version']
        parent.append(ribbon)


def add_modal(parent, project, soup):
    if project['state'] == 'private':
        return

    modal_content_div = create_modal_content_div(parent, project, soup)
    add_modal_header(modal_content_div, project, soup)
    add_modal_body(modal_content_div, project, soup)
    add_modal_footer(modal_content_div, soup)


def add_modal_header(parent, project, soup):
    modal_header_div = soup.new_tag('div')
    modal_header_div['class'] = 'modal-header'
    parent.append(modal_header_div)
    upper_close_button = soup.new_tag('button')
    upper_close_button['class'] = 'close'
    upper_close_button['data-dismiss'] = 'modal'
    upper_close_button['aria-label'] = 'Close'
    modal_header_div.append(upper_close_button)
    upper_close_button.append(soup.new_tag('span'))
    upper_close_button.span['aria-hidden'] = 'true'
    upper_close_button.span.string = '&times;'
    modal_header_div.append(soup.new_tag('h4'))
    modal_header_div.h4['class'] = 'modal-title'
    modal_header_div.h4['id'] = 'myModalLabel'
    if project['tspr'] > 0:
        modal_header_div.h4.string = 'TSPR{:04} <small>'.format(project['tspr']) + project[
            'project-title'] + '</small> - ' + project['title']
    else:
        modal_header_div.h4.string = project['project-title'] + ' - ' + project['title']


def add_modal_body(modal_content_div, project, soup):
    modal_body_div = soup.new_tag('div')
    modal_body_div['class'] = 'modal-body'
    modal_content_div.append(modal_body_div)
    add_modal_body_content(modal_body_div, project, soup)


def add_modal_body_content(parent, project, soup):
    description_row = soup.new_tag('div')
    description_row['class'] = 'row'
    parent.append(description_row)

    description_div = soup.new_tag('div')
    description_div['class'] = 'col-xs-9'
    description_div.string = '<p>' + project['description'] + '</p>'
    description_row.append(description_div)

    add_tag_field(description_div, project, soup)

    description_icon_div = soup.new_tag('div')
    description_icon_div['class'] = 'col-xs-3 text-center'
    icon = soup.new_tag('i')
    icon_descr = soup.new_tag('p')
    icon_descr['style'] = 'font-size: 80%; opacity: 0.5'
    description_icon_div.append(icon)
    description_icon_div.append(icon_descr)

    if project['state'] == 'in-progress':
        icon['class'] = 'fa fa-3x fa-cog fa-spin'
        icon_descr.string = 'Work in progress'
    elif project['state'] == 'released':
        if project['tspr'] > 0:
            icon['class'] = 'fa fa-3x fa-star'
            icon_descr.string = 'TSPR project'
        else:
            icon['class'] = 'fa fa-3x fa-briefcase'
            icon_descr.string = 'Released project'
    description_row.append(description_icon_div)

    if project['state'] == 'released':
        add_buttons(parent, project, soup)


def add_modal_footer(parent, soup):
    modal_footer_div = soup.new_tag('div')
    modal_footer_div['class'] = 'modal-footer'
    parent.append(modal_footer_div)
    modal_footer_div.append(soup.new_tag('button'))
    modal_footer_div.button['type'] = 'button'
    modal_footer_div.button['class'] = 'btn btn-default btn-xs'
    modal_footer_div.button['data-dismiss'] = 'modal'
    modal_footer_div.button.string = 'Close'


def create_modal_content_div(parent, project, soup):
    modal_fade_div = soup.new_tag('div')
    modal_fade_div['class'] = 'modal fade'
    if project['tspr'] > 0:
        modal_fade_div['id'] = 'TSPR{:04}'.format(project['tspr'])
    else:
        modal_fade_div['id'] = project['project-title']
    modal_fade_div['tabIndex'] = '-1'
    modal_fade_div['role'] = 'dialog'
    modal_fade_div['aria-labelledby'] = 'myModalLabel'
    parent.append(modal_fade_div)
    modal_dialog_div = soup.new_tag('div')
    modal_dialog_div['class'] = 'modal-dialog'
    modal_dialog_div['role'] = 'document'
    modal_fade_div.append(modal_dialog_div)
    modal_content_div = soup.new_tag('div')
    modal_content_div['class'] = 'modal-content'
    modal_dialog_div.append(modal_content_div)
    return modal_content_div


def render_tspr_projects(soup):
    for tspr_div in soup.find_all('div', class_='tspr-projects'):
        print('TSPR rendering TSPR projects..')
        for project in [p for p in store.projects if p['tspr'] > 0]:
            add_tspr_project(tspr_div, project, soup)


def add_tspr_project(parent, project, soup):
    list_group_item = create_tspr_list_group_item(parent, project, soup)
    add_tspr_ribbon(list_group_item, project, soup)
    add_tspr_icon(list_group_item, project, soup)
    add_tspr_title(list_group_item, project, soup)


def create_tspr_list_group_item(parent, project, soup):
    col_div = soup.new_tag('div')
    parent.append(col_div)
    col_div['class'] = 'col-xs-12 col-sm-6 col-md-4'
    list_group_div = soup.new_tag('div')
    list_group_div['class'] = 'list-group'
    list_group_div['style'] = 'overflow: hidden'
    col_div.append(list_group_div)
    if project['state'] != 'private':
        list_group_item = soup.new_tag('a')
        list_group_item['href'] = '#'
        list_group_item['class'] = 'list-group-item'
        list_group_item['data-toggle'] = 'modal'
        list_group_item['data-target'] = '#TSPR{:04}'.format(project['tspr'])
    else:
        list_group_item = soup.new_tag('div')
        list_group_item['class'] = 'list-group-item disabled'
    list_group_div.append(list_group_item)
    return list_group_item


def add_tspr_icon(list_group_item, project, soup):
    icon_div = soup.new_tag('div')
    icon_div['class'] = 'text-center'
    icon_div['style'] = 'margin: 10px'
    list_group_item.append(icon_div)
    badge = soup.new_tag('i')
    badge_abbr = soup.new_tag('abbr')
    badge_abbr.append(badge)
    icon_div.append(badge_abbr)
    badge_abbr['style'] = 'border: none !important'
    badge_abbr['title'] = 'TSPR{:04} project. Released. Latest version: {}'.format(project['tspr'], project['version'])
    badge['class'] = 'fa fa-3x fa-star'


def add_tspr_ribbon(parent, project, soup):
    if project['state'] == 'released':
        ribbon = soup.new_tag('div')
        ribbon['class'] = 'project-version-ribbon tspr'
        ribbon.string = project['version']
        parent.append(ribbon)


def add_tspr_title(parent, project, soup):
    title_h3 = soup.new_tag('h3')
    title_h3['class'] = 'list-group-item-heading text-center'
    parent.append(title_h3)
    title_h3.string = 'TSPR{:04}'.format(project['tspr'])
    title_h4 = soup.new_tag('h4')
    title_h4['class'] = 'list-group-item-heading text-center'
    parent.append(title_h4)
    title_h4.string = project['title']

