import csv

from django.contrib import admin
from django.http import HttpResponse



from api.models import Source, Brand, Link, Product


def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response
export_as_csv.short_description = "Export Selected as CSV"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('source', 'country', 'brand', 'category', 'link')
    list_display_links = ('country', 'category', 'link')
    list_editable = ('source', 'brand')
    list_filter = ('category', 'country', 'brand')
    list_per_page = 30

    actions = [export_as_csv]

    fieldsets = (
        ('Brand', {
            'fields': ('brand', 'category')
        }),
        ('Source', {
            'fields': ('country', 'source', 'link')
        }),
    )


admin.site.register(Brand)
admin.site.register(Source)
admin.site.register(Link)
