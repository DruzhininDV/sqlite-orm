from sqlite_orm.database import Database
from sqlite_orm.field import IntegerField, BooleanField, TextField
from sqlite_orm.table import BaseTable


class User(BaseTable):
    __table_name__ = 'users'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)
    active = BooleanField(not_null=True, default_value=1)


class Post(BaseTable):
    __table_name__ = 'posts'

    id = IntegerField(primary_key=True)
    name = TextField(not_null=True)
    id_user = IntegerField(foreign_key=User.id)


if __name__ == '__main__':
    with Database("test.db") as db:
        # создание таблиц;
        db.query(Post, User).create().execute()

        # insert
        user1 = User(id=1, name='User1')
        user2 = User(id=2, name='User2')
        user3 = User(id=3, name='User3')

        post1 = Post(id=1, name='Post1', id_user=user1.id)
        post2 = Post(id=2, name='Post2', id_user=user2.id)
        post3 = Post(id=3, name='Post3', id_user=user3.id)

        db.query().insert(user1, user2, user3, post1, post2, post3).execute()

        # select с указанием необходимых столбцов + автоджоин таблиц, на которые есть fk;
        print('\n=======SELECT + Auto Join=======')
        for row in db.query(User, Post.name).select().join(Post).execute():
            print(row)

        # update
        db.query(User).update(name='User3_UPDATED').filter(User.name == 'User3').execute()

        print('\n=======SELECT after update=======')
        for row in db.query(User, Post.name).select().join(Post).execute():
            print(row)

        db.query(User).delete().filter(User.name == 'User3_UPDATED').execute()

        print('\n=======SELECT after delete=======')
        for row in db.query(User, Post.name).select().join(Post).execute():
            print(row)

        # удаление таблиц;
        db.query(User, Post).drop().execute()

    # + обработка базовых ошибок (нет таблицы, нет столбца, не указано значение у обязательного столбца);
