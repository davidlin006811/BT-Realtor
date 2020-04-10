from django.shortcuts import get_object_or_404, redirect
from listings.models import Listing
from .models import Contact
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def index(request):
    if request.method == "POST":
        listing_id = request.POST['listing_id']
        listing = get_object_or_404(Listing, pk=listing_id)
        user_id = request.POST['user_id']
        
        
        if Contact.objects.all().filter(Q(user_id = user_id) and Q(listing_id=listing_id)).exists():
           
            messages.error(request,'You have already made an inquery for this listing')
        
        else:
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            message = request.POST['message']
            realtorEmail = request.POST['realtor_email']
            contact = Contact(user_id = user_id, name = name, email = email, phone=phone, message=message, listing=listing, listing_id = listing_id)
            contact.save()
            # Send email
            send_mail(
                'Property Listing Inquiry',
                'There has been an inquery for' + listing + '. Sign into the admin panel for more info',
                'davidlin006811@gmail.com',
                [realtorEmail],
                fail_silently = False
            )
            messages.success(request, 'Your request has been submited, a realtor will get back to you soon')
       
        return redirect('/listings/'+ listing_id)