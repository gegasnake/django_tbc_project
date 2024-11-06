from modeltranslation.translator import translator, TranslationOptions
from .models import Product  # example model


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # Fields you want to translate


translator.register(Product, ProductTranslationOptions)
