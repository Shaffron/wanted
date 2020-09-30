from flask import jsonify
from flask_restplus import Resource

from app.models import Company


class CompaniesView(Resource):
    def get(self):
        companies = Company.query.all()
        return jsonify(companies)


class CompanyView(Resource):
    def get(self, id):
        return {}

    def put(self, id):
        return {}

    def delete(self, id):
        return {}