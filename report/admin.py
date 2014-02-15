from django.contrib import admin
from report.models import Client, ClientCrossshop, ClientModelMomentum

admin.site.register(Client)
admin.site.register(ClientCrossshop)
admin.site.register(ClientModelMomentum)