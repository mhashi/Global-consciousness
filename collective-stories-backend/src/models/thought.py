from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Thought(db.Model):
    __tablename__ = 'thoughts'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500))  # Comma-separated tags
    is_anonymous = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(100))  # City, Country
    ip_address = db.Column(db.String(45))  # For location detection
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used_in_story = db.Column(db.Boolean, default=False)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'tags': self.tags.split(',') if self.tags else [],
            'is_anonymous': self.is_anonymous,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'used_in_story': self.used_in_story
        }

class Story(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    contributor_count = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationship to thoughts
    thoughts = db.relationship('Thought', backref='story', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'excerpt': self.excerpt,
            'created_at': self.created_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'contributor_count': self.contributor_count,
            'is_published': self.is_published
        }

