
from django.db import models
from django.contrib.auth.models import User, Group

def CharField():
    return models.CharField(max_length=500)

class Comment(models.Model):
    text = models.TextField()
    for_uri = CharField()
    group = models.ForeignKey(Group)
    #user = models.ForeignKey(User)

class Link(models.Model):
    uri = CharField()
    group = models.ForeignKey(Group)

from django.conf import settings
from django.shortcuts import render_to_response
import subprocess

from constellation.lib import run_planet

class Stream(models.Model):
    """
    Represents a single Planet
    """
    group = models.ForeignKey(Group)

    def update_planet(self):
        template_writer(self)
        run_planet(self.config_file())

    def render_to_response(self):
        template = self.output_template()
        context = {'group': self.group}
        return render_to_response(template, context)

    def config_dir(self):
        return os.path.join(
            settings.PLANET_CONFIG_DIR,
            self.group.name)

    def config_file(self):
        return os.path.join(self.config_dir(), "config.ini")

    def output_dir(self):
        return os.path.join(settings.PLANET_OUTPUT_DIR,
                            'planet_output',
                            self.group.name)

    def output_template(self):
        return 'planet_output/%s/index.html' % self.group.name

class Feed(models.Model):
    url = CharField()
    title = CharField()
    stream = models.ForeignKey(Stream)

from django.template.loader import render_to_string

import os
from django.contrib.admin import site

site.register(Stream)
site.register(Feed)
site.register(Comment)
site.register(Link)

import constellation.settings

def template_writer(stream):
    try:
        PLANET_TEMPLATE_FILES = settings.PLANET_TEMPLATE_FILES
    except AttributeError:
        PLANET_TEMPLATE_FILES = constellation.settings.PLANET_TEMPLATE_FILES

    context = {
        'stream': stream,
        'PLANET_CACHE_DIR': settings.PLANET_CACHE_DIR,
        'PLANET_TEMPLATE_FILES': PLANET_TEMPLATE_FILES,
        'PLANET_OUTPUT_DIR': settings.PLANET_OUTPUT_DIR,
        }
    output = render_to_string('planet_config.ini',
                              context)

    config_dir = stream.config_dir()
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    output_dir = stream.output_dir()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    fp = open('%s/config.ini' % config_dir, 'w')
    fp.write(output)
    fp.close()
