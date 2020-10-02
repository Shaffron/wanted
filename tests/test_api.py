import unittest

from app import app, db
from app.models import Company, Tag


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # 테스트 환경구축의 편의성을 위해 sqlite 의 in-memory db 사용
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

        cls.client = app.test_client()

        return

    def setUp(self):
        super().setUp()
        db.drop_all()
        db.create_all()
        self.prepare_data()

        return

    def prepare_data(self):
        self.company_data = {
            'company_ko': '원티드랩',
            'company_en': 'WantedLab',
            'company_ja': None,
            'tag_ko': '태그_4|태그_20|태그_16',
            'tag_en': 'tag_4|tag_20|tag_16',
            'tag_ja': 'タグ_4|タグ_20|タグ_16'
        }
        insert_stmt = Company.__table__.insert().values(**self.company_data)
        result = db.session.execute(insert_stmt)
        self.company_id = result.lastrowid

        tag_objects = [
            Tag(company_id=self.company_id, title='태그_4', type='ko'),
            Tag(company_id=self.company_id, title='태그_20', type='ko'),
            Tag(company_id=self.company_id, title='태그_16', type='ko'),
            Tag(company_id=self.company_id, title='tag_4', type='en'),
            Tag(company_id=self.company_id, title='tag_20', type='en'),
            Tag(company_id=self.company_id, title='tag_16', type='en'),
            Tag(company_id=self.company_id, title='タグ_4', type='ja'),
            Tag(company_id=self.company_id, title='タグ_20', type='ja'),
            Tag(company_id=self.company_id, title='タグ_16', type='ja'),
        ]
        db.session.bulk_save_objects(tag_objects)

        db.session.commit()

        return

    def test_search_all_companies(self):
        # When
        response = self.client.get('/api/companies')
        payload = response.json

        # Then
        data = self.company_data
        data['id'] = self.company_id
        expect = [data]
        self.assertEqual(payload, expect)

        return

    def test_search_by_name(self):
        # When (Korean)
        response = self.client.get('/api/companies?keyword=원티드&category=name')
        payload = response.json

        # Then
        data = self.company_data
        data['id'] = self.company_id
        expect = [data]
        self.assertEqual(payload, expect)

        return

    def test_search_by_tag(self):
        # When (Korean)
        response = self.client.get('/api/companies?keyword=태그_4&category=tag')
        payload = response.json

        # Then
        data = self.company_data
        data['id'] = self.company_id
        expect = [data]
        self.assertEqual(payload, expect)

        # When (English)
        response = self.client.get('/api/companies?keyword=tag_20&category=tag')
        payload = response.json

        # Then
        self.assertEqual(payload, expect)

        # When (Japanese)
        response = self.client.get('/api/companies?keyword=タグ_16&category=tag')
        payload = response.json

        # Then
        self.assertEqual(payload, expect)

        return

    def test_insert_tag(self):
        # When (Korean)
        insert_response = self.client.post(f'/api/companies/{self.company_id}/tag', data={'tag': '태그_100'})

        # Then
        self.assertEqual(insert_response.status_code, 201)

        search_response = self.client.get('/api/companies')
        payload = search_response.json.pop(0)

        self.assertTrue('태그_100' in payload['tag_ko'])
        self.assertTrue('tag_100' in payload['tag_en'])
        self.assertTrue('タグ_100' in payload['tag_ja'])

        # When (English)
        insert_response = self.client.post(f'/api/companies/{self.company_id}/tag', data={'tag': 'tag_101'})
        self.assertEqual(insert_response.status_code, 201)

        search_response = self.client.get('/api/companies')
        payload = search_response.json.pop(0)

        self.assertTrue('태그_101' in payload['tag_ko'])
        self.assertTrue('tag_101' in payload['tag_en'])
        self.assertTrue('タグ_101' in payload['tag_ja'])

        # When (Japanese)
        insert_response = self.client.post(f'/api/companies/{self.company_id}/tag', data={'tag': 'タグ_102'})
        self.assertEqual(insert_response.status_code, 201)

        search_response = self.client.get('/api/companies')
        payload = search_response.json.pop(0)

        self.assertTrue('태그_102' in payload['tag_ko'])
        self.assertTrue('tag_102' in payload['tag_en'])
        self.assertTrue('タグ_102' in payload['tag_ja'])

        return

    def test_delete_tag(self):
        # When (Korean)
        insert_response = self.client.post(f'/api/companies/{self.company_id}/tag', data={'tag': '태그_100'})
        self.assertEqual(insert_response.status_code, 201)

        delete_response = self.client.delete(f'/api/companies/{self.company_id}/tag', data={'tag': '태그_100'})

        # Then
        self.assertEqual(delete_response.status_code, 200)
        search_response = self.client.get('/api/companies')
        payload = search_response.json.pop(0)

        self.assertTrue('태그_100' not in payload['tag_ko'])
        self.assertTrue('tag_100' not in payload['tag_en'])
        self.assertTrue('タグ_100' not in payload['tag_ja'])

        # When (English)
        insert_response = self.client.post(f'/api/companies/{self.company_id}/tag', data={'tag': 'tag_101'})
        self.assertEqual(insert_response.status_code, 201)

        delete_response = self.client.delete(f'/api/companies/{self.company_id}/tag', data={'tag': 'tag_101'})

        # Then
        self.assertEqual(delete_response.status_code, 200)
        search_response = self.client.get('/api/companies')
        payload = search_response.json.pop(0)

        self.assertTrue('태그_101' not in payload['tag_ko'])
        self.assertTrue('tag_101' not in payload['tag_en'])
        self.assertTrue('タグ_101' not in payload['tag_ja'])

        # When (Japanese)
        insert_response = self.client.post(f'/api/companies/{self.company_id}/tag', data={'tag': 'タグ_102'})
        self.assertEqual(insert_response.status_code, 201)

        delete_response = self.client.delete(f'/api/companies/{self.company_id}/tag', data={'tag': 'タグ_102'})

        # Then
        self.assertEqual(delete_response.status_code, 200)
        search_response = self.client.get('/api/companies')
        payload = search_response.json.pop(0)

        self.assertTrue('태그_102' not in payload['tag_ko'])
        self.assertTrue('tag_102' not in payload['tag_en'])
        self.assertTrue('タグ_102' not in payload['tag_ja'])

        return
