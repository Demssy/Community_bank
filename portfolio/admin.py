from django.contrib import admin
from .models import Project
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from .models import ProjectType
from django.http import FileResponse, HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from django import forms
from django.shortcuts import render
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from collections import Counter
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'title', 'image', 'project_type')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'url', 'project_type', 'image')
        }),
    )
   



class ProjectTypeAdmin(admin.ModelAdmin):
    actions = ['export_project_pdf']
    def export_project_pdf(self, request, queryset):
        # get selected project types
        selected_types = [project_type.name for project_type in queryset]
        if selected_types:
            filtered_projects = Project.objects.filter(project_type__in=selected_types)
            
            fields = request.GET.getlist('fields', ['title', 'description', 'project_type', 'url','username'])
            # Retrieve project data
            projects = filtered_projects
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            content_disposition = request.GET.get('content_disposition', 'attachment')
            response['Content-Disposition'] = f"{content_disposition}; filename=projects.pdf"
            # Create the PDF object
            doc = SimpleDocTemplate(response, pagesize=landscape(letter))
            # Container for the 'Flowable' objects
            elements = []
            # Add project data to the PDF
            styles = getSampleStyleSheet()
            my_style = ParagraphStyle(name="my_style", fontSize=14, leading=16)
            data = [['Title', 'Description', 'Project Type', 'URL','Username']] 
            title = Paragraph("Projects PDF", style=my_style)
            elements.insert(0, title)  
            project_type_count = Counter(project.project_type for project in filtered_projects)
            count_data = [['Project Type', 'Count']]
            for project_type, count in project_type_count.items():
                count_data.append([project_type, count])
            count_table = Table(count_data)
            elements.append(count_table) 
            for project in projects:
                data.append([
                    project.title,
                    project.description,
                    project.project_type,
                    project.url,
                    project.user.username
                ])
            table = Table(data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch,2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            doc.build(elements)
            return response
        else:
            self.message_user(request, "Please select a project type before generating the pdf.")
    export_project_pdf.short_description = "Export projects as pdf by type"



admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(Project, ProjectAdmin)