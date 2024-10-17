from app.schemas import ma
from marshmallow import fields, validate

class UserSchema(ma.Schema):
    id = fields.Integer(required=False)
    first_name = fields.String(required=True, validate=validate.Length(max=255))
    last_name = fields.String(required=True, validate=validate.Length(max=255))
    username = fields.String(required=True, validate=validate.Length(max=255))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role_id = fields.Integer(required=False)

# Create instances of the schema
user_input_schema = UserSchema()
user_output_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
user_login_schema = UserSchema(only=["username", "password"])