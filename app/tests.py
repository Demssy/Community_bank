from django.test import TestCase
# # from accounts import models as m1
from accounts.models import CustomUser

class ScholarshipViewTestCase(TestCase):
    def test_scholarship_view(self):
        response = self.client.get('/scholarship/')
        self.assertTemplateUsed(response, 'Scholarship.html')
        self.assertContains(response, 'scholardata')

class AddScholarShipViewTestCase(TestCase):
    def test_add_scholarship_view(self):
        user = CustomUser.objects.create(username='testuser')
        scholarship = scholarship.objects.create(title='Test Scholarship')
        self.client.force_login(user)
        response = self.client.post('/add_scholarship/{}/'.format(scholarship.id))
        self.assertContains(response, 'scholardata')
        self.assertEqual(user.scholarships.count(), 1)



#          {% extends 'global/page.html' %}
#  <!-- {% block content %}
# {%load static%}
# <head>
#   <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
#   <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
#   <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>

#   <style media="screen">
#     a:link {
#       text-decoration: none;
#     }

#     h6 {
#       text-align: center;
#     }

#     .row {
#       margin: 100px;
#     }
#   </style>
# </head>
# <div class="container">
#   <div class="panel panel-primary">
#     <div class="panel-heading">
#       <h6 class="panel-title">Scholarships</h6>
#     </div>
#     <table class="table table-hover" id="dev-table">
#       <thead>
#         <tr>

#           <th>Title</th>
#           <th>content</th>
#           <th>Location</th>
#           <th>requirements</th>
#           <th>Amount</th>
#           <th>Hours</th> 
#           <th>Register</th> 
#         </tr>
#       </thead>

#       {% for d in scholardata %}

#         <td> {{d.title}}</td>
#         <td>{{d.content}}</td>
#         <td>{{d.Location}}</td>
#         <td>{{d.requirements}}</td>
#         <td>{{d.Amount}}</td>
#         <td>{{d.Hours}}</td>
#         <td> 
        
        
#         <a href="{% url 'add_ScholarShip' d.id %}"></a> <button id="myButton" onclick="changeColor(this)">for Register</button></td></li></td>

# <script>
# function changeColor(item) {
#   if (item.style.backgroundColor === "yellow") {
#     item.style.backgroundColor = "";
#     item.innerHTML = "for Register";
#   } else {
#     item.style.backgroundColor = "yellow";
#     item.innerHTML = "Registered";
#     window.location.href = "/add_scholarship/" + item.id;
#   }
# }
# </script>

#       </tr>
#       {% endfor %}
#     </table>
#   </div>
# </div>
# {% endblock content %}
# {%load static%}


# class Register(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField(max_length=500)
#     file = models.FileField(upload_to='uploads/')

# class Registeradmin(forms.ModelForm):
#     class Meta:
#         model = Register
#         fields = ["name", "email" ,"message", "file"]

# def updateVhours(request):
#     if request.method == 'POST':
#         scholarship_id = request.POST['scholarship_select']
#         hours = request.POST['hours']
#         scholarship = Scholarship.objects.get(id=scholarship_id)
#         scholarship.volunteer_hours += hours
#         scholarship.save()
#         return redirect('success')
#     return render(request, 'reports.html')


# def Registeradmin(request):
#     if request.method == 'GET':
#         return render(request, 'reports.html')
#     else:
#         form = Registeradmin(request.POST)
#         message = 'Message was sent successfully'
#         hasError = False
#         if form.is_valid():
#             form = Registeradmin(request.POST)
#             form.save()
