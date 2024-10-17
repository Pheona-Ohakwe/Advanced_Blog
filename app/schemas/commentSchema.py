from app.schemas import ma
from marshmallow import fields, validate

class CommentSchema(ma.Schema):
    id = fields.Integer(required=False)
    content = fields.String(required=True, validate=validate.Length(max=1000))
    user_id = fields.Integer(required=True)
    post_id = fields.Integer(required=True)

# Create an instance of the Comment Schema
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)