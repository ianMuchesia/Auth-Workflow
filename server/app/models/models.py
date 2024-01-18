import uuid
from sqlalchemy import Column, Integer, String, TIMESTAMP, text,Enum,event,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    internal_id = Column(Integer, primary_key=True, autoincrement=True)  # Internal primary key
    id = Column(String,  nullable=False, index=True,unique=True, default=lambda: str(uuid.uuid4()))  # External/public ID for API/frontend
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


    @classmethod
    def before_update_listener(cls, mapper, connection, target):
        target.updated_at = datetime.utcnow()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        
        

#this is the user model        
class User(BaseModel, Base):
    __tablename__ = "users"
    
    name = Column(String, unique=False, nullable=False)
    email = Column(String,  nullable=False)
    password = Column(String, unique=False, nullable=False)
    verificationToken = Column(String,  nullable=False)
    isVerified = Column(Boolean, unique=False, nullable=False, default=False)

    verified = Column(TIMESTAMP(timezone=True), nullable=True)
    passwordToken = Column(String,  nullable=True)
    passwordTokenExpires = Column(TIMESTAMP(timezone=True), nullable=True)
    role = Column(Enum("admin", "user", name="role_types"), nullable=False, default="user")
    
    
    @classmethod
    def before_update_listener(cls, mapper, connection, target):
        BaseModel.before_update_listener(mapper, connection, target)
        
        
event.listen(User, 'before_update', User.before_update_listener)



class Token(BaseModel, Base):
    __tablename__ = "tokens"
    
    refreshToken = Column(String,  nullable=False)
    ip = Column(String,  nullable=False)
    userAgent = Column(String,  nullable=False)
    isValid = Column(Boolean,  nullable=False, default=True)
    user = Column(String, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    
    @classmethod
    def before_update_listener(cls, mapper, connection, target):
        BaseModel.before_update_listener(mapper, connection, target)
        
event.listen(Token, 'before_update', Token.before_update_listener)





class Task(BaseModel,Base):
    __tablename__ = "tasks"
    
    title = Column(String,  nullable=False)
    description = Column(String,  nullable=False)
    completed = Column(Boolean,  nullable=False, default=False)
    user_id = Column(String, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
    
    user = relationship("User", back_populates="tasks")
    @classmethod
    def before_update_listener(cls, mapper, connection, target):
        BaseModel.before_update_listener(mapper, connection, target)
        
event.listen(Task, 'before_update', Task.before_update_listener)