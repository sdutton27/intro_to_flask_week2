from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
#db = SQLAlchemy(app)

# for followers
followers = db.Table('followers',
       db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
       db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable=False)              
)

# this name is actually lowercase
class User(db.Model, UserMixin):
                # datatype, any constraints
                # you can find the datatypes on SQLAlchemy
                # for example, String will cover VARCHAR
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    # next was added later to show how we update tables
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow) # default timestamp now
    # it has a Relationship to the post (can have multiple posts), for our reference
                        #what table are you connecting to(in "" as str, uppercase), backref=so we can eventually get the author of a post (who created it-> which instance of the User), lazy= True
    posts = db.relationship('Post', backref='author', lazy = True)
    # use the secondary to get the actual Post object
    liked_posts = db.relationship('Post', secondary='like', lazy=True)

    # get the list of people that I follow
    # we can also do secondary=followers since it's defined above lol        # get back the list of people that I follow
    followed = db.relationship('User',
                secondary='followers',
                lazy='dynamic',
                backref=db.backref('followers',
                lazy='dynamic'),        #c. is the column
                primaryjoin = (followers.c.follower_id == id), # this is the ON for a JOIN from SQL
                secondaryjoin=(followers.c.followed_id == id)
                )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() # actually commits things

    def follow(self, user):
        self.followed.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.followed.remove(user)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False) # since it's instagram we need photos
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow) # default timestamp now
                                                # table (lowercase).column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    # create a backref to the like object itself...but we only really care about the list of users who've liked something
    likers = db.relationship('Like', lazy = True)

    # another way:                   #model we are connecting to, # secondary = tablename of join table
    #people_who_liked = db.relationship('User', secondary='like')

    # for the Table.db
    likers_2 = db.relationship('User', secondary='like_2')

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit() # actually commits things

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_changes_to_db(self):
        db.session.commit()

    def to_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'caption' : self.caption,
            'img_url' : self.img_url,
            'author' : self.author.username, # we have this backref
            'likes' : len(self.likers), # how many people have liked a post
            'date_created' : self.date_created,
        }

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     post_id = db.Column(db.Integer, nullable=False) 
#     message = db.Column(db.String(300), nullable=False)

#lets make something called likes_2 just to try making a table instead
# 'likes' variable means nothing, can be called whatever
likes = db.Table('like_2', 
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False), 
                db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False))


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id 

    # No need to have an update function because we will not update who created a like

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()