from app.schemas import ma
from marshmallow import fields, validate

class PostSchema(ma.Schema):
    id = fields.Integer(required=False)
    title = fields.String(required=True, validate=validate.Length(max=255))
    body = fields.String(required=False, validate=validate.Length(max=1000))
    user_id = fields.Integer(required=True)

# Create an instance of the PostSchema
post_schema = PostSchema()
posts_schema = PostSchema(many=True)