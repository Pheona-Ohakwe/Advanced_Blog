from app.schemas import ma
from marshmallow import fields, validate
from app.schemas.userSchema import UserSchema

class RoleSchema(ma.Schema):
    id = fields.Integer(required=False)
    role_name = fields.String(required=True, validate=validate.Length(max=255))
    users = fields.List(fields.Nested("UserSchema", only=["id", "username"]))

# Create an instance of the RoleSchema
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)