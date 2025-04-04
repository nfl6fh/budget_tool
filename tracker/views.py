from django.shortcuts import render, HttpResponseRedirect
from .models import *
import re
from datetime import datetime

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
    print(context)
    # Render the index.html template
    return render(request, "tracker/index.html", context)

def add_transaction(request):
    """
    View function for adding a transaction.
    This is a placeholder and will be implemented later.
    """
    # create a new transaction and handle the form submission
    print(request.POST)
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
        category.negative_budget = category.budget * -1
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

    print(request.POST)

    if request.method == "POST":
        # If the request is a POST, update the category name
        if 'name' in request.POST:
            category.name = request.POST['name']
            category.save()  # Save the updated category to the database
            print(category.name)
        if 'amount' in request.POST:
            try:
                # Attempt to convert the budget to a decimal
                category.budget = float(request.POST['amount'])
                category.save()  # Save the updated budget to the database
                print(category.budget)
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