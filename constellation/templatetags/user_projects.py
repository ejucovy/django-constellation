from constellation.models import Comment

from django import template

from djangohelpers.templatetags import TemplateTagNode

class GetComments(TemplateTagNode):

    noun_for = {"for":"href"}

    def __init__(self, varname, href):
        TemplateTagNode.__init__(self, varname, href=href)

    def execute_query(self, href):
        return Comment.objects.filter(for_uri=href)

register = template.Library()
register.tag('get_comments', GetComments.process_tag)
