import unittest
from pprint import pprint

from tspr import Store

class SyncWithJsonTests(unittest.TestCase):
    def setUp(self):
        self.store = Store()

    def test__sync_with_json__one_project(self):
        init_json = [
            {
                'id': 1,
                'title': 'title1',
                'description': 'description1',
                'tags': ['tag11', 'tag12'],
                'state': 'in-progress',
                'repo-name': 'repo1'
            }
        ]

        self.store.sync_with_json(init_json)

        self.assertEqual(1, len(self.store.projects))
        self.assertEqual(init_json[0], self.store.projects[0])

    def test__sync_with_json__one_project_with_offset(self):
        init_json = [
            {
                'id': 2,
                'title': 'title1',
                'description': 'description1',
                'tags': ['tag11', 'tag12'],
                'state': 'in-progress',
                'repo-name': 'repo1'
            }
        ]

        self.store.sync_with_json(init_json)

        self.assertEqual(2, len(self.store.projects))
        self.assertEqual({'id': 1, 'state': 'private'}, self.store.projects[0])
        self.assertEqual(init_json[0], self.store.projects[1])

    def test__sync_with_json__one_project_with_two_offsets(self):
        init_json = [
            {
                'id': 3,
                'title': 'title1',
                'description': 'description1',
                'tags': ['tag11', 'tag12'],
                'state': 'in-progress',
                'repo-name': 'repo1'
            }
        ]

        self.store.sync_with_json(init_json)

        self.assertEqual(3, len(self.store.projects))
        self.assertEqual({'id': 1, 'state': 'private'}, self.store.projects[0])
        self.assertEqual({'id': 2, 'state': 'private'}, self.store.projects[1])
        self.assertEqual(init_json[0], self.store.projects[2])

    def test__sync_with_json_do_not_overrides_other_entries(self):
        init_json = [
            {
                'id': 1,
                'title': 'title1',
                'description': 'description1',
                'tags': ['tag11', 'tag12'],
                'state': 'in-progress',
                'repo-name': 'repo1'
            }
        ]

        self.store.projects.append({'something': 42})

        self.store.sync_with_json(init_json)

        self.assertEqual(1, len(self.store.projects))
        self.assertEqual(42, self.store.projects[0]['something'])

    def test__missing_mandatory_key__invalidates_sync_process(self):
        init_json = [
            {
                'id': 1,
                'description': 'description1',
                'tags': ['tag11', 'tag12'],
                'state': 'in-progress',
                'repo-name': 'repo1'
            }
        ]

        self.store.projects.append({'something': 42})

        self.store.sync_with_json(init_json)

        self.assertEqual(1, len(self.store.projects))
        self.assertEqual({'something': 42}, self.store.projects[0])

