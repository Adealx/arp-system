import csv
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from .models import Customer
from .forms import CustomerForm



def dashboard(request):
    search_query = request.GET.get('search')

    if search_query:
        customers = Customer.objects.filter(name__icontains=search_query)
    else:
        customers = Customer.objects.all()

    form = CustomerForm()

    if request.method == 'POST':

        if 'add_customer' in request.POST:
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')

        elif 'record_payment' in request.POST:
            customer_name = request.POST.get('customer_name')
            payment = request.POST.get('payment')

            try:
                customer = Customer.objects.get(name=customer_name)
                customer.paid += int(payment)
                customer.save()
            except:
                pass

            return redirect('/')

        elif 'delete_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            Customer.objects.get(id=customer_id).delete()
            return redirect('/')

    total_outstanding = sum(customer.balance for customer in customers)
    total_customers = customers.count()
    fully_paid = customers.filter(invoice__lte=0).count()
    owing_customers = total_customers - fully_paid

    context = {
        'customers': customers,
        'form': form,
        'total_outstanding': total_outstanding,
        'total_customers': total_customers,
        'fully_paid': fully_paid,
        'owing_customers': owing_customers,
    }

    return render(request, 'dashboard.html', context)


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


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customers.pdf"'

    p = canvas.Canvas(response)

    y = 800
    p.drawString(100, y, "Accounts Receivable Report")

    customers = Customer.objects.all()

    y -= 40

    for customer in customers:
        line = f"{customer.name} | Invoice: {customer.invoice} | Paid: {customer.paid} | Balance: {customer.balance}"
        p.drawString(50, y, line)
        y -= 30

    p.save()

    return response
def send_reminder(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    send_mail(
        'Payment Reminder',
        f'Dear {customer.name}, your outstanding balance is {customer.balance}. Kindly make payment.',
        settings.EMAIL_HOST_USER,
        [customer.email],
        fail_silently=False,
    )

    return HttpResponse("Reminder email sent successfully!")

