from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    # Storing settings as key/value pairs
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'key': self.setting_key,
            'value': self.setting_value,
            'description': self.description
        }

class ContentBlock(db.Model):
    __tablename__ = 'content_blocks'
    id = db.Column(db.Integer, primary_key=True)
    block_key = db.Column(db.String(100), unique=True, nullable=False)
    content_text = db.Column(db.Text, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'key': self.block_key,
            'content': self.content_text,
            'description': self.description
        }

class ImageAsset(db.Model):
    __tablename__ = 'image_assets'
    id = db.Column(db.Integer, primary_key=True)
    asset_key = db.Column(db.String(100), unique=True, nullable=False) # e.g. "hero_background"
    file_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'key': self.asset_key,
            'url': f"/static/uploads/{self.file_path}",
            'description': self.description
        }

class Page(db.Model):
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    meta_description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Published')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sections = db.relationship('Section', backref='page', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'meta_description': self.meta_description,
            'status': self.status,
            'sections': [s.to_dict() for s in self.sections]
        }

class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'), nullable=False)
    section_name = db.Column(db.String(100), nullable=False)
    section_type = db.Column(db.String(50))
    content_json = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'section_name': self.section_name,
            'section_type': self.section_type,
            'content': json.loads(self.content_json) if self.content_json else {},
            'order': self.order
        }

class Inquiry(db.Model):
    __tablename__ = 'inquiries'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    interest_area = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'interest_area': self.interest_area,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }
