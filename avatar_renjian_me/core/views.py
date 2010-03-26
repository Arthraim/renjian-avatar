# coding=UTF8
import urllib2
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.db.models import Count
from core.models import Renjianer

def indexRequest(request):
    if request.method == 'GET':
        rens = Renjianer.objects.order_by('-date')[0:5]
        render_var = {
            'rens': rens,
            'avatars': None
        }
        return render_to_response('index.html', render_var)

def getAvatars(request):
    if request.method == 'GET':
        screen_name = request.GET.get('user')
        if not screen_name:
            return HttpResponseRedirect('/error?message=screen_name or id may be wrong.')

        rnjn_url = 'http://api.renjian.com/'
        user_url = rnjn_url + 'users/show.json?id=' + screen_name.encode('UTF-8')
        try:
            retval = urllib2.urlopen(user_url)
            json = retval.read()
            data = simplejson.loads(json, encoding='UTF-8')
            ren = Renjianer()
            ren.user_name = data['screen_name']
            user_id = data['id']
            ren.user_id = user_id
            img_url = unicode(data['profile_image_url'])
            if img_url == 'http://renjian.com/images/buddy_icon/120x120.jpg':
                num = 0
            else:
                img_url = img_url.replace('http://avatar.renjian.com/' + unicode(user_id) + '/120x120_', '')
                img_url = img_url.replace('.jpg', '')
                num = int(img_url)
            ren.avatar_num = num
            ren.save()
        except urllib2.HTTPError, ex:
            return HttpResponseRedirect('/error?message=API request result: ' + unicode(ex.code))
        except ValueError, ex:
            return HttpResponseRedirect('/error?message=user [' + ren.user_name + '] data got error! (' + ex.message + ')')
        i = num
        avatars = []
        while i:
            avatars.append('http://avatar.renjian.com/' + unicode(user_id) + '/120x120_' + unicode(i) + '.jpg')
            i = i - 1
        rens = Renjianer.objects.order_by('-date')[0:5]
        render_var = {
            'user': data,
            'rens': rens,
            'avatars': avatars
        }
        return render_to_response('index.html', render_var)
    
def postName(request):
    if request.method == 'POST':
        screen_name = request.POST.get('content').lstrip().rstrip()
        if not screen_name:
            return HttpResponseRedirect('/error?message=screen_name or id may be wrong.')
        return HttpResponseRedirect('/avatars?user=' + screen_name);

def error(request):
    message = request.GET.get('message')
    if message:
        message = message.encode('UTF-8')
    else:
        message = None
    return render_to_response('error.html', {'message': message})

def history(request):
    ITEMS_NUM = 15
    
    p_index = request.GET.get('p')
    if not p_index: 
        p_index = 1
    else:
        p_index = int(p_index)
    if p_index <= 1: 
        p_index = 1
        newer = None
    else: 
        newer = p_index - 1
    older = p_index + 1
    
    p_itempos = (p_index - 1) * ITEMS_NUM
    p_itemnum = p_index * ITEMS_NUM
    
    visitQ = Renjianer.objects.order_by('-date')
    visitnum = visitQ.__len__()
    if (visitnum / ITEMS_NUM + 1) == p_index:
        older = None
        p_itemnum = visitnum

    pageQ = Renjianer.objects.order_by('-date')[p_itempos:p_itemnum]

    userQ = Renjianer.objects.all()
    userQ.query.group_by = ['user_name']
    usernum = userQ.__len__()
    
    template_parameters = {
        'newer': newer,
        'older': older,
        'visitnum': visitnum,
        'p_itempos': p_itempos + 1,
        'p_itemnum': p_itemnum,
        'usernum': usernum, 
        'rens': pageQ
    }
    return render_to_response('history.html', template_parameters)
