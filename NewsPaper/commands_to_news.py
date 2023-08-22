# from news.models import *
#
# User1 = User.objects.create_user(username='John')
# User2 = User.objects.create_user(username='Vinc')
#
# Author1 = Author.objects.create(user=User1)
# Author2 = Author.objects.create(user=User2)
#
# Category1 = Category.objects.create(name='спорт')
# Category2 = Category.objects.create(name='политика')
# Category3 = Category.objects.create(name='образование')
# Category4 = Category.objects.create(name='искусство')
#
# News1 = Post.objects.create(author=Author1, title='Заголовок новость 1', text='Праздники являются важнейшим элементом традиции и в этом качестве играют роль стабилизатора общества, сохраняя и передавая социально значимую информацию от поколения к поколению.')
#
# Post1 = Post.objects.create(author=Author2, title='Заголовок статья 1', text='В статье выражается развернутая обстоятельная аргументированная концепция автора по поводу проблемы. Также в статье журналист должен интерпретировать факты.', p_type='AR')
#
# Post2 = Post.objects.create(author=Author1, title='Заголовок статья 2', text='Как правило, новости на телевидении и радио передаются несколько раз в день,  длятся от двух минут до часа. Новости обычно бывают из разных областей.', p_type='AR')
#
# News1.categories.add(Category1)
# News1.categories.add(Category2)
#
# Post1.categories.add(Category3)
# Post1.categories.add(Category4)
#
# Post2.categories.add(Category1)
# Post2.categories.add(Category4)
#
# Comment1 = Comment.objects.create(user=User1, post=News1, text='comment to news')
# Comment2 = Comment.objects.create(user=User2, post=News1, text='comment to news 222')
# Comment3 = Comment.objects.create(user=User1, post=Post1, text='comment to article 11')
# Comment4 = Comment.objects.create(user=User2, post=Post1, text='comment to article 22')
# Comment5 = Comment.objects.create(user=User1, post=Post2, text='comment to article 33')
# Comment6 = Comment.objects.create(user=User2, post=Post2, text='comment to article 44')
#
# News1.like()
# News1.like()
# News1.like()
#
# Post1.like()
#
# Post2.like()
# Post2.like()
#
# Comment1.like()
# Comment2.like()
# Comment3.like()
# Comment4.like()
# Comment5.like()
# Comment6.like()
#
# Author1.update_rating()
# Author2.update_rating()
#
# News1.dislike()
# News1.dislike()
#
# Post1.dislike()
#
# Post2.dislike()
#
# Comment2.dislike()
# Comment5.dislike()
# Comment6.dislike()
#
# Author1.update_rating()
# Author2.update_rating()
#
# best_author = Author.objects.all().order_by('-_rating').first()
# best_author.user.username
# best_author.rating
#
# best_post = Post.objects.all().order_by('-_rating').first()
# best_post.post_date
# best_post.author.user.username
# best_post.rating
# best_post.title
# best_post.preview()
#
# Comment.objects.filter(post=best_post).values('com_date', 'user', '_rating', 'text')
