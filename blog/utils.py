from .models import *
import json
import datetime


def rollback_to(date):
    print(date)
    previous_states = Temporary.objects.filter(
        StartDate__lte=date
    ).order_by('StartDate')

    if previous_states:
        print(len(previous_states))
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Like.objects.all().delete()
        Tag.objects.all().delete()
        for state in previous_states:
            data = json.loads(state.JsonData)[0]
            print(data['model'])
            if data['model'] == 'blog.post':
                if state.action == 'delete':
                    Post.objects.filter(title=data['fields']['title']).delete()
                else:
                    try:
                        new_post = Post(title=data['fields']['title'], content=data['fields']['content'], id=int(data['pk']),
                                        date_posted=datetime.datetime.strptime(data['fields']['date_posted'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                        author=User.objects.filter(id=int(data['fields']['author'])).get())

                    except Exception:
                        new_post = Post(title=data['fields']['title'], content=data['fields']['content'], id=int(data['pk']),
                                        date_posted=datetime.datetime.strptime(data['fields']['date_posted'], '%Y-%m-%dT%H:%M:%S.%f'),
                                        author=User.objects.filter(id=int(data['fields']['author'])).get())
                    new_post.tags.set(data['fields']['tags'])
                    new_post.save()
                print()
            elif data['model'] == 'blog.comment':
                if state.action == 'delete':
                    Comment.objects.filter(content=data['fields']['content'], author=int(data['fields']['author'])).delete()
                else:
                    try:
                        new_comment = Comment(content=data['fields']['content'],
                                              created=datetime.datetime.strptime(data['fields']['created'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                              author=User.objects.filter(id=int(data['fields']['author'])).get(),
                                              post=Post.objects.filter(id=int(data['fields']['post'])).get())
                    except Exception:
                        new_comment = Comment(content=data['fields']['content'],
                                              created=datetime.datetime.strptime(data['fields']['created'], '%Y-%m-%dT%H:%M:%S.%f'),
                                              author=User.objects.filter(id=int(data['fields']['author'])).get(),
                                              post=Post.objects.filter(id=int(data['fields']['post'])).get())

                    new_comment.save()
            elif data['model'] == 'blog.like':
                if state.action == 'delete':
                    Like.objects.filter(post=Post.objects.filter(id=int(data['fields']['post'])).get(),
                                        user=User.objects.filter(id=int(data['fields']['user'])).get()).delete()
                else:
                    try:
                        new_like = Like(user=User.objects.filter(id=int(data['fields']['user'])).get(),
                                        post=Post.objects.filter(id=int(data['fields']['post'])).get(),
                                        created_at=datetime.datetime.strptime(data['fields']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'))
                    except Exception:
                        new_like = Like(user=User.objects.filter(id=int(data['fields']['user'])).get(),
                                        post=Post.objects.filter(id=int(data['fields']['post'])).get(),
                                        created_at=datetime.datetime.strptime(data['fields']['created_at'], '%Y-%m-%dT%H:%M:%S.%f'))
                    new_like.save()
            elif data['model'] == 'blog.tag':
                if state.action == 'delete':
                    Tag.objects.filter(name=data['fields']['name']).delete()
                else:
                    new_tag = Tag(name=data['fields']['name'], slug=data['fields']['slug'],
                                  id=data['pk'])
                    new_tag.save()
    else:
        pass
