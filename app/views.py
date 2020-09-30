from flask_restplus import Namespace
from app.company import CompaniesView, CompanyView

namespace = Namespace('company', description='company search api')
namespace.add_resource(CompaniesView, '/companies')
namespace.add_resource(CompanyView, '/companies/<int:id>')
