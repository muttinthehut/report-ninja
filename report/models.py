from django.db import models
from django.core import serializers

# Create your models here.

# The parent client model

class Client(models.Model):
    clientname = models.CharField(max_length=128)
    clientemail = models.EmailField(max_length=50)
    dataiumclientid = models.IntegerField(default=0)
    dataiumreportmonth = models.CharField(max_length=50)
    clientdma = models.CharField(max_length=50)
    clientcity = models.CharField(max_length=50)
    clientstate = models.CharField(max_length=12)
    clientwebsite = models.CharField(max_length=50)
    clientshopimage = models.CharField(max_length=100)
    clientdmmimage = models.CharField(max_length=100)
    clienthitlistimage = models.CharField(max_length=100)
    clientsocialimage = models.CharField(max_length=100)
    clientutilityimage = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.clientname



        
class ClientCrossshop(models.Model):
    client = models.ForeignKey(Client,related_name='shops')
    dataiumclientid = models.IntegerField(default=0)
    clientmodel = models.CharField(max_length=50)
    crossmodel = models.CharField(max_length=50)
    shops = models.IntegerField(default=0)


    def __unicode__(self):
        return ' '.join([self.clientmodel, ',',self.crossmodel,',',str(self.shops),])
        # return '%s,%s,%s' % (self.clientmodel,self.crossmodel,str(self.shops))    
        # return serializers.serialize('json',ClientCrossshop.objects.all())
    



# jpb, 2/10/2014, TO DO:  NEED TO WORK ON THE ERROR IN THE DMM FIELD HERE
# jpb, 2/13/2014 TO DO:   NEED TO ADD THE "CROSS MODEL"  Right now it's using client model (i.e. malibu-fusion, malibu-camry)
class ClientModelMomentum(models.Model):
    client = models.ForeignKey(Client, related_name='dmm')
    dataiumclientid = models.IntegerField(default=0)
    clientmodel = models.CharField(max_length=50)
    yearmonth = models.CharField(max_length=20)
    dmm = models.CharField(max_length=10)
    active = models.CharField(max_length=2)
    
    def __unicode__(self):
        return ' '.join([self.clientmodel,' ',self.yearmonth,' ',self.dmm,])
        
# jpb, 2/13/2014, ADDED Hit List Info
class ClientHitList(models.Model):
    client = models.ForeignKey(Client, related_name='hitlist')
    dataiumclientid = models.IntegerField(default=0)
    stocknumber = models.CharField(max_length=20)
    vehicle = models.CharField(max_length=50)
    shopperindex = models.CharField(max_length=20)
    lastviewed = models.CharField(max_length=20)
    
    def __unicode__(self):
        return ' '.join([str(self.clientid),' ',str(self.dataiumclientid),' ',self.stocknumber,' ',self.vehicle,' ',self.shopperindex,' ', self.lastviewed,])
        
        

        