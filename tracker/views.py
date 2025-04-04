from django.shortcuts import render, HttpResponseRedirect
from .models import *
from datetime import datetime
from django.db.models import Sum
import calendar
from django.db.models.functions import ExtractYear
import csv
from io import TextIOWrapper

# Create your views here.
def index(request):
    """
    View function for the index page of the budget tool.
    """
    # Retrieve 5 most recent transactions from the database to display on the index page
    # This will fetch the latest 5 transactions from the database
    transactions = Transaction.objects.all()
    # Retrieve all categories from the database
    categories = Category.objects.all()  # Get all categories from the database
    sources = Source.objects.all()  # Retrieve all sources from the database, if needed for future use
    # Pass the transactions and categories to the template context
    today = datetime.now().strftime("%Y-%m-%d")  # Get today's date in the format YYYY-MM-DD for any future use in the template
    context = {
        'transactions': transactions,  # Pass the latest transactions to the template
        'categories': categories,  # Pass all categories to the template
        'sources': sources,  # Pass all sources to the template, if needed
        'today': today  # Pass today's date to the template for any future use
    }
    # print(context)
    # Render the index.html template
    return render(request, "tracker/index.html", context)

def add_transaction(request):
    """
    View function for adding a transaction.
    This is a placeholder and will be implemented later.
    """
    # create a new transaction and handle the form submission
    # print(request.POST)
    if not request.POST:
        # If the request is not a POST, redirect to the index page
        return HttpResponseRedirect("/")
    if not 'description' in request.POST:
        # If the 'description' field is not in the POST data, redirect to the index page
        # This is a simple validation check
        return HttpResponseRedirect("/")
    if not 'amount' in request.POST:
        # If the 'amount' field is not in the POST data, redirect to the index page
        # This is a simple validation check
        return HttpResponseRedirect("/")
    if not 'date' in request.POST or not is_valid_date(request.POST['date']):
        # If the 'date' field is not in the POST data, redirect to the index page
        # This is a simple validation check
        return HttpResponseRedirect("/")
    if not 'category' in request.POST or not 'source' in request.POST:
        # If neither category nor source is provided, use default values
        # Redirect to the index page
        return HttpResponseRedirect("/")
    
    try:
        category = Category.objects.get(id=request.POST['category'])  # Get the category object from the database
    except Category.DoesNotExist:
        # If the category does not exist, set it to None
        # This will allow the transaction to be saved without a category
        category = None
    try:
        source = Source.objects.get(id=request.POST['source'])  # Get the source object from the database
    except Source.DoesNotExist:
        # If the source does not exist, set it to None
        # This will allow the transaction to be saved without a source
        source = None
    
    new_transaction = Transaction(description=request.POST['description'],amount=request.POST['amount'],date=request.POST['date'],category=category, source=source)
    new_transaction.save()  # Save the new transaction to the database

    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def add_category(request):
    """
    View function for adding a new category.
    This is a placeholder and will be implemented later.
    """
    if not request.POST:
        # If the request is not a POST, redirect to the index page
        return HttpResponseRedirect("/")
    
    if not 'name' in request.POST:
        # If the 'name' field is not in the POST data, redirect to the index page
        return HttpResponseRedirect("/")
    
    new_category, created = Category.objects.get_or_create(name=request.POST['name'], budget=request.POST['budget'])
    new_category.save()  # Save the new category to the database

    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def add_source(request):
    """
    View function for adding a new source.
    This is a placeholder and will be implemented later.
    """
    if not request.POST:
        # If the request is not a POST, redirect to the index page
        return HttpResponseRedirect("/")
    
    if not 'name' in request.POST:
        # If the 'name' field is not in the POST data, redirect to the index page
        return HttpResponseRedirect("/")
    
    new_source, created = Source.objects.get_or_create(name=request.POST['name'])
    new_source.save()  # Save the new source to the database

    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def settings_page(request):
    """
    View function for the settings page.
    This is a placeholder and will be implemented later.
    """
    categories = Category.objects.all()  # Retrieve all categories from the database
    for category in categories:
        category.annual_budget = category.budget * 12  # Calculate the annual budget for each category
        category.negative_budget = category.budget * -1
        category.annual_negative_budget = category.annual_budget * -1
    sources = Source.objects.all()
    transactions = Transaction.objects.all()  # Retrieve all transactions from the database, if needed for future use
    today = datetime.now().strftime("%Y-%m-%d")  # Get today's date in the format YYYY-MM-DD for any future use in the template

    # Pass the categories and sources to the template context
    context = {
        'categories': categories,  # Pass all categories to the template
        'sources': sources,  # Pass all sources to the template
        'transactions': transactions,  # Pass all transactions to the template, if needed
        'today': today  # Pass today's date to the template for any future use
    }
    return render(request, "tracker/settings.html", context)

