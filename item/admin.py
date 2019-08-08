from django.contrib import admin
from .models import *



class ImagesInline (admin.TabularInline):
    model = ItemImage
    readonly_fields = ('image_tag', )
    extra = 0


class ItemsInline (admin.TabularInline):
    model = Item
    extra = 0

class ItemsInlineCollections (admin.TabularInline):
    model = Item.collection.through
    extra = 0

class FilterInline(admin.TabularInline):
    model = Filter
    extra = 0

class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name','article','price','discount',]
    #list_display = [field.name for field in Item._meta.fields]
    inlines = [ImagesInline]
    search_fields = ('name_lower', 'article')
    list_filter = ('subcategory', 'collection', 'is_active', 'is_present', 'is_new', 'is_reserved',)
    exclude = ['name_slug','buys','views', 'name_lower'] #не отображать на сранице редактирования
    class Meta:
        model = Item

    def make_new(modeladmin, request, queryset):
        queryset.update(is_new=True)

    def make_not_new(modeladmin, request, queryset):
        queryset.update(is_new=False)

    def make_reserved(modeladmin, request, queryset):
        queryset.update(is_reserved=True)

    def make_not_reserved(modeladmin, request, queryset):
        queryset.update(is_reserved=False)
    
    def make_present(modeladmin, request, queryset):
        queryset.update(is_present=True)
    def make_not_present(modeladmin, request, queryset):
        queryset.update(is_present=False)

    def make_active(modeladmin, request, queryset):
        queryset.update(is_active=True)
    def make_not_active(modeladmin, request, queryset):
        queryset.update(is_active=False)
    make_new.short_description = "Отметить все отмеченные товары новинкой"
    make_not_new.short_description = "Отметить все отмеченные товары НЕ новинкой"
    make_reserved.short_description = "Отметить все отмеченные товары в резерве"
    make_not_reserved.short_description = "Отметить все отмеченные товары НЕ в резерве"
    make_present.short_description = "Отметить все отмеченные товары в наличии"
    make_not_present.short_description = "Отметить все отмеченные товары НЕ в наличии"
    make_active.short_description = "Отметить все отмеченные товары как активные"
    make_not_active.short_description = "Отметить все отмеченные товары как НЕ активные"

    actions = [make_new, make_not_new, make_reserved, make_not_reserved, make_present,
               make_not_present, make_active, make_not_active]
class SubcatAdmin(admin.ModelAdmin):
    # list_display = ['name','discount']
    list_display = [field.name for field in SubCategory._meta.fields]
    inlines = [ FilterInline]
    exclude = ['name_slug','views'] #не отображать на сранице редактирования
    class Meta:
        model = SubCategory

class CollectionAdmin(admin.ModelAdmin):
   # inlines = [ItemsInlineCollections]
    exclude = ['name_slug', 'views']
    class Meta:
        model = Collection

class FilterAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name_slug')

admin.site.register(Category)
admin.site.register(SubCategory, SubcatAdmin)
admin.site.register(Filter,FilterAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemImage)
admin.site.register(Collection,CollectionAdmin)
admin.site.register(PromoCode)