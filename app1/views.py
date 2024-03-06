from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import pickle
import pandas as pd

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if (uname == '') or (email == '') or (pass1 == '') or (pass2 == ''):
            return HttpResponse("Empty Field")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def ContactPage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mail = request.POST.get('mail')
        message = request.POST.get('message')

        email_message = f"Name: {name}\nEmail: {mail}\n\n{message}"
        send_mail('Contact Form', email_message, settings.EMAIL_HOST_USER, ['spranjul2592@gmail.com'], fail_silently=False)
    return render(request, 'contact.html')

def AboutPage(request):
    return render(request, 'about.html')


def recommendations(moviename):
    movie_index = movies[movies["Name"] == moviename].index[0]
    similarities = list(enumerate(similarity[movie_index]))
    sorted_similarities = sorted(
        similarities, key=lambda x: x[1], reverse=True)[0:6]
    recommended_movie = []
    recommended_movie_poster = []
    recommended_movie_id = []
    for i in sorted_similarities:
        recomended_movies_tilte = movies.iloc[i[0]]["Name"]
        recomended_movies_post = movies.iloc[i[0]]["poster"]
        recomended_movies_id1 = movies.iloc[i[0]]["ID"]

        recommended_movie.append(recomended_movies_tilte)
        recommended_movie_poster.append(recomended_movies_post)
        recommended_movie_id.append(recomended_movies_id1)
    return recommended_movie, recommended_movie_poster, recommended_movie_id

def fetch_selected_movie_detials(selected_movie_name):
    data = used_data[used_data["Name"] == selected_movie_name]
    overview = data["Overview"].values[0]
    title = data["Name"].values[0]
    genre = data["Genre"].values[0]
    runtime = str(data["Runtime"].values[0]) + " min"
    rating = "⭐ " + str(data["Rating"].values[0])
    director = data["Director"].values[0]
    actor = str(data["Actors"].values[0])[1:-1]
    overview = data["Overview"].values[0]
    return title, genre, runtime, rating, director, actor, overview



def ReviewPage(request):
    if request.method == 'POST':
        moviename = request.POST.get('moviename')
        recommended_movie, recommended_movie_poster, recommended_movie_id = recommendations(moviename)
        title, genre, runtime, rating, director, actor, overview = fetch_selected_movie_detials(moviename)

        return render(request, 'recommendation.html',{'recommended_movie': recommended_movie,
                'recommended_movie_poster': recommended_movie_poster,'recommended_movie_id': recommended_movie_id,
                'title': title, 'genre': genre, 'runtime': runtime, 'rating': rating, 'director': director,
                'actor': actor, 'overview': overview})
    return render(request, 'recommendation.html')


movie_data = pickle.load(open("movie_data4.pkl", "rb"))
movies = pd.DataFrame(movie_data)
movie_list = movies["Name"].values
similarity = pickle.load(open("similarity3.pkl", "rb"))
used_data = pickle.load(open("used_data.pkl", "rb"))
used_data = pd.DataFrame(used_data)

