import app.services.user as UserService
from app.models.schemas.user import UserFromIDToken



def test_login_and_authenticate(user_from_id_token: UserFromIDToken):
    session = UserService.login(user=user_from_id_token)
    user =  UserService.authenticate(session.id)
    assert user.name == user_from_id_token.name
    assert user.role == "reader"



