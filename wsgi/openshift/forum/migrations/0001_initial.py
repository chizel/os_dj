# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Branch'
        db.create_table(u'forum_branch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('count_themes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'forum', ['Branch'])

        # Adding model 'Theme'
        db.create_table(u'forum_theme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_branch', to=orm['forum.Branch'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_author', to=orm['userprofile.UserProfile'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_post', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_last_author', to=orm['userprofile.UserProfile'])),
            ('count_posts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'forum', ['Theme'])

        # Adding model 'Post'
        db.create_table(u'forum_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_theme_id', to=orm['forum.Theme'])),
            ('post', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_user_id', to=orm['userprofile.UserProfile'])),
        ))
        db.send_create_signal(u'forum', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Branch'
        db.delete_table(u'forum_branch')

        # Deleting model 'Theme'
        db.delete_table(u'forum_theme')

        # Deleting model 'Post'
        db.delete_table(u'forum_post')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'forum.branch': {
            'Meta': {'object_name': 'Branch'},
            'count_themes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'forum.post': {
            'Meta': {'object_name': 'Post'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_theme_id'", 'to': u"orm['forum.Theme']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_user_id'", 'to': u"orm['userprofile.UserProfile']"})
        },
        u'forum.theme': {
            'Meta': {'object_name': 'Theme'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_branch'", 'to': u"orm['forum.Branch']"}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'count_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_last_author'", 'to': u"orm['userprofile.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_author'", 'to': u"orm['userprofile.UserProfile']"})
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

    complete_apps = ['forum']