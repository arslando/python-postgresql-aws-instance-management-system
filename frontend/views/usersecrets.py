
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.utils.translation import gettext as _

import requests

from core.models import *

from frontend.forms import *

from django.apps import apps

from .functions import OPS, get_apidata, save_form

from frontend.forms import UserSecretForm as ahomeForm

from core.utils import DICT_CREDENTIALS


API_NAME = 'usersecrets'
MODEL_NAME = 'UserSecret'
MODEL_OBJ = UserSecret


CREDENTIAL_JSON = 'credential_form'
URL_CREATE = '%s_create' % MODEL_NAME.lower()
URL_UPDATE = '%s_update' % MODEL_NAME.lower()
URL_DELETE = '%s_delete' % MODEL_NAME.lower()
URL_CREDENTIAL = '%s_credential' % MODEL_NAME.lower()
INCLUDE_PATH = 'frontend/includes/%s/list.html' % API_NAME
CONTEXT = dict(
    api_name = API_NAME,
    model_name = MODEL_NAME, 
    include_path =  INCLUDE_PATH, 
    url_create = URL_CREATE, 
    url_update = URL_UPDATE,
    url_delete = URL_DELETE,
    url_credential = URL_CREDENTIAL,
    credential_json = CREDENTIAL_JSON,
    # wizardform = WizardForm(prefix='wizard', jsonform=jsonform, initial={'firstname': 'Afahounko', 'lastname': 'Danny', 'age': 37, 'occupation': 'engineer'}),
    # credentialform = WizardForm(prefix='crendential', jsonform=libvirtform, initial={'username': 'userec2', 'password': 'secret_password'}),

    )


CONTEXT.update({ "{}_active".format(API_NAME): 'active', })




def usersecrets(request):

    wizardboxes_fields = dict()
    wizardboxes_fields = get_apidata("wizardboxes", request)

    apidata = get_apidata(API_NAME, request)

    # CONTEXT.update({ 'apidata': apidata, })
    CONTEXT.update({ 'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields, })

    return render(request, 'frontend/includes/%s/index.html' % API_NAME, CONTEXT)

def usersecrets_list(request):

    wizardboxes_fields = dict()
    wizardboxes_fields = get_apidata("wizardboxes", request)

    apidata = get_apidata(API_NAME, request)

    # CONTEXT.update({ 'apidata': apidata, })
    CONTEXT.update({ 'apidata': apidata, 'wizardboxes_fields': wizardboxes_fields, })

    return render(request, 'frontend/includes/%s/list.html' % API_NAME, CONTEXT)


def usersecrets_form(request, kind):
    # jsonform = DICT_CREDENTIALS.get("sshkey")
    jsonform = DICT_CREDENTIALS.get(kind)
    data = {'data': jsonform}
    return JsonResponse(data)


@csrf_exempt
def usersecrets_create(request):

    # jsonform = DICT_CREDENTIALS.get("kvm")

    kind = "secret"
    jsonform = DICT_CREDENTIALS.get(kind)

    hiddeninputs = dict(
        kind=kind,
        schema=jsonform,
        )

    CONTEXT.update(dict(
        credentialform = WizardForm(prefix='credential', jsonform=jsonform, initial={}),
        hiddeninputs = hiddeninputs,
        ))

    if request.method == 'POST':
        form = ahomeForm(request.POST)
    else:
        form = ahomeForm()

    return save_form(request, form, 'frontend/includes/%s/create.html' % API_NAME, 'create', API_NAME, MODEL_NAME, CONTEXT)


def usersecrets_update(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/update.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)




def usersecrets_credential(request, pk):
    

    instance = get_object_or_404(MODEL_OBJ, pk=pk)

    jsonform = instance.schema

    initial = instance.inputs

    hiddeninputs = dict(
        kind = instance.kind,
        schema = instance.schema,
        )

    CONTEXT.update(dict(
        credentialform = WizardForm(prefix='credential', jsonform=jsonform, initial=initial),
        hiddeninputs = hiddeninputs,
        ))

    if request.method == 'POST':
        form = ahomeForm(request.POST, instance=instance)
    else:
        form = ahomeForm(instance=instance)
    return save_form(request, form, 'frontend/includes/%s/credential.html' % API_NAME, 'update', API_NAME, MODEL_NAME, CONTEXT)





def usersecrets_delete(request, pk):


    instance = get_object_or_404(MODEL_OBJ, pk=pk)
    
    data = dict()
    
    if request.method == 'POST':
        
        instance.delete()

        data['form_is_valid'] = True  # This is just to play along with the existing code

        apidata = get_apidata(API_NAME, request)

        CONTEXT.update({ 'apidata': apidata, 'ops': 'delete', })
        
        data['html_model_list'] = render_to_string('frontend/includes/%s/list.html' % API_NAME, CONTEXT)
        
        data['html_toast_notification'] = render_to_string('frontend/includes/helpers/alert-success.html', CONTEXT)

        data['html_search_nav'] = render_to_string('frontend/includes/helpers/search.html', CONTEXT)

    else:
  
        CONTEXT.update({ 'instance': instance, })
        data['html_form'] = render_to_string('frontend/includes/%s/delete.html' % API_NAME,
            CONTEXT,
            request=request,
        )
    return JsonResponse(data)







