from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Category,seller
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def home(request):
    products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render (request,'',context)

def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.object.filter(available=True)
    
    if query:
        products = Product.filter(
            Q(name__icontains=query)|
            Q(description__icontains=query)|
            Q(seller_username__icontains=query)
            
        )
        
        
    if category_id:
        products = products.filter(category_id=category_id)
        
        
        products = products.order_by('-created_at')
        
        paginator = paginator(products,12)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        
        
        categories = Category.objects.all()
        
        context = {
            'products': products,
            'categories': categories,
            'query': query,
            'select_category':int(category_id) if category_id else None,
        
        }
        return render(request,'',context)
        
        


@login_required 
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request,"Product added successfully")
            return redirect('')
        
    else:
        form=ProductForm()
    return render()
    
    
@login_required
def update_product(request,pk):
    product=get_object_or_404(Product,pk=pk,seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Product updated successfully")
            return redirect()
        
    else:
        form = ProductForm(instance=product)
    return render()

@login_required
def delete_product(request,pk):
    product=get_object_or_404(Product,pk=pk,seller=request.user)
    
    if seller != request.user:
        messages.error(request,"You cannot delete others product")
        return redirect('')
    
    if request.method == 'POST':
        product.delete()
        messages.success(request,"Product deleted successfully")
        return redirect('')
    return render()


    
    