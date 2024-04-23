from django.db import models
import json

# Customer Dependencies

class stock(models.Model):
    productname = models.CharField(max_length=70, db_index=True)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.productname
    
class client(models.Model):
    clientname = models.CharField(max_length=50)
    contactnumber = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.clientname
    

class bill(models.Model):
    client = models.ManyToManyField(client)
    # billno = models.CharField(max_length=10)
    billdate = models.DateField(auto_now_add=True)
    billstatus = models.BooleanField(default=False) #Bill Closed/Open
    products = models.JSONField() #Will hold product name/quantiy and bill pricing details(discount/grandtotal/subtotal)
    grandtotal = models.CharField(max_length=10)


    def __str__(self):
        return str(self.billdate)
    
    def get_products(self):
        return json.loads(self.products)

    def set_products(self, products):
        self.products = json.dumps(products)

# Employee Dependencies

class labor(models.Model):
    laborname = models.CharField(max_length=50)
    contactnumber = models.CharField(max_length=20)
    address = models.TextField()
    salarystatus = models.BooleanField(default=False)

    def __str__(self):
        return self.laborname
    