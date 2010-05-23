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

from constellation.models import Stream, Link, Comment, Feed

def stream(request, gid):
    stream = get_object_or_404(Stream, group__id=gid)

    return stream.render_to_response({'user': request.user})

    #return HttpResponse(open(stream.output_dir() + '/index.html').read())

def forbidden():
    return HttpResponseForbidden()

@allow_http("POST")
def comment(request, gid):
    group = get_object_or_404(Group, id=gid)
    if group not in request.user.groups.all():
        return forbidden()    
    uri = request.POST.get('uri')
    text = request.POST.get('text')
    comment = Comment(for_uri=uri, text=text, group=group)
    comment.save()
    return HttpResponseRedirect(reverse('group_stream', args=[gid]))

@allow_http("GET", "POST")
def links(request, gid):
    if request.method == "GET": return show_links(request, gid)
    group = get_object_or_404(Group, id=gid)
    if group not in request.user.groups.all():
        return forbidden()
    uri = request.POST.get('uri')
    link = Link(uri=uri, group=group)
    link.save()
    return HttpResponseRedirect('.')

@allow_http("GET")
@rendered_with('constellation/links.html')
def show_links(request, gid):
    group = get_object_or_404(Group, id=gid)
    links = Link.objects.filter(group=group)

    return {'links': links, 'group': group}

@rendered_with('constellation/group.html')
def group(request, gid):
    group = get_object_or_404(Group, id=gid)
    return {'group': group}

@rendered_with('constellation/index.html')
def index(request):
    streams = Stream.objects.all()
    return {'streams': streams}

@allow_http("GET", "POST")
@rendered_with('constellation/feeds.html')
def feeds(request, gid):
    group = get_object_or_404(Group, id=gid)
    feeds = Feed.objects.filter(stream__group=group)
    return {'feeds': feeds, 'group': group}
