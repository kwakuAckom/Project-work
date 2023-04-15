import json
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import ExpenseForm
from .models import Project, Category, Expense
from django.views.generic import CreateView

# Create your views here.
#OKAY

def project_list(request):
    return render(request, 'budget/project-list.html')


def project_detail(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    category_list = Category.objects.filter(project=project)
    return render(request, 'budget/project-detail.html', {'project':project, 'expense_list': project.expenses.all()})
    

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name','budget')

    def form_valid(self, form):
        #project = Project()
        self.object = form.save(commit=False)
        self.object.save()
        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            Category.objects.create(
                project = Project.objects.get(id=self.object.id),
                name = category
            ).save()
        return HttpResponseRedirect(self.get_success_url())
    def get_success_url(self):
        return reverse('detail', args=[self.object.slug])

    
