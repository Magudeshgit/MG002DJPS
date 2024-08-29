from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import stock, client, bill, labor, attendance
from .models import salarymanagement as salaryobj
from django.utils import timezone
from django.db.models import Sum, Q
from json import JSONDecodeError
#from easy_pdf.rendering import render_to_pdf_response
import json

months = [
"January", "February", "March", "April", "May", "June",
"July", "August", "September", "October", "November", "December"
]

def home(request):
    return HttpResponse("Home page")
@login_required(login_url='/auth/signup/')
def dashboard(request):
    model = stock.objects.all()
    # MonthlyReport.objects.get_or_create(month=months[timezone.localdate().month])
    ovdc = model.order_by('productname')
    model_bills = bill.objects.filter(billstatus='opened')
    ic_stock  = 0
    for i in model:
        if i.quantity < i.maximumstock:
            ic_stock+=1

    

    context = {
        'overviewdata':ovdc.reverse()[:5],
        'stockcount': model.count(),
        'iccount': ic_stock,
        'billcount': model_bills.count(),
        'salarydue': salaryobj.objects.aggregate(Sum('salarydue'))['salarydue__sum']
        }
    
    return render(request, "core/dashboard.html", context)   

def stocks(request):
    stocks = stock.objects.all()
    if request.method == 'POST':
        i = request.POST.get('id')
        c = stock.objects.filter(Q(id__icontains=i) | Q(productname__icontains = i))
        print(c)
        return render(request, "core/stocks.html", {'stocks':c}) 

    return render(request, "core/stocks.html", {'stocks':stocks})

def incomingstocks(request):
    stocks = stock.objects.all()
    return render(request, "core/incomingstocks.html", {'stocks':stocks})

def damagedmaterials(request):
    return render(request, "core/damagedmaterials.html")

def addstock(request):
    created=False
    if request.method == 'POST':
        _productname = request.POST.get('productname')
        _category = request.POST.get('category')
        _quantity = request.POST.get('quantity')
        _price = request.POST.get('price')

        stock.objects.create(productname = _productname, category=_category, maximumstock=_quantity,quantity=_quantity, price=_price)
        created=True
    return render(request, "core/addstock.html", context={"created": created})

def editstock(request,pk):
    created=False
    prod = stock.objects.get(id=pk)
    if request.method == 'POST':
        _productname = request.POST.get('productname')
        _category = request.POST.get('category')
        _quantity = request.POST.get('quantity')
        _price = request.POST.get('price')
        #temp= int(prod.maximumstock)
        # temp += _quantity

        prod.productname = _productname
        prod.category=_category
        prod.maximumstock=int(_quantity)
        prod.quantity=int(_quantity)
        prod.price=_price
        prod.save()
        created=True
    return render(request, "core/editstock.html", context={"created": created, "editinfo": prod})

def deletestock(request,pk):
    prod = stock.objects.get(id=pk)
    prod.delete()
    return redirect('/stocks')

def addcustomer(request):
    created=False
    if request.method == 'POST':
        _customername = request.POST.get('customername')
        _contact = request.POST.get('contact')
        _address = request.POST.get('address')

        client.objects.create(
            clientname=_customername,
            contactnumber=_contact,
            address = _address
        )

        created=True
    return render(request, "core/addclient.html", context={'created':created})

def editcustomer(request,pk):
    created=False
    cust = client.objects.get(id=pk)
    if request.method == 'POST':
        _customername = request.POST.get('customername')
        _contact = request.POST.get('contact')
        _address = request.POST.get('address')

        cust.clientname = _customername
        cust.contactnumber=_contact
        cust.address=_address
        cust.save()
        created=True
    return render(request, "core/editclient.html", context={"created": created, "editinfo": cust})

def deletecustomer(request,pk):
    cust = client.objects.get(id=pk)
    cust.delete()
    return redirect('/clientbook')

