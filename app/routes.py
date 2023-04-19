from flask import flash, get_flashed_messages, render_template, request, redirect, url_for
from app import app
from .forms import PostForm # GOTTA INCLUDE THIS
from .models import Post, User, Like
from flask_login import login_required, current_user

@app.route('/')
def homePage():
    users = User.query.all() # gives a list of all users


    return render_template('index.html', users=users)

# @app.route('/signup', methods=["GET", "POST"])
# def signupPage():
#     # instantiate the form
#     form = SignUpForm()
#     # if the method is POST, do something
#     #print(request.method)
#     if request.method == 'POST':
#         #print('valid post request made')
#         if form.validate(): # if the form is valid, this is True
#             username = form.username.data
#             email = form.email.data
#             password = form.password.data
            
#             user = User.query.filter_by(username = username).first()
#             if user:
#                 flash('That username is taken', 'danger')
#                 return render_template('signup.html', form = form)
#             user = User.query.filter_by(email = email).first()
#             if user:
#                 flash('That email is already in user. Please use another email', 'danger')
#                 return render_template('signup.html', form = form)

#             user = User(username, email, password)
#             #print(user)
#             user.save_to_db() # helper method

#             flash('Successfully created your account', 'success')

#             return redirect(url_for('loginPage'))

#         else:
#             flash('Invalid entry, please try again', 'danger')

#     # if the method is GET
#     return render_template('signup.html', form = form)


# @app.route('/login', methods=["GET", "POST"])
# def loginPage():
#     form = LoginForm()
#     if request.method == "POST":
#         if form.validate(): #if form is valid
#             username = form.username.data
#             password = form.password.data

#             # what we want: SELECT * FROM user WHERE username=username
#             # SQLAlchemy has a query that we can use
#             # <table we want it from>.query.<method>
#             # get() is only for primary key

#             # we know that username is unique so this will only give us 1
#             # but it will still return as a list so we have to do .first()
#             user = User.query.filter_by(username=username).first()
#             # method would go here if we were doing anything to user object
            

#             # returns either the instance of the user of None
#             if user: # user was found
#                 # verify password
#                 # looks at the password in the database = the password you sent in the form
#                 if user.password == password:
#                     # log in
#                     login_user(user) #login the user
#                     #print('log me in')

#                     # take the user back to the homepage
#                     return redirect(url_for('homePage'))
#                 else:
#                     # invalid password
#                     print('incorrect username(just for security) or password(true)')
#             else: # user was not found
#                 print('incorrect username(true) or password(just for security)')

#     return render_template('login.html', form = form)

# @app.route('/logout')
# def logMeOut():
#     logout_user()
#     # we don't want a render_template here because it would need a form and that's hectic
#     return redirect(url_for('loginPage'))

@app.route('/posts/create', methods=["GET", "POST"])
@login_required
def createPost():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            # create post and save to db
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            post.save_to_db()

            # takes you to your feed
            return redirect(url_for('showAllPosts'))
    return render_template('createpost.html', form = form)

@app.route('/posts')
def showAllPosts():
    # .all() so you get the list of all
    #posts = Post.query.all()
    posts = Post.query.order_by(Post.date_created.desc()).all()
    # gives posts to posts.html
    return render_template('posts.html', posts = posts)

@app.route('/posts/<int:post_id>')
    # we need post_id as a keyword argument to pass in in route ^
def showPost(post_id):
    post = Post.query.get(post_id) # only works for primary keys
    if post:
        return render_template('singlepost.html', post = post) 
    else:
        redirect(url_for("showAllPosts"))

@app.route('/posts/delete/<int:post_id>')
@login_required # you must be logged in to delete
def deletePost(post_id):
    # find this post
    post = Post.query.get(post_id)
    if post:
        # make sure you are the author
        if post.user_id == current_user.id:
            post.delete_from_db()
        else:
            print("You cannot delete another user's post")
    else:
        print('the post you are trying to delete does not exist')
    return redirect(url_for('showAllPosts'))

@app.route('/posts/update/<int:post_id>', methods = ['GET','POST'])
@login_required # you must be logged in to delete
def updatePost(post_id):
    # find this post
    post = Post.query.get(post_id)
    if post:
        # make sure you are the author
        if post.user_id == current_user.id:
            form = PostForm()
            if request.method == 'POST':
                if form.validate():
                    title = form.title.data
                    img_url = form.img_url.data
                    caption = form.caption.data
                    # update the post!
                    post.title = title
                    post.img_url = img_url
                    post.caption = caption
                    # we should have a last_updated timestemp but we didn't implement this lol
                    # we don't need to add to session just commit
                    post.save_changes_to_db()

                    flash('Successfully updated your post', 'success')

                    return redirect(url_for('showPost', post_id = post.id))

            return render_template('updatepost.html', form = form, post = post)
        else:
            flash("you cannot update anther user's post", 'danger')
    else:
        flash('the post you are trying to update does not exist', 'danger')
    return redirect(url_for('showAllPosts'))

@app.route('/posts/like/<int:post_id>')
@login_required
def likePost(post_id):
    like = Like(current_user.id, post_id)
    like.saveToDB()
    return redirect(url_for('showAllPosts'))

@app.route('/posts/unlike/<int:post_id>')
@login_required
def unlikePost(post_id):
    like = Like.query.filter_by(postid=post_id).first() # should only have 1 that matches
    if like:
        like.deleteFromDB()
    return redirect(url_for('showAllPosts'))

@app.route('/follow/<int:user_id>')
@login_required
def followUser(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.follow(user)
    return redirect(url_for('homePage'))

@app.route('/unfollow/<int:user_id>')
@login_required
def unfollowUser(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.unfollow(user)
    return redirect(url_for('homePage'))

import requests as r
import os
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

@app.route('/news')
def newsPage():
    # note at end of this we add the pageSize=20
    url = f'https://newsapi.org/v2/everything?q=tesla&from=2023-03-18&sortBy=publishedAt&apiKey={NEWS_API_KEY}&pageSize=20'
    response = r.get(url)
    data = response.json()
    articles = []
    # in the JSON it says that status should be 'ok', written in the JSON file
    if data['status'] == 'ok':
        articles = data['articles']
    return render_template('news.html', articles=articles)