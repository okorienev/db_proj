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
                        Table)
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine('mysql+pymysql://root:example@localhost:3306/test')
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_session():
    return Session()


def create_all():
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    login = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    role = relationship('Role', back_populates='users')


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    rights = relationship('Rights', secondary='roles_rights', back_populates='roles')


roles_rights = Table('roles_rights', Base.metadata,
                     Column('role_id', Integer, ForeignKey('roles.role_id')),
                     Column('right_id', Integer, ForeignKey('rights.right_id')))


class Right(Base):
    __tablename__ = 'rights'

    right_id = Column(Integer, primary_key=True)
    field_type_id = Column(Integer, ForeignKey('field_types.ft_id'))
    field_type = relationship('FieldType')
    operation_type_id = Column(Integer, ForeignKey('operation_types.opt_id'))
    operation_type = relationship("OperationType", back_populates='rights')


class FieldType(Base):
    __tablename__ = 'field_types'

    ft_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    required = Column(Boolean, default=False)
    sensitive = Column(Boolean, default=True)
    field_archetype_id = Column(Integer, ForeignKey('field_archetypes.fa_id'))
    field_archetype = relationship('FieldArchetype', back_populates='types')


class FieldArchetype(Base):
    __tablename__ = 'field_archetypes'

    fa_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    shortened_name = Column(String(3), nullable=False, unique=True)


class Field(Base):
    __tablename__ = 'fields'

    f_id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('personal_cards.card_id'))
    card = relationship('PersonalCard')
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


class OperationType(Base):
    __tablename__ = 'operation_types'

    opt_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)


class Operation(Base):
    __tablename__ = 'operations'

    operation_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('User', back_populates='operations')
    opt_id = Column(Integer, ForeignKey('operation_types.opt_id'))
    operation = relationship(OperationType, back_populates='operations')
    date = Column(DateTime)
    field_id = Column(Integer, ForeignKey('fields.f_id'))
    field = relationship(Field)
    previous = Column(LargeBinary)
    current = Column(LargeBinary)
