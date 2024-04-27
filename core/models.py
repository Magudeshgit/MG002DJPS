from django.db import models
import json

# Customer Dependencies

class stock(models.Model):
    productname = models.CharField(max_length=70, db_index=True)
    category = models.CharField(max_length=50)
    maximumstock = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.productname
    
    def get_incoming(self):
        return self.maximumstock - self.quantity
    
class client(models.Model):
    clientname = models.CharField(max_length=50)
    contactnumber = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.clientname
    
    def billcount(self):
        return bill.objects.filter(client=self.pk,billstatus=False).count()

class bill(models.Model):
    client = models.ForeignKey(client, on_delete=models.CASCADE, blank=True)
    #billno = models.CharField(max_length=10, blank=True)
    billdate = models.DateField(auto_now_add=True, blank=True)
    billstatus = models.BooleanField(default=False) #Bill Closed/Open
    products = models.JSONField(blank=True) #Will hold product name/quantiy and bill pricing details(discount/grandtotal/subtotal)
    grandtotal = models.CharField(max_length=10,blank=True)


    def __str__(self):
        return str(self.billdate)
    
    def get_products(self):
        return json.loads(self.products)

    def set_products(self, products):
        self.products = json.dumps(products)

    def get_client(self):
        return self.client.all()

# Employee Dependencies

class labor(models.Model):
    laborname = models.CharField(max_length=50)
    contactnumber = models.CharField(max_length=20)
    address = models.TextField()
    salarystatus = models.BooleanField(default=False)
    day_wage = models.PositiveIntegerField(blank=True)
    salary_amount = models.PositiveBigIntegerField(blank=True)

    def __str__(self):
        return self.laborname
    
class attendance(models.Model):
    date = models.DateField(auto_now_add=True)
    absentees = models.ManyToManyField(labor)

    def __str__(self):
        return str(self.date)
    
    def absent(self):
        a=[]
        for i in self.absentees.all():
            a.append(i.laborname)
        return a