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

# jpb, added for user auth
from report.forms import ClientForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# jpb, added for email testing
from django.views.generic.base import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context


from django.http import HttpResponseRedirect



# view to point to home page (index.html)
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

# jpb, 2-24 added user_login
def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

#jpb, 2/24, added user log out
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
    
# jpb, 2/24/ now working
def register(request):
        # Get the requests context.
        context = RequestContext(request)
        
        # A boolean value for telling the template whether the registration was successful.
        # Set to false initially.  Code changes to TRUE when registration succeeds.
        registered = False

        # If it's a HTTP Post , we're interested in processing form data.
        if request.method == 'POST':
            # Attempt to grab info from the raw form information.
            # Note that we make use of User Form (in the original example there was a "UserProfileFOrm" that had 
            #  Additional attributes
            user_form = UserForm(data=request.POST)

            # if the form is valid...
            if user_form.is_valid():
                user = user_form.save()
                
                # Now hash the password with the set_password method.
                # once hashed, update the user object.
                user.set_password(user.password)
                user.save()
                
                # Update variable to tell registration was successful
                registered = True
            
            # Invalid form - mistakes, etc.
            # reject and show to user
            else:
                print user_form.errors
            
        # If it's not an HTTP POST we render the form as blank, ready for user input.
        else:
            user_form = UserForm()
            
        # Render the template depending on the context
        return render_to_response('register.html', {'user_form':user_form,'registered':registered},context)
        

## END OF REGISTRATION


## START OF DASHBOARD (NOT MARKET REPORT, BUT USER DASHBOARD)

## jpb, 2/28 added dashboard
@login_required
def dashboard(request):
    context = RequestContext(request)
    
    return render_to_response('dashboard.html', {}, context)

## end of dashboard

## jpb, 3/1, START OF EMAIL VIEWS
def sendmktrpt(request, client_id=1):
    client=Client.objects.get(id=client_id)
    bogus_shops = client.shops.all()
    shops = serializers.serialize('json',bogus_shops)
    bogus_dmm = client.dmm.filter(active='Y')
    dmm = serializers.serialize('json',bogus_dmm)
    hitlist = client.hitlist.all()

    subject = "Market Report Test"
    to = ['JoeB615@gmail.com']
    from_email = 'jburns@dataium.com'
    ctx = {
        'client_id':2
    }
    
    message = get_template('client.html').render(Context(ctx))
    msg = EmailMessage(subject,message,to=to,from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()
    return HttpResponse('email sent')
    
## jpb, END OF EMAIL VIEWS

## START OF MARKET REPORT

## jpb, 2/7 THIS WORKED AND ALLOWED ME TO GET ALL CHILDREN BACK FROM PARENT CLASS  
##   locals() will create the dictionary automagically
##   'shops' is the variable that contains the info
##    this is main report - don't remove
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



## jpb, 2/13, THIS VIEW GENERATES A CLIENT CROSS SHOP CHART ONLY - DON"T REMOVE
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


    
def get_model_shops(request):
    return render(request,'client_report.html',{'client_model_shops':ClientCrossshop})




## VIEWS NOT USED BELOW
## THESE ARE OLD AND NOT USED

## This is old report.  can be removed
def report(request):
    return render_to_response('report.html')
    
## this is old sample report, not used    
def client_report(request, client_id=1):
    return render_to_response('client_report.html',{'client':Client.objects.get(id=client_id) })

## jpb, 2/13 NOT USED ANYMORE
##  THIS VIEW IS FOR THE BOOTSTRAP MOCKUP SHOWING LIVE CHARTS
##  IT IS BASED ON THE PREVIOUS VIEW (Client_Name) but uses "Client_REport.html" 
###  WHICH EXTENDS the template "base.html" to produce D3.JS charts
##   THIS IS NOT USED ANYMORE
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

## old sample - not used    
def shops(request, myid=1):
    clientobj = ClientCrossshop.objects.filter(client_id=myid)
    crossshops_as_json = serializers.serialize('json',clientobj)
    # return HttpResponse(crossshops_as_json, content_type = 'json')
    return render_to_response('shops.html',{'crossshops':clientobj})
    