from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

import datetime


class Category(models.Model):
    """Category model"""
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'library_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('library_category_detail', None, {'slug': self.slug})


class Article(models.Model):
    """Article model"""
    STATUSES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField(_('body'), )
    intro = models.TextField(_('intro'), blank=True, help_text=_('Inroduction text'))
    status = models.IntegerField(_('status'), choices=STATUSES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    #tags = TagField()
    #objects = PublicManager()

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        db_table  = 'library_articles'
        ordering  = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return reverse('library:article_detail', kwargs={
            'slug': self.slug,
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day
        })

    def get_previous_article(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_article(self):
        return self.get_next_by_publish(status__gte=2)
