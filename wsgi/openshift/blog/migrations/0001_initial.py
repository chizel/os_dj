# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'blog_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'blog', ['Tag'])

        # Adding model 'BlogPost'
        db.create_table(u'blog_blogpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blog_user', to=orm['userprofile.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('count_comments', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'blog', ['BlogPost'])

        # Adding M2M table for field tag on 'BlogPost'
        m2m_table_name = db.shorten_name(u'blog_blogpost_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blogpost', models.ForeignKey(orm[u'blog.blogpost'], null=False)),
            ('tag', models.ForeignKey(orm[u'blog.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['blogpost_id', 'tag_id'])

        # Adding model 'BlogPostComment'
        db.create_table(u'blog_blogpostcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comment_post', to=orm['blog.BlogPost'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comment_user', to=orm['userprofile.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('parent_comment', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'blog', ['BlogPostComment'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'blog_tag')

        # Deleting model 'BlogPost'
        db.delete_table(u'blog_blogpost')

        # Removing M2M table for field tag on 'BlogPost'
        db.delete_table(db.shorten_name(u'blog_blogpost_tag'))

        # Deleting model 'BlogPostComment'
        db.delete_table(u'blog_blogpostcomment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'blog.blogpost': {
            'Meta': {'object_name': 'BlogPost'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'count_comments': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blog_user'", 'to': u"orm['userprofile.UserProfile']"})
        },
        u'blog.blogpostcomment': {
            'Meta': {'object_name': 'BlogPostComment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_comment': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_post'", 'to': u"orm['blog.BlogPost']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comment_user'", 'to': u"orm['userprofile.UserProfile']"})
        },
        u'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'userprofile.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'count_messages': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'unread_pm': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['blog']