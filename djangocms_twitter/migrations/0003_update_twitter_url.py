# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-14 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

TWITTER_URL = r'https://twitter.com/'


def fwd_old_to_new(apps, schema_editor):
    update_model(apps, True)


def rev_new_to_old(apps, schema_editor):
    update_model(apps, False)


def update_model(apps, fwd):
    twitter_model = apps.get_model('djangocms_twitter', 'twittertimeline')
    cmsplugin_model = apps.get_model('cms', 'cmsplugin')

    for inst in twitter_model.objects.all():

        cms_plugin =  cmsplugin_model.objects.get(id=inst.cmsplugin_ptr_id)
        twitter_url = str(inst.twitter_url)

        # Add Twitter URL to user id: https://twitter.com/TWITTER_USER
        if fwd:
            cms_plugin_plugin_type = 'TwitterTimelinePlugin'
            if not twitter_url.startswith(TWITTER_URL):
                twitter_url =  TWITTER_URL + twitter_url
        else:
            cms_plugin_plugin_type = 'TwitterRecentEntriesPlugin'
            if twitter_url.startswith(TWITTER_URL):
                twitter_url = twitter_url.replace(TWITTER_URL, '')

        inst.twitter_url = twitter_url
        inst.save()

        cms_plugin.plugin_type = cms_plugin_plugin_type
        cms_plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('djangocms_twitter', '0002_rename_twitter_model'),
    ]

    # Run reversible Python script
    # ----------------------------------
    operations = [
        migrations.RunPython(fwd_old_to_new, rev_new_to_old),
    ]

