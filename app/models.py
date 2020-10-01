from dataclasses import dataclass

from sqlalchemy import UniqueConstraint

from app import db


@dataclass
class Company(db.Model):
    id: int
    company_ko: str
    company_en: str
    company_ja: str
    tag_ko: str
    tag_en: str
    tag_ja: str

    id = db.Column(db.Integer, primary_key=True)
    company_ko = db.Column(db.String(100), nullable=True, index=True)
    company_en = db.Column(db.String(100), nullable=True, index=True)
    company_ja = db.Column(db.String(100), nullable=True, index=True)
    tag_ko = db.Column(db.TEXT, nullable=True)
    tag_en = db.Column(db.TEXT, nullable=True)
    tag_ja = db.Column(db.TEXT, nullable=True)

    tags = db.relationship("Tag")

    __tablename__ = "company"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}


@dataclass
class Tag(db.Model):
    id: int
    company_id: int
    title: str
    type: str

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    title = db.Column(db.String(100), nullable=False, index=True)
    type = db.Column(db.String(100), nullable=False)

    parent = db.relationship("Company", back_populates="tags", lazy="joined", innerjoin=True)

    UniqueConstraint(company_id, title)

    __tablename__ = "tag"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