def addlabor(request):
    created=False
    if request.method == 'POST':
        _laborname = request.POST.get('laborname')
        _contact = request.POST.get('contact')
        _address = request.POST.get('address')
        _daywage = request.POST.get('daywage')
        _salary = request.POST.get('salary')

        laborobj = labor.objects.create(
            laborname=_laborname,
            contactnumber=_contact,
            address = _address,
            day_wage=_daywage,
            salary_amount=_salary
        )
        
        opb = salaryobj.objects.create(
            employee=laborobj,
            absentdays=0,
            salarydue = _salary
        )
        created=True
    return render(request, "core/addlabor.html", {'created':created})

def editlabor(request,pk):
    created=False
    cust = labor.objects.get(id=pk)
    if request.method == 'POST':
        _laborname = request.POST.get('laborname')
        _contact = request.POST.get('contact')
        _address = request.POST.get('address')

        cust.laborname = _laborname
        cust.contactnumber=_contact
        cust.address=_address
        cust.save()
        created=True
    return render(request, "core/editlabor.html", context={"created": created, "editinfo": cust})

def deletelabor(request,pk):
    cust = labor.objects.get(id=pk)
    cust.delete()
    return redirect('/laborbook')

def salarymanagement(request):
    salary = salaryobj.objects.all()
    context = {
        'salary':salary,
        'salsum': salary.aggregate(Sum('salarydue'))['salarydue__sum'],
        'labcount': labor.objects.all().count()
        }
    return render(request, 'core/salarymanagement.html', context)

def editsalary(request, pk):
    ss = salaryobj.objects.get(id=pk)
    print(request.method)
    if request.method == 'POST':
        print("POST REQUEST", request.POST)
        transtype = request.POST.get('type')
        reason = request.POST.get('reason')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        
        _transaction = [transtype,reason,amount,date]
        if transtype == 'Addition':
            ss.salarydue += int(amount)
        else:
            ss.salarydue -= int(amount)

        if ss.transaction is None:
            ss.transaction = json.dumps({"transaction": [_transaction]})
            ss.save()
        else:
            a = json.loads(ss.transaction)
            b = a['transaction'].append(_transaction)
            ss.transaction = json.dumps(a)
            ss.save()
    return render(request, 'core/editsalary.html', {'editinfo': ss, 'transacts': ss.transaction})

def bills(request):
    bill_ = bill.objects.all()
    _bill = reversed(bill_)
    if request.method == "POST":
        search_param = request.POST.get("searchparam")
        c = client.objects.filter(Q(clientname__icontains=search_param) | Q(contactnumber__icontains=search_param))
        print("Asdad",search_param,c)
        if len(c) >= 1:
            searched_bills = bill.objects.filter(Q(client=c[0]))
            print("search",searched_bills)
            return render(request, "core/bills.html", {"bills":searched_bills})
        else:
            return render(request, "core/bills.html", {"status": {"bills": None}})
        
    context = {'bills':_bill}
    return render(request, "core/bills.html", context)

def newbill(request):

    # Measurement Based Billing Materials Initialization
    measitems = ['PVC பந்தல்', 'Carpet (Flower Red)', 'Carpet (Red)', 'Carpet (Green)']

    if request.method == 'POST':
        customer = request.POST.get('customer')
        items = request.POST.get('items')
        billstatus = request.POST.get('billstatus')
        vehiclerent = request.POST.get('vehiclerent')
        totaldays = request.POST.get('totaldays')
        subtotal = request.POST.get('subtotal')
        discount = request.POST.get('discount')
        grandtotal = request.POST.get('grandtotal')
        items = json.loads(items)
        jsondata = {'items': items, 'totaldays':totaldays, 'vehiclerent': vehiclerent,'subtotal': subtotal, 'discount': discount, 'grandtotal': grandtotal}
        jsondata = json.dumps(jsondata)

        
        if billstatus == 'opened':
            for i in items:
                if not i[0] in measitems:
                    _product = stock.objects.get(productname=i[0])
                    _product.quantity = _product.quantity - int(i[1])
                    _product.save()

        _customer, status = client.objects.get_or_create(clientname=customer)
        new_bill = bill.objects.create(client=_customer,products=jsondata,billstatus=billstatus,grandtotal=int(grandtotal))   
        new_bill.save()
    
    clients = client.objects.values_list('clientname')
    stocks = stock.objects.values_list('productname')
    clients = json.dumps(list(clients.values()))
    stocks = json.dumps(list(stocks.values()))
    
    context = {"clients": clients, "products": stocks}
    return render(request, "core/newbill.html", context)