def edit_source(request, source_id):
    """
    View function for editing an existing source.
    """
    try:
        source = Source.objects.get(id=source_id)  # Retrieve the source to edit
    except Source.DoesNotExist:
        # If the source does not exist, redirect to the settings page
        return HttpResponseRedirect("/settings/")

    if request.method == "POST":
        # If the request is a POST, update the source name
        if 'name' in request.POST and request.POST['name']:
            source.name = request.POST['name']
            source.save()  # Save the updated source to the database
            return HttpResponseRedirect("/settings/")
    
    # Render the edit source template with the current source details
    context = {'source': source}
    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def edit_category(request, category_id):
    """
    View function for editing an existing category.
    """
    try:
        category = Category.objects.get(id=category_id)  # Retrieve the category to edit
    except Category.DoesNotExist:
        # If the category does not exist, redirect to the settings page
        return HttpResponseRedirect("/settings/")

    # print(request.POST)

    if request.method == "POST":
        # If the request is a POST, update the category name
        if 'name' in request.POST:
            category.name = request.POST['name']
            category.save()  # Save the updated category to the database
            # print(category.name)
        if 'amount' in request.POST:
            try:
                # Attempt to convert the budget to a decimal
                category.budget = float(request.POST['amount'])
                category.save()  # Save the updated budget to the database
                # print(category.budget)
            except ValueError:
                print("Invalid budget value")  # Handle invalid budget input
        return HttpResponseRedirect("/settings/")  # Redirect to the settings page after saving

    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def edit_transaction(request, transaction_id):
    """
    View function for editing an existing transaction.
    """
    try:
        transaction = Transaction.objects.get(id=transaction_id)  # Retrieve the transaction to edit
    except Transaction.DoesNotExist:
        # If the transaction does not exist, redirect to the index page
        return HttpResponseRedirect("/")

    if request.method == "POST":
        # If the request is a POST, update the transaction details
        if 'description' in request.POST and request.POST['description']:
            transaction.description = request.POST['description']
        if 'amount' in request.POST and request.POST['amount']:
            transaction.amount = request.POST['amount']
        if 'date' in request.POST and is_valid_date(request.POST['date']):
            transaction.date = request.POST['date']
        if 'category' in request.POST:
            transaction.category_id = request.POST['category']
        if 'source' in request.POST:
            transaction.source_id = request.POST['source']
        
        transaction.save()  # Save the updated transaction to the database
        return HttpResponseRedirect("/")  # Redirect to the index page after saving
    
    # Render the edit transaction template with the current transaction details
    context = {'transaction': transaction}
    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def delete_source(request, source_id):
    """
    View function for deleting an existing source.
    """
    try:
        source = Source.objects.get(id=source_id)  # Retrieve the source to delete
        source.delete()  # Delete the source from the database
    except Source.DoesNotExist:
        # If the source does not exist, redirect to the settings page
        pass
    
    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def delete_category(request, category_id):
    """
    View function for deleting an existing category.
    """
    try:
        category = Category.objects.get(id=category_id)  # Retrieve the category to delete
        category.delete()  # Delete the category from the database
    except Category.DoesNotExist:
        # If the category does not exist, redirect to the settings page
        pass
    
    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)

def delete_transaction(request, transaction_id):
    """
    View function for deleting an existing transaction.
    """
    try:
        transaction = Transaction.objects.get(id=transaction_id)  # Retrieve the transaction to delete
        transaction.delete()  # Delete the transaction from the database
    except Transaction.DoesNotExist:
        # If the transaction does not exist, redirect to the index page
        pass
    
    # Get the referring URL or use a default if it's not available
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    # Redirect to the referring URL
    return HttpResponseRedirect(referring_url)


