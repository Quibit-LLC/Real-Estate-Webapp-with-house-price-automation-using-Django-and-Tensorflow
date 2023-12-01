from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoomForm, AgentForm, SignupForm, AgentRequestForm, RatingForm, EditReviewForm, HouseDataForm
from .models import Room, Review, House,Payments, Agent
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .decorators import unauthenticated_users, allowed_users, admin_only
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q 
import tensorflow as tf# Import joblib to load your trained model
import numpy as np
from django.http import HttpResponse, JsonResponse
import stripe
from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
# Create your views here.
@csrf_protect  
def signup(request):

    #ensuring that the form is saved
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
                return render(request,'signup.html',{'form':form})
    else:            
        form = SignupForm()
    return render(request,'signup.html',{
        'form':form})

def logout(request):
    auth.logout(request)
    return redirect('about/')

@login_required
def index(request):
    room = Room.objects.all()
    context = {
        'room': room,
    }
    return render(request, 'index.html', context)


def about(request):
    house = House.objects.all()
    return render(request,'about.html',{
        "house": house
    })

@login_required
def property(request):
    query=request.GET.get('query','')
    room = Room.objects.filter(is_booked=False).order_by("?")
    house=House.objects.all()
    house_id=request.GET.get('house',0)
    if house_id:
        room=room.filter(house_id=house_id)
    if query:
        room=room.filter(Q(location__icontains=query) | Q(address__icontains=query))

    context = {
        'room': room,
        'query':query,
        'house':house,
        'house_id':int(house_id)
        }
    return render(request, 'property.html', context)


@login_required
#@admin_only

def detail(request, room_id):

    room = get_object_or_404(Room, id=room_id)
    related_room=Room.objects.filter(house=room.house, is_booked=False).exclude(pk=room_id)[0:3]
    agent = Agent.objects.get(pk=room_id)
    context = {
        'room': room,
        'related_rooms':related_room,
        'agent':agent
    }
    return render(request, 'detail.html', context)


def rating(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        rating_form = RatingForm(request.POST or None)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user  # Set the user attribute
            rating.room = room  # Set the room attribute
            rating.save()
            return redirect('index')
    else:
        rating_form = RatingForm()
    
    context = {
        'form': rating_form,
        'room': room
    }
    return render(request, 'review.html', context)

@login_required
@allowed_users(allowed_roles=['agents', 'staff'])

def add_house(request):

    if request.method == 'POST':
        room_form = RoomForm(request.POST, request.FILES)
        agent_form = AgentForm(request.POST, request.FILES)
        

        if room_form.is_valid() and agent_form.is_valid():
            # Save the Room object
            room = room_form.save(commit=False)
            room.created_by = request.user
            room.save()

            # Associate the agent with the specific room
            agent = agent_form.save(commit=False)
            agent.user = request.user  # Set the user field
            agent.room = room
            agent.save()



            return redirect('property')  # Redirect to a success page
    else:
        room_form = RoomForm()
        agent_form = AgentForm()

    context = {
        'room_form': room_form,
        'agent_form': agent_form,
    }

    return render(request, 'add_house.html', context)



@login_required
def agent_request(request):
    if request.method == 'POST':
        form = AgentRequestForm(request.POST)
        if form.is_valid():
            # Create the RealEstateAgent object and associate it with the current user
            agent = form.save(commit=False)  # Create the agent object but don't save it to the database yet
            agent.user = request.user  # Associate the agent with the current logged-in user
            agent.save()  # Save the agent object to the database
            
            return redirect('agent_application_success')  # Redirect to a success page after successful submission
    else:
        form = AgentRequestForm()

    return render(request, 'agent_request.html', {'form': form})

def agent_application_success(request):
    return render(request, 'agent_application_success.html')


# Add new review

# Edit existing review 
def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('room_detail', review.room.id)
    else:
        form = EditReviewForm(instance=review)
    
    context = {'form': form, 'review': review}
    return render(request, 'detail/edit_review.html', context)


# Delete review
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('room_detail', review.room.id)
    return render(request, 'detail/delete_review.html', {'review': review})

def advert(request):
    return render(request,'advert.html')


# Load your trained model here
model = tf.keras.models.load_model('home_price.h5')

def predict_price(request):
    if request.method == 'POST':
        form = HouseDataForm(request.POST)
        if form.is_valid():
            # Get the form data and preprocess it
            #form.save()
            data = form.cleaned_data
            input_data = [data['area'], data['bedrooms'], data['bathrooms'], data['stories'], data['mainroad'],
                          data['guestroom'], data['basement'], data['hotwaterheating'], data['airconditioning'],
                          data['parking']]
            # Convert input_data to a NumPy array
            input_data = np.array(input_data).reshape(1, -1)
            # Make a prediction using your trained model
            predicted_price = model.predict([input_data])

            # Display the prediction result
            return render(request, 'prediction_success.html', {'predicted_price': predicted_price[0]})

    else:
        form = HouseDataForm()

    return render(request, 'prediction_form.html', {'form': form})


def prediction_success(request):
    return render(request, 'prediction_success.html')


#stripe payments
# This is your test secret API key.
stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

YOUR_DOMAIN = 'http://127.0.0.1:8000'  # Update with your Django app's domain

class CreateCheckoutSessionView(View):
    def create_checkout_session(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Payments.objects.get(id=product_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price_data':{
                            'currency':'usd',
                            'unit_amount':product.price,
                            'product_data':{
                                'name':product.name
                            },
                        },
                        'quantity':1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return JsonResponse({
                "id": checkout_session['id'],
            })
        except Exception as e:
            return HttpResponse(str(e), status=500)

        #return redirect(checkout_session.url, code=303)

class PremiumPage(TemplateView):
    template_name='premium.html'
    def get_context_data(self, **kwargs):
        product = Payments.objects.get(name="Pro")
        context = super(PremiumPage, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY
        })
        return context
    

class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"