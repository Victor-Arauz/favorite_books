from django.shortcuts import redirect, render
from .models import Book, User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

@property
def full_name(self):
    return f"{self.first_name} {self.last_name}"

def register(request):

    errors = User.objects.registrationValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    

        newUser = User.objects.create(
            first_name = request.POST['first_name'].title(),
            last_name = request.POST['last_name'].title(),
            email = request.POST['email'],
            password = pw_hash
            )
        
        request.session['loggedInId'] = newUser.id
        request.session['first_name'] = newUser.first_name


    return redirect('/dashboard')

def dashboard(request):
    if 'loggedInId' not in request.session:
        return redirect('/')
    context = {
        'loggedInId': User.objects.get(id= request.session['loggedInId']),
        'allBooks': Book.objects.all(),
        'favorite': Book.objects.all()
    }

    return render(request, 'dashboard.html', context)

def login(request):
    
    # user = User.objects.get(email=request.POST['email'])
    errors = User.objects.loginValidator(request.POST)
    print(errors)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        
        user = User.objects.filter(email=request.POST['email']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            logged_user = user[0] 
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['loggedInId'] = logged_user.id
                # never render on a post, always redirect
        matchingEmail = User.objects.filter(email = request.POST['email'])
        request.session['loggedInId'] = matchingEmail[0].id
        request.session['user'] = matchingEmail[0].first_name

    return redirect('/dashboard')

def create_book(request):

    errors = Book.objects.bookValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    else:
        Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by =  User.objects.get(id= request.session['loggedInId'])
            )    

    return redirect('/dashboard')

def show_book(request, book_id):
    if 'loggedInId' not in request.session:
        return redirect('/')    
    context = {
        'oneBook': Book.objects.get(id= book_id),
    }
    return render(request, 'show_book.html', context)

def edit_book(request, book_id):
    context = {
        'oneBook': Book.objects.get(id= book_id),
    }

    return render(request, 'edit_book.html', context)

def update_book(request, book_id):

    errors = Book.objects.bookValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/book/edit/{book_id}')
    else:
        bookUpdate = Book.objects.get(id= book_id)
        bookUpdate.title =  request.POST['title']
        bookUpdate.desc = request.POST['desc']
        bookUpdate.save()

    return redirect('/dashboard')

def create_favorite_book(request, book_id):
    user = request.session['loggedInId']
    print(user)
    favorite = Book.objects.get(id= book_id)
    print(favorite)
    favorite.users_who_like.add(user)
    
    return redirect('/dashboard')

def delete_favorite_book(request, book_id):
    user = request.session['loggedInId']
    print(user)
    favorite = Book.objects.get(id= book_id)
    print(favorite)
    favorite.users_who_like.remove(user)
    
    return redirect('/dashboard')

def delete_book(request, book_id):
    bookDelete = Book.objects.get(id= book_id)
    bookDelete.delete()

    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')