def reports_view(request):
    year_values = (
        Transaction.objects.annotate(year=ExtractYear("date"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("year")
    )
    # Handle month/year selection
    month = int(request.GET.get("month", datetime.today().month))
    year = int(request.GET.get("year", datetime.today().year))
    
    transactions = Transaction.objects.filter(date__month=month, date__year=year, amount__lt=0)

    income_total = Transaction.objects.filter(date__month=month, date__year=year, category__name='income').aggregate(total=Sum('amount'))

    income_total_amount = income_total['total'] if income_total['total'] else 0

    print(income_total_amount)
    # print(transactions)
    
    # Pie chart data (by category)
    pie_data = transactions.values("category__name").annotate(total=Sum("amount")*-1)

    # Line chart data (cumulative spend by date)
    daily_totals = (
        transactions.order_by("date")
        .values("date")
        .annotate(daily_total=Sum("amount"))
    )
    cumulative_total = 0
    line_data = [{"date": datetime(year, month, 1).strftime("%Y-%m-%d"), "cumulative": 0}]
    for item in daily_totals:
        cumulative_total += item["daily_total"] * -1
        line_data.append({"date": item["date"].strftime("%Y-%m-%d"), "cumulative": cumulative_total})
    
    total_spent = float(sum([x["total"] for x in pie_data]))

    # Convert pie chart data to JSON-safe format
    pie_data_safe = []
    for item in pie_data:
        total = float(item["total"])
        percentage = total / total_spent * 100
        budget = float(Category.objects.get(name=item["category__name"]).budget) if Category.objects.filter(name=item["category__name"]).exists() else 0
        surplus = abs(budget - total)
        pie_data_safe.append({
            "category__name": item["category__name"],
            "total": total,
            "percentage": percentage,
            "budget": budget,
            "surplus": surplus,
        })


    # Convert line chart data to JSON-safe format
    line_data_safe = [
        {"date": item["date"], "cumulative": float(item["cumulative"])}
        for item in line_data
    ]

    context = {
        "selected_month": month,
        "selected_year": year,
        "income": income_total_amount,
        "total_spent": total_spent,
        "pie_data": pie_data_safe,
        "line_data": line_data_safe,
        "months": [(i, calendar.month_name[i]) for i in range(1, 13)],
        "years": list(year_values),
    }


    return render(request, "tracker/reports.html", context)

def import_csv_preview(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        decoded_file = TextIOWrapper(csv_file.file, encoding="utf-8")
        reader = csv.DictReader(decoded_file)
        # print("HEADERS:", reader.fieldnames)


        column_aliases = {
            "description": ["description", "desc", "details"],
            "amount": ["amount", "amt", "value"],
            "date": ["date", "transaction date", "timestamp"],
            "category": ["category", "type", "label"],
            "source": ["source", "payment method", "account", "wallet", "account/card from"],
        }

        # Map lowercase header -> original header
        header_map = {header.lower().strip(): header for header in reader.fieldnames}

        # Map desired keys to original headers
        column_map = {}
        for key, aliases in column_aliases.items():
            for alias in aliases:
                if alias.lower() in header_map:
                    column_map[key] = header_map[alias.lower()]
                    break


        # Store headers + rows in session for confirmation step
        preview_rows = []
        rows = []
        for i, row in enumerate(reader):
            # print("RAW CSV ROW:", row)
            if i < 10:  # Show only first 10 rows
                preview_rows.append({k: row.get(v, "") for k, v in column_map.items()})
            rows.append({k: row.get(v, "") for k, v in column_map.items()})

        request.session["csv_data"] = {
            "rows": rows,
            "column_map": column_map,
        }
        # print(preview_rows)

        return render(request, "tracker/import_preview.html", {
            "preview_rows": preview_rows,
            "column_map": column_map,
        })

    return HttpResponseRedirect("/")

def import_csv_confirm(request):
    data = request.session.get("csv_data", {})
    if not data:
        return HttpResponseRedirect("/")

    column_map = data.get("column_map", {})
    rows = data.get("rows", [])

    for row in rows:
        try:
            category = row.get("category")
            source = row.get("source")
            category_obj = Category.objects.get_or_create(name=category)[0] if category else None
            source_obj = Source.objects.get_or_create(name=source)[0] if source else None

            # Clean date format from m/d/yy to YYYY-MM-DD
            date_str = row.get("date")
            if date_str:
                try:
                    date_cleaned = datetime.strptime(date_str, "%m/%d/%y").date()
                except ValueError:
                    # Handle invalid date format
                    date_cleaned = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                date_cleaned = None

            # Clean amount format from $1,234.56 to 1234.56
            amount_str = row.get("amount")
            if amount_str:
                amount_cleaned = float(amount_str.replace("$", "").replace(",", ""))
            else:
                amount_cleaned = None
            
            Transaction.objects.get_or_create(
                description=row["description"],
                amount=amount_cleaned,
                date=date_cleaned,
                category=category_obj,
                source=source_obj,
            )
        except Exception as e:
            print(f"Error importing row: {row} — {e}")

    # Clear session after import
    del request.session["csv_data"]

    return HttpResponseRedirect("/")

