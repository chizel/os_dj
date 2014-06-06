from django.contrib import admin
from blog.models import BlogPost, BlogPostComment, Tag

admin.site.register(BlogPost)
admin.site.register(BlogPostComment)
admin.site.register(Tag)
