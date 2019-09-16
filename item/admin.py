from django.contrib import admin
from .models import *



class ImagesInline (admin.TabularInline):
    model = ItemImage
    readonly_fields = ('image_tag', )
    exclude = ('image_small',)
    extra = 0

class PriceInline (admin.TabularInline):
    model = ItemPrice
    extra = 0

class ItemsInline (admin.TabularInline):
    model = Item.subcategory.through
    extra = 0

# class ItemsInlineCollections (admin.TabularInline):
#     model = Item.collection.through
#     extra = 0

class FilterInline(admin.TabularInline):
    model = Filter
    extra = 0

class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name']
    #list_display = [field.name for field in Item._meta.fields]
    inlines = [PriceInline,ImagesInline]
    search_fields = ('name_lower',)
    list_filter = ('subcategory', 'is_active', 'is_present',)
    exclude = ['name_slug', 'name_lower', 'zapah', 'views', 'buys',
               'discount', 'page_title', 'page_description', 'page_keywords'] #не отображать на сранице редактирования
    class Meta:
        model = Item

    def make_present(modeladmin, request, queryset):
        queryset.update(is_present=True)
    def make_not_present(modeladmin, request, queryset):
        queryset.update(is_present=False)

    def make_active(modeladmin, request, queryset):
        queryset.update(is_active=True)
    def make_not_active(modeladmin, request, queryset):
        queryset.update(is_active=False)

    make_present.short_description = "Отметить все отмеченные товары в наличии"
    make_not_present.short_description = "Отметить все отмеченные товары НЕ в наличии"
    make_active.short_description = "Отметить все отмеченные товары как активные"
    make_not_active.short_description = "Отметить все отмеченные товары как НЕ активные"
    actions = [make_present, make_not_present, make_active, make_not_active]

class SubcatAdmin(admin.ModelAdmin):
    # list_display = ['name','discount']
    list_display = ['name','is_active','views']#[field.name for field in SubCategory._meta.fields]
    exclude = ['name_slug','views','discount','image','short_description','description'] #не отображать на сранице редактирования
    class Meta:
        model = SubCategory

class SubSubcatAdmin(admin.ModelAdmin):
    # list_display = ['name','discount']
    list_display = ['name','is_active','views']#[field.name for field in SubSubCategory._meta.fields]
    inlines = [ FilterInline,ItemsInline]
    exclude = ['name_slug','views','discount','image','short_description','description'] #не отображать на сранице редактирования
    class Meta:
        model = SubSubCategory

class CatAdmin(admin.ModelAdmin):
    # list_display = ['name','discount']
    list_display = ['name','is_active','views']#[field.name for field in Category._meta.fields]
    exclude = ['name_slug','views','image','short_description','description'] #не отображать на сранице редактирования
    class Meta:
        model = Category

class FilterAdmin(admin.ModelAdmin):
    search_fields = ('name', 'name_slug')

admin.site.register(Category,CatAdmin)
admin.site.register(SubCategory, SubcatAdmin)
admin.site.register(SubSubCategory, SubSubcatAdmin)
admin.site.register(Filter,FilterAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemImage)

admin.site.register(PromoCode)