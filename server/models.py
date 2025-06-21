from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty.")

        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        existing = Author.query.filter_by(name=name).first()
        if existing and existing.id != getattr(self, 'id', None):
            raise ValueError("Name must be unique.")

        return name



    @validates('phone_number')
    def test_requires_ten_digit_phone_number(self, key, phone_number):
        if not isinstance(phone_number, str) or len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be a string of exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('title')
    def validate_title(self, key, title_value):

        if not title_value and title_value.strip() == "":
            raise ValueError("Title cannot be empty")
        
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title_value for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait-y and contain one of: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        
        return title_value
    
    @validates('content')
    def validate_content(self, key, content_value):
        if not isinstance(content_value, str) or len(content_value) < 250:
            raise ValueError("Content is too short")
        return content_value
    
    @validates('summary')
    def validate_summary(self, key, summary_value):
        if not isinstance(summary_value, str) or  len(summary_value) > 250:
            raise ValueError("summary is too long")
        return summary_value
    
    @validates('category')
    def validate_catergory(self, key, category_option):
        allowed = ["Fiction", "Non-Fiction"]
        if category_option not in allowed:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'")
        return category_option



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
