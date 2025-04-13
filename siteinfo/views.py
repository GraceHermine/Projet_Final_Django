from django.shortcuts import render
from .models import Faq, Politique,Conditions,Equipe,Propos
# Create your views here.

def faq(request):
    faqs = Faq.objects.filter(statut=True).order_by('-created_at')

    datas = {
        'faqs': faqs
    }
    return render(request, 'faq.html', datas)




def policy(request):
    politique = Politique.objects.filter(statut=True).order_by('created_at')
    
    datas = {
        'politique': politique
    }
    return render(request, 'privacy-policy.html', datas)

def notfound(request):
    datas = {

    }
    return render(request, '404.html', datas)



def contact(request):
    datas = {
    

    }
    return render(request, 'contact.html', datas)

def service(request):
    conditions = Conditions.objects.filter(statut=True).order_by('created_at')
    datas = {
        'cond': conditions
    }
    return render(request, 'services.html', datas)



# Début du about
def about(request):

    membres = Equipe.objects.filter(statut=True)
    
    propos = Propos.objects.filter(statut=True).first()
    datas = {
        
        'propos': propos,
        'membres': membres,
    }

    return render(request, 'about.html', datas)
#  Fin du about