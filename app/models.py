from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column,
                        create_engine,
                        Integer,
                        String,
                        Boolean,
                        ForeignKey,
                        Date,
                        LargeBinary,
                        DateTime,
                        Table,)
from sqlalchemy.orm import relationship, sessionmaker
from hashlib import sha512
from datetime import datetime


engine = create_engine('mysql+pymysql://root:example@localhost:3306/test')
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_session():
    return Session()


def delete_all():
    Base.metadata.drop_all(engine)


def create_all():
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    login = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    role = relationship('Role', back_populates='users')
    operations = relationship('Operation')

    def set_password(self, password: str):
        self.password = sha512(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return sha512(password.encode()).hexdigest() == self.password


roles_rights = Table('roles_rights', Base.metadata,
                     Column('role_id', Integer, ForeignKey('roles.role_id')),
                     Column('right_id', Integer, ForeignKey('rights.right_id')))

# class RolesRights(Base):
#     __tablename__ = 'roles_rights'
#
#     role_id = Column(Integer(), ForeignKey('roles.role_id'))
#     role = relationship('Role')
#     right_id = Column(Integer(), ForeignKey('rights.right_id'))
#     right = relationship('Rights')


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    rights = relationship('Right',
                          secondary=roles_rights,
                          back_populates='roles')
    users = relationship('User', back_populates='role')


class Right(Base):
    __tablename__ = 'rights'

    right_id = Column(Integer, primary_key=True)
    field_type_id = Column(Integer, ForeignKey('field_types.ft_id'))
    field_type = relationship('FieldType')
    operation_type_id = Column(Integer, ForeignKey('operation_types.opt_id'))
    operation_type = relationship("OperationType", back_populates='rights')
    roles = relationship('Role',
                         secondary=roles_rights,
                         back_populates='rights')


class FieldType(Base):
    __tablename__ = 'field_types'

    ft_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    required = Column(Boolean, default=False)
    sensitive = Column(Boolean, default=True)
    field_archetype_id = Column(Integer, ForeignKey('field_archetypes.fa_id'))
    field_archetype = relationship('FieldArchetype', back_populates='types')
    fields = relationship('Field')


class FieldArchetype(Base):
    __tablename__ = 'field_archetypes'

    fa_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    shortened_name = Column(String(3), nullable=False, unique=True)
    types = relationship('FieldType')


class Field(Base):
    __tablename__ = 'fields'

    f_id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('personal_cards.card_id'))
    card = relationship('PersonalCard', back_populates='fields')
    field_type_id = Column(Integer, ForeignKey('field_types.ft_id'))
    field_type = relationship('FieldType', back_populates='fields')
    value = Column(LargeBinary)


class PersonalCard(Base):
    __tablename__ = 'personal_cards'

    card_id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    surname = Column(String(40), nullable=False)
    birth_date = Column(Date, nullable=True)
    patronymic = Column(String(40))
    fields = relationship('Field')
    is_archive = Column(Boolean, default=False)


class OperationType(Base):
    __tablename__ = 'operation_types'

    opt_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    rights = relationship('Right', back_populates='operation_type')
    operations = relationship('Operation')


class Operation(Base):
    __tablename__ = 'operations'

    operation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('User', back_populates='operations')
    opt_id = Column(Integer, ForeignKey('operation_types.opt_id'))
    operation_type = relationship(OperationType, back_populates='operations')
    date = Column(DateTime)
    field_id = Column(Integer, ForeignKey('fields.f_id'))
    field = relationship(Field)
    previous = Column(LargeBinary)
    current = Column(LargeBinary)


if __name__ == "__main__":
    delete_all()
    create_all()
    session = get_session()
    # create field archetypes
    archetypes = [
        FieldArchetype(**{"name": "integer", "shortened_name": "int"}),
        FieldArchetype(**{"name": "string", "shortened_name": "str"}),
        FieldArchetype(**{"name": "text", "shortened_name": "txt"})
    ]
    for art in archetypes:
        session.add(art)
    # create operation types
    operation_types = [  # list of use cases names to assign rights to perform some actions
        OperationType(**{"name": "view-pd"}),
        OperationType(**{"name": "view-extended-pd"}),
        OperationType(**{"name": "add-by-hand"}),
        OperationType(**{"name": "import-pd"}),
        OperationType(**{"name": "export-pd"}),
        OperationType(**{"name": "create-role"}),
        OperationType(**{"name": "edit-role"}),
        OperationType(**{"name": "set-role"}),
        OperationType(**{"name": "edit-pd"}),
        OperationType(**{"name": "archive-pd"}),
        OperationType(**{"name": "view-pd-archived"}),
        OperationType(**{"name": "create-user"}),
        OperationType(**{"name": "edit-user"}),
        OperationType(name="login")
    ]
    for i in operation_types:
        session.add(i)
    admin_role = Role(name='admin') # create admin role
    admin = User(name="Julius Caesar", login='admin', email='email') # create admin
    admin.set_password('admin')  # setting password (can't be set directly cause db store only hashes)
    admin_role.users.append(admin)  # adding to relationship
    session.add(admin)  # add admin object (non-dependable from role)
    session.add(admin_role)  # add role object (dependable from user cause of created relationship)
    # add rights for admin
    for operation_type in operation_types:
        tmp_right = Right()
        tmp_right.operation_type = operation_type
        admin_role.rights.append(tmp_right)
    # add some field types to profiles
    field_types = [
        FieldType(name='biography', field_archetype=archetypes[2], required=True, sensitive=True),
        FieldType(name='nickname', field_archetype=archetypes[1], required=False, sensitive=False),
        FieldType(name='height', field_archetype=archetypes[0], required=True, sensitive=False)
    ]
    for i in field_types:
        session.add(i)
    # create profiles
    cards = [
        PersonalCard(name="James",
                     surname='Bodn',
                     birth_date=datetime.date(datetime.utcnow()),
                     is_archive=False),
        PersonalCard(name="John",
                     surname="Snow",
                     birth_date=datetime.date(datetime.utcnow()),
                     is_archive=False),
        PersonalCard(name="Steven",
                     surname="Hoking",
                     birth_date=datetime.date(datetime.utcnow()),
                     is_archive=False),
        PersonalCard(name="Igor",
                     surname="Sikorsky",
                     birth_date=datetime.date(datetime.utcnow()),
                     is_archive=False)
    ]
    for i in cards:
        session.add(i)
    # add some custom fields
    fields = [
        Field(field_type=field_types[0], value="Some bio1".encode(), card=cards[0]),
        Field(field_type=field_types[0], value="Some bio2".encode(), card=cards[1]),
        Field(field_type=field_types[0], value="Some bio3".encode(), card=cards[2]),
        Field(field_type=field_types[0], value="Some bio4".encode(), card=cards[3]),
        Field(field_type=field_types[1], value="Some bio1".encode(), card=cards[0]),
        Field(field_type=field_types[1], value="Some bio2".encode(), card=cards[1]),
        Field(field_type=field_types[1], value="Some str3".encode(), card=cards[2]),
        Field(field_type=field_types[1], value="Some str4".encode(), card=cards[3]),
        Field(field_type=field_types[2], value="180".encode(), card=cards[0]),
        Field(field_type=field_types[2], value="176".encode(), card=cards[1]),
        Field(field_type=field_types[2], value="178".encode(), card=cards[2]),
        Field(field_type=field_types[2], value="190".encode(), card=cards[3]),
    ]
    for i in fields:
        session.add(i)
    session.commit()  # save all the changes to the db
