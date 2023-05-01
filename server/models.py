from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    #!Write Validations here:
    #All Authors have a name
    #No two Authors have the same name
    @validates('name')
    def validate_name(self, key, name_value):
        all_names = db.session.query(Author.name).all()
        # all_names = [author.name for author in all_authors]
        if not name_value:
            raise ValueError("Must have name entry")
        elif name_value in all_names:
            raise ValueError("Author already exists, enter new name")
        return name_value
            
    #Author phone numbers are exactly 10 digits
    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number MUST be 10 digits")
    

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
    
    #!Write Validations here:
    # All posts have a title => nullable=false already covers this
    @validates('title')
    def validate_title(self, key, title):
        title_strings = ["Won't Believe", "Secret", "Top", "Guess"]
        for clickbait in title_strings:
            if clickbait not in title:
                raise ValueError("Title Does not containt clickbait terms")
        return title
    # @validates('title')
    # def validate_title(self, key, title):
    #     clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
    #     if not any(substring in title for substring in clickbait):
    #         raise ValueError("No clickbait found")
    #     return title
            
    # Post content is at least 250 characters long
    @validates('content')
    def _validate_content(self, key, content_value):
        if len(content_value) <= 250:
            raise ValueError("Content must be at least 250 characters long")
        return content_value
    
    #Post summary is a max of 250 characters
    @validates('summary')
    def _validate_summary(self, key, summary_value):
        if len(summary_value) >= 250:
            raise ValueError("Content can only be  250 characters long")
        return summary_value
    #Post category is fiction or non-fiction
    @validates('category')
    def _validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("category must be Fiction or Non-Fiction")
        return category
    
    
    # @validates('content', 'summary')
    # def validate_length(self, key, string):
    #     if( key == 'content'):
    #         if len(string) <= 250:
    #             raise ValueError("Post content must be greater than or equal 250 characters long.")
    #     if( key == 'summary'):
    #         if len(string) >= 250:
    #             raise ValueError("Post summary must be less than or equal to 250 characters long.")
    #     return string

    # @validates('category')
    # def validate_category(self, key, category):
    #     if category != 'Fiction' and category != 'Non-Fiction':
    #         raise ValueError("Category must be Fiction or Non-Fiction.")
    #     return category



