from django.shortcuts import render, redirect, HttpResponse
from .models import User, UserManager, Quote, QuoteManager, Likes, CheckManager
from django.contrib import messages
import bcrypt


# Create your views here.

def index(request):
    users = User.objects.all()
    context = {
        "all_users": users
    }
    return render(request, "index.html", context)

# Successful login page
def successDisplay(request, user_Val):
    users = User.objects.get(id = user_Val)
    quotes = Quote.objects.all()
    filter_quotes = Quote.objects.filter().order_by('-id')[:3]
    all_users = User.objects.all()

    if "user" not in request.session:
        return redirect("/")
    context = {
        "create_user": users,
        "these_quotes": quotes,
        "the_users": all_users,
        "three_quotes": filter_quotes,
    }
    return render(request, "BookPage.html", context)

# Create a new user
def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    password = request.POST['type_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
    print(pw_hash) 
    
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        # print("*"*50, "\n", errors)
        return redirect("/")
    else:
        newUser = User.objects.create(first_name = request.POST["type_first_name"], 
        last_name = request.POST["type_last_name"], email = request.POST["type_email"],
        password = pw_hash)

        request.session['user'] = newUser.id
        return redirect(f"/success/{newUser.id}")
    
# Checks if their is a user that exist in the database
def validate_login(request):
    user = User.objects.filter(email=request.POST['type_login_email']) 
    print(user)
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['type_login_password'].encode(), logged_user.password.encode()):
            request.session["user"] = logged_user.id
            print("password match")
            return redirect("/success/{}".format(logged_user.id))
        else:
            print("failed password")
            messages.error(request, "Invalid password")
            return redirect("/")
    messages.error(request, "No account associated to email")
    print ("No account associated to email")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")


# Show adding/creating a book/author
def AddQuote(request):

    quoteError = Quote.objects.getValid(request.POST)
    this_user_id = User.objects.get(id = request.session['user'])
    ok_user = this_user_id.id

    if len(quoteError) > 0:
        for v in quoteError.items():
            messages.error(request, v)
        return redirect(f"/success/{ok_user}")
    else:
    # this_user_id = User.objects.get(id = request.session['user'])
        create_quote = Quote.objects.create(quote = request.POST['quote_add'], uploaded_by = this_user_id)
    # ok_user = this_user_id.id
        return redirect(f"/success/{ok_user}")

# Viewing the user's page
def view_this_user(request, user_ID):
    ok_user = User.objects.get(id = request.session['user'])
    context = {
        "this_user": ok_user,
        
    } 
    return render(request, "EditPage.html", context)

def editProcess(request, the_id):

    the_user = User.objects.get(id = request.session['user'])

    errors = User.objects2.check_validator(post_data=request.POST, request=request.session)

    if len(errors) > 0:
        for value in errors.items(): 
            messages.error(request,value)
        return redirect(f"/myaccount/{the_user.id}")
    # if len(request.POST["change_first"]) < 3:
    #     messages.error(request, "First Name should be at least 3 characters or more")
    # if len(request.POST["change_last"]) < 2:
    #     messages.error(request, "Last Name should be at least 2 characters or more")
    # if email 

    the_user.first_name = request.POST["change_first"]
    the_user.last_name = request.POST["change_last"]
    the_user.email = request.POST["change_email"]
    the_user.save()
    return redirect(f"/myaccount/{the_user.id}")

def view_other_users(request, this_user):
    other_user = User.objects.get(id = this_user)
    quotes = Quote.objects.filter(uploaded_by = other_user)
    this_user = User.objects.get(id=request.session['user'])
    all_user = User.objects.all()
    my_likes = Likes.objects.all()

    context = {
        "this_user": other_user,
        "make_quotes": quotes,
        "user": this_user,
        "users": all_user,
        "this_likes": my_likes,
        
    } 
    return render(request, "viewUser.html", context)

def putLikes(request, other_user_id):
    this_user = User.objects.get(id=request.session['user'])
    my_id = this_user.id

    the_other_user = User.objects.get(id = other_user_id)

    getQuote = Quote.objects.get(id=request.POST["id"])

    found_user = False
    for l in getQuote.my_likes.all():
        if l.get_like_user.id == my_id:
            found_user = True
            break
    if not found_user:
        Likes.objects.create(mylike = 0, related_quote = getQuote, get_like_user = this_user)

    return redirect(f"/users/{the_other_user.id}")

def delquote(request, get_id):
    del_quote = Quote.objects.get(id=get_id)
    del_quote.delete()
    this_user = User.objects.get(id=request.session['user'])
    return redirect(f"/success/{this_user.id}") 

def unlikeButton(request, other_id):
    this_user = User.objects.get(id=request.session['user'])
    my_id = this_user.id

    the_other_user = User.objects.get(id = other_id)

    getQuote = Quote.objects.get(id=request.POST["bad_id"])

    found_user = False
    for l in getQuote.my_likes.all():
        if l.get_like_user.id == my_id:
            l.delete()
            found_user = True
            break
    if not found_user:
        return redirect(f"/users/{the_other_user.id}")

    return redirect(f"/users/{the_other_user.id}")
