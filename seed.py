from models import User, Post, db, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

user1 = User(first_name='Taco', last_name='Tuesday', image_url='example.jpg')
user2 = User(first_name='Chip', last_name='Ahoy', image_url='example2.jpg')

post1 = Post(title='NEWPOST', content='THIS IS MY FIRST POST', user_id=1)
post2 = Post(title='second post', content='this is the second post', user_id=1)
post3 = Post(title='second user post', content='THIS IS MY FIRST POST', user_id=2)

db.session.add_all([user1, user2])
db.session.commit()

tag1 = Tag(name='test1')
tag2 = Tag(name='test2')
tag3 = Tag(name='test3')

db.session.add_all([tag1, tag2, tag3])
db.session.commit()

db.session.add_all([post1, post2, post3])
db.session.commit()


post_tag1 = PostTag(post_id=post1.id, tag_id=tag1.id)
post_tag2 = PostTag(post_id=post2.id, tag_id=tag2.id)
post_tag3 = PostTag(post_id=post1.id, tag_id=tag3.id)

db.session.add_all([post_tag1, post_tag2, post_tag3])
db.session.commit()