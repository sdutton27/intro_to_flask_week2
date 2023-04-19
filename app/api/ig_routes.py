from . import api
from ..models import Post
from flask import abort

#@api.routes('/posts')
@api.get('/posts')
# this will only ever be GET so we don't need methods="GET"
def getPostsAPI():
    posts = Post.query.all()
    return {
        'status' : 'ok',
        'results' : len(posts),
        # we need to convert posts to a list of dictionaries with the proper attributes from a Post object
        'posts' : [p.to_dict() for p in posts] # for every post in posts, let's create a dictionary for it
    }

@api.get('/posts/<int:post_id>')
# this will only ever be GET so we don't need methods="GET"
def getPostAPI(post_id):
    post = Post.query.get(post_id)
    # return something to the user if the page doesn't exist
    if post:
        return {
            'status' : 'ok',
            'results' : 1,
            'posts' : post.to_dict() # for every post in posts, let's create a dictionary for it
        }
    else:
        #abort(404)
        # or we could just give them a result, but a non result
        return {
            'status' : 'not ok',
            'message' : 'The post you are looking for does not exist'
        }, 404 # 404 is the status code
