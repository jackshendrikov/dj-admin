import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Link, Category, Brand, Country, Source
from .forms import TestForm


def get_requests(request):
    if request.method == 'GET':
        sorting = request.GET.get('sorting', False)

        products = Product.objects.all().values_list('country__country', 'category__category',
                                                     'brand__brand', 'link__link', 'source__source')

        if sorting:
            if sorting == 'byCountry':
                products = products.order_by('country__country')
            elif sorting == 'bySource':
                products = products.order_by('source__source')

        field_names = ['country', 'category', 'brand', 'link', 'source']

        products = [dict(zip(field_names, product)) for product in products]

        return JsonResponse(products,
                            content_type="application/json", safe=False,
                            json_dumps_params={'indent': 4}, status=200)

        # output = json.dumps({'products': products}, indent=4)
        # content = {
        #     'json_response': output,
        #     'status': 'HTTP 200 OK',
        # }
        # return render(request, 'my_form.html', content, status=200)

    return HttpResponse(status=400)


@csrf_exempt
def post_requests(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            source, created = Source.objects.get_or_create(source=data['source'])
            country, created = Country.objects.get_or_create(country=data['country'])
            brand, created = Brand.objects.get_or_create(brand=data['brand'])
            category, created = Category.objects.get_or_create(category=data['category'])
            link, created = Link.objects.get_or_create(link=data['link'])

            Product(source=source, country=country, brand=brand, category=category, link=link).save()

            # return JsonResponse(data,
            #                     content_type="application/json", safe=False,
            #                     json_dumps_params={'indent': 4}, status=201)

            output = json.dumps(data, indent=4)
            content = {
                'form': form,
                'json_response': output,
                'status': 'HTTP 201 Created',
            }
            return render(request, 'my_form.html', content, status=201)
        else:
            # return JsonResponse(dict(form.errors.items()),
            #                     content_type="application/json", safe=False,
            #                     json_dumps_params={'indent': 4}, status=400)
            output = json.dumps(dict(form.errors.items()), indent=6)
            content = {
                'form': form,
                'json_response': output,
                'status': 'HTTP 400 Bad Request',

            }
            return render(request, 'my_form.html', content, status=400)

    else:
        form = TestForm()

    return render(request, 'my_form.html', {'form': form})
