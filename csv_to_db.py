import csv
from collections import defaultdict
from typing import List, Optional

from flask_script import Command

from app.constants import LANGUAGE


class Immigration(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # prevent circular import
        from app.models import Company, db, Tag
        self.Company = Company
        self.Tag = Tag
        self.db = db

        return

    def run(self):
        payload = self.parse_csv()

        self.insert_company(payload)
        self.db.session.commit()

        return

    def parse_csv(self) -> List[dict]:
        payload = []

        with open('./wanted_temp_data.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for line, row in enumerate(reader):
                if line == 0:
                    columns = row
                    continue

                else:
                    data = defaultdict()
                    for index, item in enumerate(row):
                        data[columns[index]] = item or None

                    payload.append(data)

        return payload

    def insert_company(self, payload: List[dict]):
        for data in payload:
            insert_stmt = self.Company.__table__.insert().values(**data)
            result = self.db.session.execute(insert_stmt)
            pk = result.inserted_primary_key.pop()

            self.insert_tags(pk, data)

        self.db.session.commit()
        return

    def insert_tags(self, company_id: int, payload: dict):
        tag_objects = []

        tag_objects.extend(self.create_tag_object(company_id, payload.get('tag_ko'), LANGUAGE.KOREAN))
        tag_objects.extend(self.create_tag_object(company_id, payload.get('tag_en'), LANGUAGE.ENGLISH))
        tag_objects.extend(self.create_tag_object(company_id, payload.get('tag_ja'), LANGUAGE.JAPANESE))

        self.db.session.bulk_save_objects(tag_objects)

        return

    def create_tag_object(self, company_id: int, tags: Optional[str], category: str) -> List['Tag']:
        if not tags:
            return []

        else:
            tag_objects = []
            tag_list = tags.split('|')

            for tag in tag_list:
                tag_objects.append(self.Tag(company_id=company_id, title=tag, type=category))

            return tag_objects
