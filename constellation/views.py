from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.http import Http404
from django.shortcuts import get_object_or_404

from django.db.models import get_model,Q

from djangohelpers.lib import rendered_with
from djangohelpers.lib import allow_http

from django.contrib.auth.models import Group

from constellation.models import Stream, Link

def stream(request, gid):
    stream = get_object_or_404(Stream, group__id=gid)

    return stream.render_to_response()

    #return HttpResponse(open(stream.output_dir() + '/index.html').read())

@rendered_with('constellation/links.html')
def links(request, gid):
    group = get_object_or_404(Group, id=gid)
    links = Link.objects.filter(group=group)

    return {'links': links, 'group': group}

@rendered_with('constellation/group.html')
def group(request, gid):
    group = get_object_or_404(Group, id=gid)
    return {'group': group}
