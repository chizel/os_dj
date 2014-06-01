from django.db import models
from userprofile.models import UserProfile

class Tag(models.Model):
    name = models.CharField(max_length=50)

    #if tag someone created then we have one entry
    #count_articles = models.PosititveIntegerField(default=1)
    
    #def increment_count_articles(self):
        #self.count_articles += 1

    #def decrement_count_articles(self):
        #if self.count_articles > 1:
            #self.count_articles -= 1
        #else:
            #self.count_articles = 0

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/blog/tag/%s' % self.name

class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    body = models.TextField()
    user = models.ForeignKey(UserProfile, related_name='blog_user')
    date = models.DateTimeField(auto_now_add=True)
    count_comments = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag)  

    def __unicode__(self):
        return self.title

    def increment_count_comments(self):
        self.count_comments += 1
        self.save()

    def decrement_count_comments(self):
        if self.count_comments > 0:
            self.count_comments -= 1
        else:
            self.count_comments = 0
        self.save()
    
    def get_absolute_url(self):
        return '/blog/post/%i/' % self.id

#add tree 
#|comment
# |else_comment
# |etc
#|and else comment
class BlogPostComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=300)
    post = models.ForeignKey(BlogPost, related_name='comment_post')
    user = models.ForeignKey(UserProfile, related_name='comment_user')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    parent_comment = models.IntegerField(default=0)
    #hidden = models.BoleanField(default=False)
    #update_rating(+-)
