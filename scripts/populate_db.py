import csv

from api.models import Source, Country, Brand, Category, Link, Product
from api.utils.check_progress import print_progress

with open("ProductLink.csv", 'r') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)

    reader = list(reader)
    l = len(reader)

    print('Started..')
    print_progress(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, row in enumerate(reader):
        source, created = Source.objects.get_or_create(source=row[0])
        country, created = Country.objects.get_or_create(country=row[1])
        brand, created = Brand.objects.get_or_create(brand=row[2])
        category, created = Category.objects.get_or_create(category=row[3])
        link, created = Link.objects.get_or_create(link=row[4])

        if Product.objects.filter(source=source, country=country, brand=brand, category=category, link=link).exists():
            continue
        else:
            Product(source=source, country=country, brand=brand, category=category, link=link).save()

        print_progress(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

    print('Done!')
    exit()
