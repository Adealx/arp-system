from django.shortcuts import render, redirect
from django.db import models
from .models import Customer
from .forms import CustomerForm


def dashboard(request):
    customers = Customer.objects.all()
    form = CustomerForm()

    if request.method == 'POST':

        if 'delete_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            Customer.objects.get(id=customer_id).delete()
            return redirect('/')

        elif 'record_payment' in request.POST:
            name = request.POST.get('customer_name')
            payment = int(request.POST.get('payment'))

            customer = Customer.objects.get(name=name)
            customer.paid += payment
            customer.save()
            return redirect('/')

        elif 'add_customer' in request.POST:
            form = CustomerForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('/')

    total_outstanding = sum(customer.balance for customer in customers)
    total_customers = customers.count()
    fully_paid = customers.filter(invoice__lte=models.F('paid')).count()
    owing_customers = total_customers - fully_paid

    return render(request, 'dashboard.html', {
        'customers': customers,
        'total_outstanding': total_outstanding,
        'total_customers': total_customers,
        'fully_paid': fully_paid,
        'owing_customers': owing_customers,
        'form': form
    })