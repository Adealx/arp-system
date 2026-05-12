from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm
from django.db import models
import csv
from django.http import HttpResponse

@login_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    customers = Customer.objects.filter(name__icontains=search_query)

    form = CustomerForm()

    if request.method == 'POST':

        if 'delete_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            Customer.objects.get(id=customer_id).delete()
            return redirect('/')

        elif 'edit_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            invoice = int(request.POST.get('invoice'))
            paid = int(request.POST.get('paid'))

            customer = Customer.objects.get(id=customer_id)
            customer.invoice = invoice
            customer.paid = paid
            customer.save()
            return redirect('/')

        elif 'record_payment' in request.POST:
            name = request.POST.get('customer_name')
            payment = int(request.POST.get('payment'))

            customer = Customer.objects.get(name=name)
            customer.paid += payment
            customer.save()
            return redirect('/')

        else:
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
        'form': form,
        'total_outstanding': total_outstanding,
        'total_customers': total_customers,
        'fully_paid': fully_paid,
        'owing_customers': owing_customers
    })


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Invoice', 'Paid', 'Balance', 'Date Added'])

    customers = Customer.objects.all()

    for customer in customers:
        writer.writerow([
            customer.name,
            customer.invoice,
            customer.paid,
            customer.balance,
            customer.created_at
        ])

    return response