def reviewbill(request,pk=None):
    if request.method == 'POST':
        customer = request.POST.get('customer')
        items = request.POST.get('items')
        vehiclerent = request.POST.get('vehiclerent')
        _billstatus = request.POST.get('billstatus')
        subtotal = request.POST.get('subtotal')
        discount = request.POST.get('discount')
        grandtotal = request.POST.get('grandtotal')


        try:
            items = json.loads(items)
        except JSONDecodeError:
            items = {"items": [["None","None", "None"]], "subtotal": "None", "discount":"None", "grandtotal":"None"}


        jsondata = {'items': items,'vehiclerent':vehiclerent, 'subtotal': subtotal, 'discount': discount, 'grandtotal': grandtotal}
        jsondata = json.dumps(jsondata)

        # Handling Central Stock

        _customer = client.objects.get(clientname=customer)
        obj = bill.objects.get(id=pk)
        obj.products=jsondata
        obj.grandtotal=int(grandtotal)
        obj.client = _customer

        if _billstatus == 'opened':
            for i in items:
                _product = stock.objects.get(productname=i[0])
                _product.quantity = _product.quantity - int(i[1])
                _product.save()
        else:
            for i in items:
                _product = stock.objects.get(productname=i[0])
                _product.quantity = _product.quantity + int(i[1])
                _product.save()
        obj.billstatus = _billstatus
        obj.save()

        return redirect('/bills')

    clients = client.objects.values_list('clientname')
    stocks = stock.objects.values_list('productname')
    clients = json.dumps(list(clients.values()))
    stocks = json.dumps(list(stocks.values()))

    _editbill = bill.objects.get(id=pk)
    context = {'bill': _editbill, 'customer': _editbill.client, 'items': _editbill.products, "clients": clients, "products": stocks}
    return render(request, "core/editbill.html", context)

def clientbook(request):
    clients = client.objects.all()
    context = {'clients': clients}
    return render(request, "core/clientbook.html", context)

def laborbook(request):
    labors = labor.objects.all()
    return render(request, "core/laborbook.html", {'labors': labors})

def attendancemanagement(request):
    attendances, status = attendance.objects.get_or_create(date=timezone.now())
    labors = labor.objects.all()
    if request.method == 'POST':
        _absentees = request.POST.get('absentees')
        _absentees = json.loads(_absentees) 
        attendances.absentees.clear()
        for i in _absentees:
            _labor = labors.get(laborname=i)
            attendances.absentees.add(_labor)
            sal = salaryobj.objects.get(employee=_labor)
            sal.update_absentdays(value=1)
            sal.save()

    return render(request, "core/attendancemanagement.html", {'attendance': attendances, 'labors':labors, 'status':status})

def attendancerecords(request):
    attendances = attendance.objects.all()
    labors = labor.objects.all()
    return render(request, "core/attendancerecord.html", {'attendance': attendances, 'labors':labors})

def testinvoice(request, pk):
    _bill = bill.objects.get(id=pk)
    _stock = stock.objects.all()
    
    stocks = stock.objects.values_list('productname')
    stocks = json.dumps(list(stocks.values()))
    return render(request, 'core/printtemplate.html', {'bill':_bill, 'stock': stocks})

def printinvoice(request, pk):
    _bill = bill.objects.get(id=pk)
    return render(request, 'core/printdocument.html')

def prindoc(request):
    return render(request, 'core/printdocument.html')

# def monthlyreport(request):
#     m = MonthlyReport.objects.get_or_create(month=months[timezone.localdate().month])
    