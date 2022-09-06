
from django.forms import widgets,ModelForm
from django import forms  
from blog.models import *
from event.models import  * 
from course.models import  * 
from shop.models import *  
  
class blogForm(forms.ModelForm): 
    # def __init__(self, *args, **kwargs):
    #     super(blogForm, self).__init__(*args, **kwargs)
    #     self.fields['blog_title'].widget.attrs.update({
    #             'required':''
    #             ,'name':'title',
    #             'id':'title',
    #             'type':'text',
    #             'class':'form-input',


    #     })
 
    # class Meta:  
    #     model = blog_detail  
    #     fields = "__all__"  
    #     exclude = ('id',) 
             

    class Meta:
        model = blog_detail
        exclude = []
        fields = "__all__"  
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # for field in self.fields.values():
            #     field.widget.attrs['class'] = 'form-control'
            self.fields.widget.attrs.update({'class':''})

  

# from django.contrib.admin import (
#       widgets,
#       site as admin_site
#     )

# def blogForm(Model,listHiddenfield=[],disablefield=[]):

#     data = {field:forms.HiddenInput() for field in listHiddenfield}
#     class newform(forms.ModelForm):
#         class Meta:
#             model = Model
#             # print()
#             # if Model._meta.object_name=='User' and Model._meta.app_label=="UserData":
#             #     fields = ['first_name','last_name','phone','email','last_login','username','dob','profile','gender','date_joined']
#             # else:
#             #     exclude = ('id',) 
#             exclude = ('id',) 
#             widgets = data
#         def __init__(self, *args, **kwargs):
#             super(newform, self).__init__(*args, **kwargs)
#             for f in Model._meta.fields:
#                 try :
#                     self.fields[f.name].widget.attrs['placeholder'] = f"enter here {f.verbose_name}".title  ()
#                 except:
#                     pass
#                 if f.name in disablefield:
#                     self.fields[f.name].widget.attrs['readonly'] = True
#                 if "DateTimeField" in str(type(f)):
#                     try:
#                         self.fields[f.name].widget.attrs['class'] = 'vDateTime'
#                     except Exception:
#                         pass
#                 if "DateField" in str(type(f)):
#                     try:
#                         self.fields[f.name].widget.attrs['class'] = 'vDateField'
#                     except Exception:
#                         pass
#                 if "ForeignKey" in str(type(f)):
#                     try:
#                         self.fields[f.name].widget  = widgets.RelatedFieldWidgetWrapper(
#                         self.fields[f.name].widget,
#                         self.instance._meta.get_field(f.name).remote_field,
#                         admin_site
#                         )
#                         self.fields[f.name].empty_label = f"Select a {f.name}"
#                     except Exception:
#                         pass 
                           
#     return newform  














#         def __init__(self, *args, **kwargs):
#             super(blogForm,self).__init__(*args, **kwargs)
#             for field in self.fields.values():
#                 field.widget.attrs['class'] = 'form-control'
       
#         # def __init__(self, *args, **kwargs):
#         #     super().__init__(*args, **kwargs)
#         #     for visible in self.visible_fields():
#         #         visible.field.widget.attrs['class'] = 'form-control'

    # username = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #     'class':'form-control',
    #     'placeholder':'Username'
    #     }
    # ))
    # password = forms.CharField(widget=forms.PasswordInput(
    #     attrs={
    #     'class':'form-control',
    #     'placeholder':'Password'
    #     }
    # ))









class demoForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)