from ..models.models import User

def create_token_user(user:User):
    return {
        "userId":user.id,
        "name":user.name,
   
        "role":user.role
       
    }