from shelf.models import Category, Product
def Context(request):
    category = Category.objects.all()
    for cat in category:
        cat.count = Product.objects.filter(categories =cat).count()
    context = {
        'category':category
    }
    return context