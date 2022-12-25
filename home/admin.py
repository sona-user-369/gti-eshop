from django.contrib import admin

from .models import *

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):

    list_display = ("id","image1", "nom", "stock","prix", "categorie",)

    list_filter = ("nom", "stock", "date_de_stock", "prix", "categorie",)

    fieldsets = (
        ("Liste de produit", {
            "fields": ("image1",


                       "nom",
                       "date_de_stock",
                       "stock",


                       "prix",
                       "categorie",

                       )
        }),
    )

# Register your models here.
