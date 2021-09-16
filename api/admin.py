import csv

from django.contrib import admin
from django.http import HttpResponse

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

from api.models import Source, Brand, Link, Product, Category, Country


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


class ProductResource(resources.ModelResource):
    source = fields.Field(column_name='source', attribute='source',
                          widget=ForeignKeyWidget(Source, 'source'))

    country = fields.Field(column_name='country', attribute='country',
                           widget=ForeignKeyWidget(Country, 'country'))

    brand = fields.Field(column_name='brand', attribute='brand',
                         widget=ForeignKeyWidget(Brand, 'brand'))

    category = fields.Field(column_name='category', attribute='category',
                            widget=ForeignKeyWidget(Category, 'category'))

    link = fields.Field(column_name='link', attribute='link',
                        widget=ForeignKeyWidget(Link, 'link'))

    class Meta:
        model = Product
        fields = ('source', 'country', 'brand', 'category', 'link')
        import_id_fields = ['source', 'country', 'brand', 'category', 'link']


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
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

    resource_class = ProductResource


admin.site.register(Brand)
admin.site.register(Source)
admin.site.register(Link)

