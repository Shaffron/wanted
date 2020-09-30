from dataclasses import dataclass

from app import db


@dataclass
class Company(db.Model):
    id: int
    company_name_ko: str
    company_name_en: str
    company_name_ja: str
    company_tag_ko: str
    company_tag_en: str
    company_tag_ja: str

    id = db.Column(db.Integer, primary_key=True)
    company_name_ko = db.Column(db.String(100), nullable=True, index=True)
    company_name_en = db.Column(db.String(100), nullable=True, index=True)
    company_name_ja = db.Column(db.String(100), nullable=True, index=True)
    company_tag_ko = db.Column(db.TEXT, nullable=True)
    company_tag_en = db.Column(db.TEXT, nullable=True)
    company_tag_ja = db.Column(db.TEXT, nullable=True)

    __tablename__ = "company"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
