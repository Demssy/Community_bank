from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from django import forms
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser 
        fields = ['id']  

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])    






class CustomUserAdmin(UserAdmin):
    actions = ['export_users_pdf', 'export_students_pdf', 'export_investors_pdf', 'export_staff_pdf', 'export_is_Active_pdf']
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    def export_users_pdf(self, request, queryset):
        
        status_query = Q(is_student=True) | Q(is_staff=True) | Q(is_investor=True) | Q(is_superuser=True)
        users_queryset = CustomUser.objects.filter(status_query).values('username','first_name','last_name','email','date_of_birth','gender','last_login','date_joined','mailing_address')
        users = list(users_queryset)


        if users:
            students_count = CustomUser.objects.filter(is_student=True).values('is_student').annotate(count=Count('is_student'))[0]['count']
            investors_count = CustomUser.objects.filter(is_investor=True).values('is_investor').annotate(count=Count('is_investor'))[0]['count']
            staff_count = CustomUser.objects.filter(is_staff=True).values('is_staff').annotate(count=Count('is_staff'))[0]['count']
            superuser_count = CustomUser.objects.filter(is_superuser=True).values('is_superuser').annotate(count=Count('is_superuser'))[0]['count']
            active_users = CustomUser.objects.filter(is_active=True).values('is_active').annotate(count=Count('is_active'))[0]['count']
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            content_disposition = request.GET.get('content_disposition', 'attachment')
            response['Content-Disposition'] = f"{content_disposition}; filename=users.pdf"

            # Create the PDF object
            doc = SimpleDocTemplate(response, pagesize=landscape(letter))

            # Container for the 'Flowable' objects
            elements = []

            # Add user data to the PDF
            data = [['Users','First Name', 'Last Name', 'Email','Date of birth','Gender','last_login','date_joined','mailing_address']]
            for user in users:
                data.append([
                    user['username'],
                    user['first_name'],
                    user['last_name'],
                    user['email'],
                    user['date_of_birth'],
                    user['gender'],
                    user['last_login'].strftime("%Y-%m-%d"),
                    user['date_joined'].strftime("%Y-%m-%d"),
                    user['mailing_address'],
                ])
            # Create the table
            table = Table(data)

            # Set the table style
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            # Set the document elements
            elements = []

            # Add a header
            header_text = "Users Table"
            style = getSampleStyleSheet()['Heading1']
            header = Paragraph(header_text, style)
            elements.append(header)

            # Add the counts
            count_text = "Students: {}\nInvestors: {}\nStaff: {}\nSuperusers: {}\nActive Users: {}".format(students_count, investors_count, staff_count, superuser_count, active_users)
            counts = Paragraph(count_text, style)
            elements.append(counts)

            # Add the table
            elements.append(table)


            doc.build(elements)
            return response
        else:
            self.message_user(request, "Please select a user type before generating the pdf.")
    export_users_pdf.short_description = "Export selected users as PDF"






    def export_students_pdf(modeladmin, request, queryset):
        # Retrieve request parameters
        is_student = request.GET.get('is_student', True)
        fields = request.GET.getlist('fields', ['username','first_name','last_name','email', 'college', 'major', 'date_of_birth','gender','last_login','date_joined','mailing_address'])

        # Retrieve user data
        users = CustomUser.objects.filter(is_student=is_student ).values(*fields)
        students_count = CustomUser.objects.filter(is_student=True).values('is_student').annotate(count=Count('is_student'))[0]['count']
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        content_disposition = request.GET.get('content_disposition', 'attachment')
        response['Content-Disposition'] = f"{content_disposition}; filename=student users.pdf"

        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))

        # Container for the 'Flowable' objects
        elements = []

        # Add user data to the PDF
        data = [['Users','First Name', 'Last Name', 'Email','Date of birth', 'Academic Institution', 'Major', 'Gender','last_login','date_joined','mailing_address']]

        for user in users:
            data.append([
                user['username'],
                user['first_name'],
                user['last_name'],
                user['email'],
                user['date_of_birth'],
                user['college'],
                user['major'],
                user['gender'],
                user['last_login'].strftime("%Y-%m-%d"),
                user['date_joined'].strftime("%Y-%m-%d"),
                user['mailing_address'],
            ])
        # Create the table
        table = Table(data)

        # Set the table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Set the document elements
        elements = []

        # Add a header
        header_text = "Student Table"
        style = getSampleStyleSheet()['Heading1']
        header = Paragraph(header_text, style)
        elements.append(header)

        # Add the counts
        count_text = "Students: {}\n".format(students_count)
        counts = Paragraph(count_text, style)
        elements.append(counts)

        # Add the table
        elements.append(table)


        doc.build(elements)
        return response
    export_students_pdf.short_description = "Export Student objects as PDF"







    def export_investors_pdf(modeladmin, request, queryset):
        # Retrieve request parameters
        is_investor = request.GET.get('is_investor', True)
        fields = request.GET.getlist('fields', ['username','first_name','last_name','email','date_of_birth','gender','last_login','date_joined','mailing_address'])

        # Retrieve user data
        users = CustomUser.objects.filter(is_investor=is_investor ).values(*fields)
        investors_count = CustomUser.objects.filter(is_investor=True).values('is_investor').annotate(count=Count('is_investor'))[0]['count']
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        content_disposition = request.GET.get('content_disposition', 'attachment')
        response['Content-Disposition'] = f"{content_disposition}; filename=users.pdf"

        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))

        # Container for the 'Flowable' objects
        elements = []

        # Add user data to the PDF
        data = [['Users','First Name', 'Last Name', 'Email','Date of birth','Gender','last_login','date_joined','mailing_address']]

        for user in users:
            data.append([
                user['username'],
                user['first_name'],
                user['last_name'],
                user['email'],
                user['date_of_birth'],
                user['gender'],
                user['last_login'].strftime("%Y-%m-%d"),
                user['date_joined'].strftime("%Y-%m-%d"),
                user['mailing_address'],
            ])
        # Create the table
        table = Table(data)

        # Set the table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Set the document elements
        elements = []

        # Add a header
        header_text = "Investor Table"
        style = getSampleStyleSheet()['Heading1']
        header = Paragraph(header_text, style)
        elements.append(header)

        # Add the counts
        count_text = "Investors: {}\n".format(investors_count)
        counts = Paragraph(count_text, style)
        elements.append(counts)

        # Add the table
        elements.append(table)


        doc.build(elements)
        return response
    export_investors_pdf.short_description = "Export Investors objects as PDF"








    def export_staff_pdf(modeladmin, request, queryset):
        # Retrieve request parameters
        is_staff = request.GET.get('is_staff', True)
        fields = request.GET.getlist('fields', ['username','first_name','last_name','email','date_of_birth','gender','last_login','date_joined','mailing_address'])

        # Retrieve user data
        users = CustomUser.objects.filter(is_staff=is_staff ).values(*fields)

        staff_count = CustomUser.objects.filter(is_staff=True).values('is_staff').annotate(count=Count('is_staff'))[0]['count']
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        content_disposition = request.GET.get('content_disposition', 'attachment')
        response['Content-Disposition'] = f"{content_disposition}; filename=users.pdf"

        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))

        # Container for the 'Flowable' objects
        elements = []

        # Add user data to the PDF
        data = [['Users','First Name', 'Last Name', 'Email','Date of birth','Gender','last_login','date_joined','mailing_address']]

        for user in users:
            data.append([
                user['username'],
                user['first_name'],
                user['last_name'],
                user['email'],
                user['date_of_birth'],
                user['gender'],
                user['last_login'].strftime("%Y-%m-%d"),
                user['date_joined'].strftime("%Y-%m-%d"),
                user['mailing_address'],
            ])
        # Create the table
        table = Table(data)

        # Set the table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Set the document elements
        elements = []

        # Add a header
        header_text = "Staff Table"
        style = getSampleStyleSheet()['Heading1']
        header = Paragraph(header_text, style)
        elements.append(header)

        # Add the counts
        count_text = "Staff: {}\n".format(staff_count)
        counts = Paragraph(count_text, style)
        elements.append(counts)

        # Add the table
        elements.append(table)


        doc.build(elements)
        return response
    export_staff_pdf.short_description = "Export Staff objects as PDF"



    def export_is_Active_pdf(modeladmin, request, queryset):
        # Retrieve request parameters
        is_active = request.GET.get('is_active', True)
        fields = request.GET.getlist('fields', ['username','first_name','last_name','email','date_of_birth','gender','last_login','date_joined','mailing_address'])

        # Retrieve user data
        users = CustomUser.objects.filter(is_active=is_active ).values(*fields)
        active_users = CustomUser.objects.filter(is_active=True).values('is_active').annotate(count=Count('is_active'))[0]['count']
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        content_disposition = request.GET.get('content_disposition', 'attachment')
        response['Content-Disposition'] = f"{content_disposition}; filename=active users.pdf"

        # Create the PDF object
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))

        # Container for the 'Flowable' objects
        elements = []

        # Add user data to the PDF
        data = [['Users','First Name', 'Last Name', 'Email','Date of birth','Gender','last_login','date_joined','mailing_address']]

        for user in users:
            data.append([
                user['username'],
                user['first_name'],
                user['last_name'],
                user['email'],
                user['date_of_birth'],
                user['gender'],
                user['last_login'].strftime("%Y-%m-%d"),
                user['date_joined'].strftime("%Y-%m-%d"),
                user['mailing_address'],
            ])
        # Create the table
        table = Table(data)

        # Set the table style
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Set the document elements
        elements = []

        # Add a header
        header_text = "Active Table"
        style = getSampleStyleSheet()['Heading1']
        header = Paragraph(header_text, style)
        elements.append(header)

        # Add the counts
        count_text = "Active: {}\n".format(active_users)
        counts = Paragraph(count_text, style)
        elements.append(counts)

        # Add the table
        elements.append(table)


        doc.build(elements)
        return response
    export_is_Active_pdf.short_description = "Export is_Active objects as PDF"
    
    list_display = (
         'username', 'id', 'email', 'first_name', 'last_name', 'is_staff',
        'is_investor', 'is_student', 'mailing_address', 'date_of_birth', 'gender','user_avatar', 'bio')

    list_filter = ('is_student',
                   'is_investor',
                   'is_staff',
                   'is_superuser',
    
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name',  'last_name', 'email', 'major', 'college', 'date_of_birth', 'gender','user_avatar', 'bio')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_investor', 'mailing_address')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_investor', 'mailing_address')
        })
    )
    

admin.site.register(CustomUser, CustomUserAdmin)
