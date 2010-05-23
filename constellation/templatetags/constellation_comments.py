from constellation.models import Comment, Group

from django import template

from djangohelpers.templatetags import TemplateTagNode

class GetComments(TemplateTagNode):

    noun_for = {"for":"href", "in":"group"}

    def __init__(self, varname, href, group):
        TemplateTagNode.__init__(self, varname, href=href, group=group)

    def execute_query(self, href, group):
        return Comment.objects.filter(for_uri=href, group=group)

register = template.Library()
register.tag('get_comments', GetComments.process_tag)
