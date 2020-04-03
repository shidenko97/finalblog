from flask import abort, request
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound

from blog.api.auth import auth
from blog.api.user import user_api
from blog.api.user.models import role_model, user_model
from blog.api.user.utils import (change_user, create_user, delete_user,
                                 get_all_roles, get_all_users, get_role,
                                 get_user)


@user_api.route("/")
class UserList(Resource):
    """Actions with not specific user"""

    # Basic auth required for those actions
    decorators = [auth.login_required]

    @user_api.doc("user_list")
    @user_api.marshal_list_with(user_model, envelope="data")
    def get(self):
        """Get list of all users"""

        return get_all_users()

    @user_api.expect(user_model, validate=True)
    @user_api.marshal_with(user_model, code=201)
    @user_api.doc("create_user", responses={
        201: "Success",
        400: "Validation Error"
    })
    def post(self):
        """Create a new user"""

        try:
            user = create_user(request.json)
        except ValueError as err:
            return abort(400, str(err))

        return user, 201


@user_api.route("/<int:user_id>")
@user_api.response(404, "User not found")
@user_api.param("user_id", "The user identifier")
class User(Resource):
    """Actions with specific user"""

    # Basic auth required for those actions
    decorators = [auth.login_required]

    @user_api.doc("get_user", responses={
        200: "Success",
    })
    @user_api.marshal_with(user_model)
    def get(self, user_id):
        """Get user by id"""

        try:
            return get_user(user_id)
        except NoResultFound:
            return abort(404, "User not found")

    @user_api.doc("delete_user")
    @user_api.response(204, "User deleted")
    def delete(self, user_id):
        """Delete user by id"""

        delete_user(user_id)
        return "", 204

    @user_api.expect(user_model, validate=True)
    @user_api.marshal_with(user_model)
    def put(self, user_id):
        """Change user by id"""

        data = request.json

        try:
            return change_user(user_id, data)
        except NoResultFound:
            # User not found by id
            return abort(404, "User not found")
        except ValueError as err:
            # Email validation not successfully
            return abort(400, str(err))


@user_api.route("/role")
class RoleList(Resource):
    """Actions with not specific role"""

    # Basic auth required for those actions
    decorators = [auth.login_required]

    @user_api.doc("role_list")
    @user_api.marshal_list_with(role_model, envelope="data")
    def get(self):
        """Get list of all roles"""

        return get_all_roles()


@user_api.route("/role/<int:role_id>")
@user_api.response(404, "Role not found")
@user_api.param("role_id", "The role identifier")
class Role(Resource):
    """Actions with specific role"""

    decorators = [auth.login_required]

    @user_api.doc("get_role", responses={
        200: "Success",
    })
    @user_api.marshal_with(role_model)
    def get(self, role_id):
        """Get role by id"""

        try:
            return get_role(role_id)
        except NoResultFound:
            return abort(404, "Role not found")
