from app.actions import CreateUser
from app.models import User, OperationType, get_session


session = get_session()


action = CreateUser(User())
action.handle()