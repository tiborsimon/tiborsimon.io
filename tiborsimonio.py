#!usr/bin/env/ python3

import requests
import pickle
import json
import time
import datetime

from pprint import pprint, pformat

class Store(object):
    storage_file = 'tspr-store.pickle'
    project_file = '../../tspr.json'

    def __init__(self):
        self.projects = []

    def __str__(self):
        return pformat(self.projects)

    @classmethod
    def load(cls):
        print('Loading TSPR data..')
        try:
            store = pickle.load(open(cls.storage_file, 'rb'))
            store.sync_with_json(json.load(open(cls.project_file)))
            #store.sync_with_github()
            store.save()
            return store
        except FileNotFoundError:
            new_store = Store()
            new_store.sync_with_json(json.load(open(cls.project_file)))
            new_store.sync_with_github()
            new_store.save()
            return new_store

    @classmethod
    def sync(cls):
        print('TSPR GitHub sync started..')
        try:
            store = pickle.load(open(cls.storage_file, 'rb'))
            store.sync_with_github()
            store.save()
            return store
        except FileNotFoundError:
            new_store = Store()
            new_store.sync_with_json(json.load(open(cls.project_file)))
            new_store.sync_with_github()
            new_store.save()
            return new_store

    def save(self):
        pickle.dump(self, open(self.storage_file, 'wb'))

    @staticmethod
    def _get_timestamp(raw=False):
        if raw:
            return time.time()
        else:
            return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def sync_with_json(self, init_json):
        temp = []
        try:
            for p in init_json:
                t = {
                    'id':          p['id'],
                    'title':       p['title'],
                    'description': p['description'],
                    'tags':        p['tags'],
                    'state':       p['state'],
                    'repo-name':   p['repo-name'],
                    'article':     p['article'],
                    'tspr':        p['tspr'],
                    'docs':        p['docs'],
                    'history':     p['history']
                }
                temp.append(t)
        except (TypeError, KeyError):
            print('PARSE ERROR: invalid JSON structure! Sync failed! Old version did not changed!')
            return

        temp = sorted(temp, key=lambda k: k['id'])

        j = 0
        for i in range(temp[-1]['id']):
            if i == len(self.projects):
                self.projects.append({})
            if i+1 == temp[j]['id']:
                self.projects[i].update({
                    'id':          temp[j]['id'],
                    'title':       temp[j]['title'],
                    'description': temp[j]['description'],
                    'tags':        temp[j]['tags'],
                    'state':       temp[j]['state'],
                    'repo-name':   temp[j]['repo-name'],
                    'article':     temp[j]['article'],
                    'discussion':  '{}#discussion'.format(temp[j]['article']),
                    'tspr':        temp[j]['tspr'],
                    'docs':        temp[j]['docs'],
                    'history':     temp[j]['history']
                })
                j += 1
            else:
                self.projects[i] = {'id': i+1, 'state': 'private', 'tspr': 0, 'title': 'Private project'}

    def sync_with_github(self):
        request_counter = 0
        for project in self.projects:
            if project['state'] == 'released' or project['state'] == 'tspr':
                url = 'https://api.github.com/repos/tiborsimon/' + project['repo-name'] + '/releases/latest'

                try:
                    if 'etag' in project:
                        headers = {'If-None-Match': project['etag']}
                        r = requests.get(url, headers=headers)
                    else:
                        r = requests.get(url)
                except requests.exceptions.ConnectionError:
                    print('  Error: Connection could not be established to GitHub. Old project data remained..')
                    return

                if r.status_code == 304:
                    print('  [304] - {} is already up to date'.format(project['title']))
                elif r.status_code == 200:
                    request_counter += 1
                    print('  [200] - {} synced with GitHub'.format(project['title']))
                    project['etag'] = r.headers['ETag']
                    resp = r.json()
                    project['repo-url'] = resp['html_url'].split('/releases')[0]
                    project['source-link'] = resp['zipball_url']
                    project['version'] = resp['tag_name']
                    project['published-at'] = resp['published_at']
                    project['assets'] = []
                    for asset in resp['assets']:
                        project['assets'].append({
                            'url': asset['url'],
                            'download-url': asset['browser_download_url'],
                            'file-name': asset['name'],
                            'size': asset['size'],
                            'download-count': asset['download_count'],
                            'updated-at': asset['updated_at']
                        })
                else:
                    print('Failed to get response from GitHub. Error: {} with project {}'.format(r.status_code, project['title']))

        print('TSPR GitHub sync finished with {} API requests. {}/{} remained available in this hour.'.format(request_counter,
                                                                                                              r.headers['X-RateLimit-Remaining'],
                                                                                                              r.headers['X-RateLimit-Limit']))

if __name__ == '__main__':
    store = Store.load()
    print(store)

if __name__ == "__main__":
    main()
