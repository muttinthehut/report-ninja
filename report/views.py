# Create your views here.

# jpb, added for report test only
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
# jpb, I added this in an attempt to return child data as JSON
from django.core import serializers
import json

# jpb, added new views for report models and testing
from report.models import Client
from report.models import ClientCrossshop
from django.views.generic import ListView

def index(request):
   #  return HttpResponse("Hello from Report app")
       # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('index.html', context_dict, context)
    
def report(request):
    return render_to_response('report.html')
    
def client_report(request, client_id=1):
    return render_to_response('client_report.html',{'client':Client.objects.get(id=client_id) })

## jpb, 2/7 THIS WORKED AND ALLOWED ME TO GET ALL CHILDREN BACK FROM PARENT CLASS  
##   locals() will create the dictionary automagically
##   'shops' is the variable that contains the info

def client_name(request, client_id=1):
    client = Client.objects.get(id=client_id)
#   jpb, this worked
    bogus_shops = client.shops.all()
    shops = serializers.serialize('json',bogus_shops)
    bogus_dmm = client.dmm.filter(active='Y')
    dmm = serializers.serialize('json',bogus_dmm)
#    bogus_hitlist = client.hitlist.all()
#    hitlist = serializers.serialize('json',bogus_hitlist)
    hitlist = client.hitlist.all()
    return render_to_response('client.html',locals(),context_instance=RequestContext(request))
#    return render_to_response('market_report.html',locals(),context_instance=RequestContext(request))


## jpb, 2/13 THIS VIEW IS FOR THE BOOTSTRAP MOCKUP SHOWING LIVE CHARTS
##  IT IS BASED ON THE PREVIOUS VIEW (Client_Name) but uses "Client_REport.html" 
###  WHICH EXTENDS the template "base.html" to produce D3.JS charts
def client_sample(request, client_id=1):
    client = Client.objects.get(id=client_id)
#   jpb, this worked
    bogus_shops = client.shops.all()
    shops = serializers.serialize('json',bogus_shops)
    bogus_dmm = client.dmm.all()
    dmm = serializers.serialize('json',bogus_dmm)
    bogus_hitlist = client.hitlist.all()
    hitlist = serializers.serialize('json',bogus_hitlist)
    return render_to_response('client_report.html',locals(),context_instance=RequestContext(request))
#    return render_to_response('market_report.html',locals(),context_instance=RequestContext(request))

## jpb, 2/13, THIS VIEW GENERATES A CLIENT CROSS SHOP CHART ONLY
def client_crossshops(request, client_id=1):
    client = Client.objects.get(id=client_id)
#   jpb, this worked
    bogus_shops = client.shops.all()
    shops = serializers.serialize('json',bogus_shops)
    bogus_dmm = client.dmm.filter(active='Y')
    dmm = serializers.serialize('json',bogus_dmm)
    bogus_hitlist = client.hitlist.all()
    hitlist = serializers.serialize('json',bogus_hitlist)

    return render_to_response('client_crossshops.html',locals(),context_instance=RequestContext(request))

## jpb, 2/13, THIS VIEW GENERATES A DMM CHART ONLY
def client_dmm(request, client_id=1):
    client = Client.objects.get(id=client_id)
#   jpb, this worked
    bogus_shops = client.shops.all()
    shops = serializers.serialize('json',bogus_shops)
    bogus_dmm = client.dmm.all()
    dmm = serializers.serialize('json',bogus_dmm)
    return render_to_response('client_dmm.html',locals(),context_instance=RequestContext(request))


## jpb, 2/13, THIS VIEW GENERATES A HITLIST ONLY
def client_hitlist(request, client_id=1):
    client = Client.objects.get(id=client_id)
    hitlist = client.hitlist.all()
    return render_to_response('client_hitlist.html',locals(),context_instance=RequestContext(request))


    
# A JSON view of the crossshop requests    
def client_crossshop(request, myid=1):
    crossshops_as_json = serializers.serialize('json',ClientCrossshop.objects.filter(client_id=myid))
    return HttpResponse(crossshops_as_json, content_type = 'json')
    
def get_model_shops(request):
    return render(request,'client_report.html',{'client_model_shops':ClientCrossshop})
    
def shops(request, myid=1):
    clientobj = ClientCrossshop.objects.filter(client_id=myid)
    crossshops_as_json = serializers.serialize('json',clientobj)
    # return HttpResponse(crossshops_as_json, content_type = 'json')
    return render_to_response('shops.html',{'crossshops':clientobj})
    
    
    