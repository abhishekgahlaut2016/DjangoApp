from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Register, ProductImage, ProductCategory, BuyerDetail, Cart

# class QuestionAdmin(admin.ModelAdmin):        ###This class is used to change the order of fields in admin panel
#     fields = ['pub_date', 'question_text']

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),            ###This class is used to provede Heading Separator between fields
#     ]




# class ChoiceInline(admin.TabularInline):   ###StackedInline or TabularInline 
#     model = Choice
#     extra = 3


# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),  ###This is used to sho all choices related to that question(foren key field in choice from question) in Question admin panel
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]


class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Register)
admin.site.register(ProductImage)
admin.site.register(ProductCategory)
admin.site.register(BuyerDetail)
admin.site.register(Cart)
