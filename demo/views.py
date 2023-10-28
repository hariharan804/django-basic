import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from db_connection import client, db
from .forms import UserForm
from .models import users_collection
import time


# Create your views here.


def home(request):
    collection_count = len(db.list_collection_names())

    # Get the total user count
    total_user_count = users_collection.count_documents({})

    # Get the count of verified users
    verified_user_count = users_collection.count_documents({"verified_profile": True})

    # Get the count of unverified users
    unverified_user_count = users_collection.count_documents({"verified_profile": False})

    # for document in user_data:
    #     print(document)
    context = {
        'browser_details': request.META['HTTP_USER_AGENT'],
        'total_user_count': total_user_count,
        'verified_user_count': verified_user_count,
        'unverified_user_count': unverified_user_count,
        'connected_db': db.name,
        'db_connect_time': test(),
        'collection_count': collection_count
    }
    return render(request, 'home.html', context=context)


def test():
    start_time = time.time()
    client.db_name.command('ping')
    end_time = time.time()

    return "{:.3f}".format(end_time - start_time)


def view_all_users(request):
    user_data = users_collection.find({})
    print(user_data)
    context = {"user_data": user_data}
    return render(request, 'view_all_users.html', context=context)


def delete_user(request):
    if request.method == 'POST':
        post_data = request.body
        try:
            post_data = post_data.decode('utf-8')
            post_data_json = json.loads(post_data)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return HttpResponse("Invalid JSON data in the request body", status=400)

        result = users_collection.delete_one({'email': post_data_json['document_email']})

        # Check if the document was successfully deleted
        if result.deleted_count == 1:
            response_data = {'message': 'User deleted successfully'}
        else:
            response_data = {'message': 'User not found or could not be deleted'}

        return JsonResponse(response_data)


def user_form(request, email=''):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email_id = form['email'].value()
            new_user = {
                "name": form['name'].value(),
                "email": form['email'].value(),
                "age": form['age'].value(),
                "verified_profile": form.cleaned_data.get('profile_verified'),
                "mobile_number": form['mobile_number'].value(),
            }
            update_data = {'$set': new_user}
            # Process form data  save to database
            if email:
                result = users_collection.update_one({email: email_id}, update_data, upsert=True)
                if result.modified_count == 0:
                    print("Document inserted.")
                else:
                    print("Document updated.")

            else:
                result = users_collection.insert_one(new_user)
            if result.acknowledged:
                print("User Added successfully with ID:", result)
                return redirect('view-all-users')
            else:
                print("User insertion failed.")

    # Redirect or display a success message
    else:
        if email:
            old_user = users_collection.find_one({"email": email})
            form = UserForm(old_user)
        else:
            form = UserForm()

    return render(request, 'user_form.html', {'form': form})
