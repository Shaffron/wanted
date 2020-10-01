import re
from typing import List, Optional, Tuple

from flask import jsonify
from flask_restplus import abort, Resource, reqparse, ValidationError
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.visitors import VisitableType

from app import db
from app.constants import LANGUAGE, WORD
from app.models import Company, Tag


class CompaniesView(Resource):
    def get(self):
        args = self.parse_arguments()

        if self.is_arguments_empty(args):
            companies = Company.query.all()
            return jsonify(companies)

        else:
            keyword = args.get('keyword')
            category = args.get('category')

            if not keyword or not category:
                abort(400, 'keyword and category are pair')

            companies: List[Optional[dict]]

            if category == 'name':
                query = f'%{keyword}%'
                companies = Company.query.filter(
                    or_(
                        Company.company_ko.like(query),
                        Company.company_en.like(query),
                        Company.company_ja.like(query)
                    )
                ).all()
                return jsonify(companies)

            elif category == 'tag':
                companies = Company.query.join(
                    Company.tags
                ).filter(
                    Tag.title == keyword
                ).order_by(
                    Company.id
                ).all()
                return jsonify(companies)

    def parse_arguments(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', required=False, type=str)
        parser.add_argument('category', required=False, type=str, choices=('name', 'tag'))
        args = parser.parse_args()

        return args

    def is_arguments_empty(self, args: dict) -> bool:
        values = args.values()
        is_empty = not all(values)

        return is_empty


class CompanyView(Resource):
    def post(self, company_id):
        company = self.get_or_404(company_id)
        args = self.parse_arguments()

        try:
            tag = args.get('tag')
            language, tag_num = self.validate_tag_format(tag)

            insert_stmt = Tag.__table__.insert().values(company_id=company.id, title=tag, type=language)
            db.session.execute(insert_stmt)

            update_stmt = self.add_tag(company, tag_num)
            db.session.execute(update_stmt)

            db.session.commit()

        except IntegrityError:
            abort(409, f'Company(ID: {company_id}) already has tag "{tag}"')

        except Exception :
            abort(500, 'Internal Server Error')

        return None, 201

    def delete(self, company_id: int):
        company = self.get_or_404(company_id)
        args = self.parse_arguments()

        try:
            tag = args.get('tag')
            language, tag_num = self.validate_tag_format(tag)

            element = Tag.query.filter(
                Tag.company_id == company.id,
                Tag.title == tag,
                Tag.type == language
            ).first()

            if not element:
                abort(404, f'Company ID({company_id}) does not have tag ({tag})')

            delete_stmt = Tag.__table__.delete().where(Tag.id == element.id)
            db.session.execute(delete_stmt)

            update_stmt = self.delete_tag(company, tag_num)
            db.session.execute(update_stmt)

            db.session.commit()

        except IntegrityError:
            abort(409, f'Company ID({company_id}) does not have tag ({tag})')

        return None, 200

    def get_or_404(self, company_id: int) -> Optional[Company]:
        company = Company.query.get(company_id)

        if not company:
            abort(404, f'Company ID({company_id}) not exist')

        return company

    def parse_arguments(self) -> dict:
        parser = reqparse.RequestParser()
        parser.add_argument('tag', required=True, type=str)
        args = parser.parse_args()

        return args

    def validate_tag_format(self, tag: str) -> Tuple[str, int]:
        regex = re.compile(r'(태그|tag|タグ)_\d+')
        matched = regex.match(tag)

        if not matched:
            raise ValidationError('invalid tag format. format must be {태그|tag|タグ}_{number} ')

        word, number = tag.split('_')
        language = self.check_language_type(word)

        return language, number

    def check_language_type(self, word: str) -> str:
        language: str

        if word == WORD.KOREAN:
            language = LANGUAGE.KOREAN

        elif word == WORD.ENGLISH:
            language = LANGUAGE.ENGLISH

        elif word == WORD.JAPANESE:
            language = LANGUAGE.JAPANESE

        return language

    def add_tag(self, company: Company, tag_num: int) -> VisitableType:
        korean_tags = company.tag_ko + f'|{WORD.KOREAN}_{tag_num}'
        english_tags = company.tag_en + f'|{WORD.ENGLISH}_{tag_num}'
        japanese_tags = company.tag_ja + f'|{WORD.JAPANESE}_{tag_num}'

        stmt = Company.__table__.update().where(
            Company.id == company.id
        ).values(
            tag_ko=korean_tags, tag_en=english_tags, tag_ja=japanese_tags
        )

        return stmt

    def delete_tag(self, company: Company, tag_num: int):
        korean_tags = self.delete_tag_in_tags(company.tag_ko, f'태그_{tag_num}')
        english_tags = self.delete_tag_in_tags(company.tag_en, f'tag_{tag_num}')
        japanese_tags = self.delete_tag_in_tags(company.tag_ja, f'タグ_{tag_num}')

        stmt = Company.__table__.update().where(
            Company.id == company.id
        ).values(
            tag_ko=korean_tags, tag_en=english_tags, tag_ja=japanese_tags
        )

        return stmt

    def delete_tag_in_tags(self, tags: str, tag: str) -> str:
        tag_list = tags.split('|')
        target_tag_index = tag_list.index(tag)
        tag_list.pop(target_tag_index)
        assembled_tags = '|'.join(tag_list)

        return assembled_tags
