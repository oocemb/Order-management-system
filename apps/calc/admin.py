from django.contrib import admin

from calc.models import (
    Calc, CalcTag, Comment, Detail, Ldstp, CategoryFurniture, FurnitureInCalc, Furniture
)


admin.site.register(Calc)
admin.site.register(CalcTag)
admin.site.register(Comment)
admin.site.register(Detail)
admin.site.register(Ldstp)
admin.site.register(CategoryFurniture)
admin.site.register(FurnitureInCalc)


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ("category", "article", "title", "price", "price_retail", "availability")
    list_display_links = ("title",)
    list_filter = ("category__title", "availability")
    search_fields = ("category__title", "title", "price", "price_retail")
