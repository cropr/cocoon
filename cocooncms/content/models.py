from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.search import index
from wagtail.api import APIField


class ContentIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]

    subpage_types = ["content.ContentPage"]


class ContentPage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    parent_page_types = ["content.ContentIndexPage"]

    content_panels = Page.content_panels + ["intro", "body"]

    api_fields = [
        APIField("intro"),
        APIField("body"),
    ]
