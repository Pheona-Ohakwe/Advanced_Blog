from app import app, cache, limiter, db
from flask import request, jsonify
from app.schemas.userSchema import user_input_schema, user_output_schema, users_schema, user_login_schema
from app.schemas.postSchema import post_schema, posts_schema
from app.schemas.commentSchema import comment_schema, comments_schema
from app.schemas.roleSchema import role_schema
from marshmallow import ValidationError
# from app.database import db
# from app import db
from app.models import User, Post, Comment, Role
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.utils import encode_token
from app.auth import token_auth
# from flask_caching import Cache
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from app import cache, limiter 
from sqlalchemy.exc import IntegrityError 



@app.route('/')
def index():
    return 'Testing'

# Token Route/ Login
@app.route('/token', methods=["POST"])
def get_token():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400
    try:
        data = request.json
        credentials = user_login_schema.load(data)
        query = db.select(User).where(User.username==credentials['username'])
        user = db.session.scalars(query).first()
        if user is not None and check_password_hash(user.password, credentials['password']):
            auth_token = encode_token(user.id)
            return {'token': auth_token}, 200
        else:
            return {"error": "Username and/or password is incorrect"}, 401 
    except ValidationError as err:
        return err.messages, 400


# Create a new role
@app.route('/roles', methods=["POST"])
def create_role():
    
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 
    try:
        data = request.json
        role_data = role_schema.load(data)
        query = db.select(Role).where(Role.role_name == role_data['role_name'])
        check_roles = db.session.scalars(query).all()
        if check_roles: 
            return {"error": "Role with that role_name already exists"}, 400 
        
        new_role = Role(
            role_name=role_data['role_name'],
        )
        
        db.session.add(new_role)
        db.session.commit()
        
        return jsonify(role_schema.dump(new_role)), 201 
    
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400




# ----------- USER ROUTES -----------

# Get all users
@app.route('/users', methods=['GET'])
@token_auth.login_required(role='admin')
@cache.cached(timeout=60) 
@limiter.limit("100 per day")
def get_all_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users)


# Get a single user by ID
@app.route('/users/<int:user_id>', methods=["GET"])
@token_auth.login_required(role='admin')
@cache.cached(timeout=60)  
@limiter.limit("100 per day")
def get_single_user(user_id):
    user = db.session.get(User, user_id)
    if user is not None:
        return user_output_schema.jsonify(user)
    return {"error": f"Customer with ID {user_id} does not exist"}, 404


# Create a new user
@app.route('/users', methods=["POST"])
@limiter.limit("100 per day")
def create_user():
    
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 
    try:
        data = request.json
        user_data = user_input_schema.load(data)
        query = db.select(User).where( (User.username == user_data['username']) | (User.email == user_data['email']) )
        check_users = db.session.scalars(query).all()
        if check_users: 
            return {"error": "User with that username and/or email already exists"}, 400 
        
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            email=user_data['email'],
            password=generate_password_hash(user_data['password'])
        )
        if 'role_id' in user_data:
            new_user.role_id = user_data['role_id']
        
        db.session.add(new_user)
        db.session.commit()
        
        return user_output_schema.jsonify(new_user), 201 
    except ValidationError as err:
        return err.messages, 400
    except ValueError as err:
        return {"error": str(err)}, 400
    

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User could not be found with that User ID'}), 404
        user_data = user_input_schema.load(request.json, partial=True)
        for field, value in user_data.items():
            setattr(user, field, value)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required(role='admin')
@limiter.limit("100 per day")
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': "User could not be found with the user ID"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200



    
# ----------- POST ROUTES -----------
    
# Get all posts
@app.route('/posts', methods=['GET'])
@token_auth.login_required
@cache.cached(timeout=60)  
@limiter.limit("100 per day")
def get_all_posts():
    posts = db.session.query(Post).all()
    return posts_schema.jsonify(posts)


# Get a single post by ID
@app.route('/posts/<int:post_id>', methods=["GET"])
@token_auth.login_required
@cache.cached(timeout=60)  
@limiter.limit("100 per day")
def get_single_post(post_id):
    post = db.session.query(Post).get(post_id)
    if post:
        return post_schema.jsonify(post)
    return {"error": f"Post with ID {post_id} does not exist"}, 404


# Create a new post
@app.route('/posts', methods=["POST"])
@limiter.limit("100 per day")
def create_post():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400 
    
    try:
        data = request.json
        post_data = post_schema.load(data)
        
        new_post = Post(
            title=post_data['title'],
            body=post_data['body'],
            user_id=post_data['user_id']
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return post_schema.jsonify(new_post), 201 
    except ValidationError as err:
        return err.messages, 400
    except Exception as e:
        return {"error": str(e)}, 500


# Update a post
@app.route('/posts/<int:post_id>', methods=['PUT'])
@token_auth.login_required
@limiter.limit("100 per day")
def update_post(post_id):
    try:
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': 'Post could not be found with that post ID'}), 404
        post_data = post_schema.load(request.json, partial=True)
        for field, value in post_data.items():
            setattr(post, field, value)
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


# Delete a post
@app.route('/posts/<int:post_id>', methods=['DELETE'])
@token_auth.login_required
@limiter.limit("100 per day")
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post could not be found with that post ID'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200




# ----------- COMMENT ROUTES -----------
    
# Get all comments
@app.route('/comments', methods=['GET'])
@token_auth.login_required
@cache.cached(timeout=60)  
@limiter.limit("100 per day")
def get_all_comments():
    comments = db.session.query(Comment).all()
    return comments_schema.jsonify(comments)


# Get a single comment by ID
@app.route('/comments/<int:comment_id>', methods=["GET"])
@token_auth.login_required
@cache.cached(timeout=60) 
@limiter.limit("100 per day")
def get_single_comment(comment_id):
    comment = db.session.query(Comment).get(comment_id)
    if comment:
        return comment_schema.jsonify(comment)
    return {"error": f"Comment with ID {comment_id} does not exist"}, 404


# Create a new comment
@app.route('/comments', methods=["POST"])
@limiter.limit("100 per day")
def create_comment():
    if not request.is_json:
        return {"error": "Request body must be application/json"}, 400
    try:
        data = request.json
        comment_data = comment_schema.load(data)
        
        if not db.session.query(Post.id).filter_by(id=comment_data['post_id']).scalar():
            return {"error": f"Post with ID {comment_data['post_id']} does not exist"}, 404
        
        new_comment = Comment(
            content=comment_data['content'],
            user_id=comment_data['user_id'],
            post_id=comment_data['post_id']
        )
        db.session.add(new_comment)
        db.session.commit()
        return comment_schema.jsonify(new_comment), 201
    
    except ValidationError as err:
        db.session.rollback() 
        return err.messages, 400
    
    except IntegrityError as e:
        db.session.rollback()  
        return {"error": f"IntegrityError: {str(e)}"}, 500
    
    except Exception as e:
        db.session.rollback()  
        return {"error": str(e)}, 500
    
    finally:
        db.session.close()


# Update a comment
@app.route('/comments/<int:comment_id>', methods=['PUT'])
@token_auth.login_required
@limiter.limit("100 per day")
def update_comment(comment_id):
    try:
        comment = Comment.query.get(comment_id)
        if not comment:
            return jsonify({'message': 'Comment could not be found with that comment ID'}), 404
        comment_data = comment_schema.load(request.json, partial=True)
        for field, value in comment_data.items():
            setattr(comment, field, value)
        db.session.commit()
        return jsonify({'message': 'Comment updated successfully'}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


# Delete a comment
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_auth.login_required
@limiter.limit("100 per day")
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'message': 'Comment could not be found with that comment ID'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200