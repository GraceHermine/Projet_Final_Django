from django.shortcuts import render

# Create your views here.
def index(request):
    datas = {
        

    }
    return render (request, 'index.html', datas)


def about(request):
    datas = {
    

    }
    return render (request, 'about.html', datas)


def blog(request):
    datas = {
        

    }
    return render (request, 'blog.html', datas)


def blog_detail(request):
    datas = {
    

    }
    return render (request, 'blog-details.html', datas)


def produit(request):
    datas = {
    

    }
    return render (request, 'product-coundown.html', datas)



def shop(request):
    datas = {
    

    }
    return render (request, 'shop-fullwidth.html', datas)



def contact(request):
    datas = {
    

    }
    return render (request, 'contact.html', datas)