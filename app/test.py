from app.models.user_role import Roles

role = Roles.filter(id=1)
print(role)