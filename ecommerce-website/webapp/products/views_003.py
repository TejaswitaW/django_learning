"""This is  product component view"""
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render
# get_object_or_404
from .models import Product

# Create your views here.


class ProductListView(ListView):
    """It shows class based List View"""
    # this is how we make query set
    # it gives everything in the database
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *args, **kwargs):
    #     """Gets context"""
    #     # now we can see our context
    #     context = super(ProductListView, self).get_context_data(
    #         *args, **kwargs)
    #     print(context)
    #     return context


def product_list_view(request):
    """It shows function based List View"""
    queryset = Product.objects.all()
    context = {
        "object_list": queryset,
    }
    return render(request, "products/list.html", context)


class ProductDetailView(DetailView):
    """It shows class based Detail View"""
    # this is how we make query set
    # it gives everything in the database
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        """Gets context"""
        # now we can see our context
        # this is default version of the context data
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context


def product_detail_view(request, pk=None, * args, **kwargs):
    # def product_detail_view(request,* args, **kwargs):
    """It shows function based Detail View"""
    # print(args)
    # print(kwargs)
    # #instance = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product, pk=pk)
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print("No product here")
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("huh?")
    instance = Product.objects.get_by_id(pk)
    print(instance)
    qs = Product.objects.filter(id=pk)
    print(qs)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist")
    context = {
        "object": instance,
    }
    return render(request, "products/detail.html", context)
