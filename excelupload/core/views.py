from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone 
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from .models import Sales, Staff
from .forms import SalesForm
import pandas as pd
# Create your views here.

''' staff creation, delete and update CBV  '''

class CreateStaff(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    ''' only managers can create staff
        potential staff must have an account
    '''
    model = Staff
    fields = '__all__'
    success_url = reverse_lazy('core:home')
    template_name = 'core/staff_creation.html'

    def test_func(self):
        
        item = Staff.objects.get(name__username=self.request.user)
        if item.designation == 'manager':
            return True
        return False

class UpdateStaff(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    ''' only managers can create staff
        potential staff must have an account
    '''
    model = Staff
    fields = '__all__'
    success_url = reverse_lazy('core:home')
    template_name = 'core/staff_creation.html'    

    def test_func(self):
        item = Staff.objects.get(name__username=self.request.user)
        if item.designation == 'manager':
            return True
        return False

class DeleteStaff(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy('core:home')
    template_name = 'core/delete.html'

    def test_func(self):
        item = Staff.objects.get(name__username=self.request.user)
        if item.designation == 'manager':
            return True
        return False

''' Functions for handling excel upload '''
## sales upload
def upload_excel(files):
    ''' handles processing of excel files '''
    try:
        df = pd.read_excel(files)
        
        vals = df.to_numpy()
        
        index = 0
        data = {}
        for item in vals:
            
            data[str(index)] = item
            index += 1
        return data
    except:
        ''' Incase of any error. Pandas read_excel() will handle file type checking '''
        return None

# log in required
@login_required 
def upload_sales(request):
    c = request.user
    form = SalesForm()
    if request.method == 'POST':
        form2 = SalesForm(request.POST, request.FILES)

        if form2.is_valid():
            c = upload_excel(request.FILES['excel_file'])
            #print(c)
            if c == None: 
                messages.error(request, 'Error in uploading file, try again')
                return render(request, 'core/upload_sales.html', {'form': form2})
            instance = Staff.objects.get(name__username = request.user)
            to_save = []
            #staff, item_sold, quantity, unit_price
            for key,val in c.items():
                key = Sales(staff=instance,
                            item_sold= val[0],
                            quantity= val[1],
                            unit_price = val[2])
                to_save.append(key)
                #key.save()

            print('List to append \n', to_save)
            with transaction.atomic():
                for item in to_save:
                    item.save()
                       
                

            return HttpResponseRedirect(reverse('core:home'))

        else:
            return render(request, 'core/upload_sales.html', {'form': form2})

    
    return render(request, 'core/upload_sales.html', {'form': form})

''' Functions for viewing excel '''
## view sales
class ViewSales(LoginRequiredMixin,ListView):
    queryset = Sales.objects.all().select_related('staff') # query optimisation
    #paginate_by= 10
    template_name= 'core/viewsales.html'
    context_object_name= 'sales_list'

# show all sales for a given day. date format error
class ArchiveDaySales(LoginRequiredMixin, DayArchiveView):
    queryset = Sales.objects.all()
    date_field= 'date'
    template_name = 'core/viewsales.html'
    context_object_name = 'sales_list'


# shaw today's sales
class TodaySales(LoginRequiredMixin, TodayArchiveView):
    queryset = Sales.objects.all().select_related('staff')
    date_field = 'date'
    template_name = 'core/viewsales.html'
    context_object_name = 'sales_list'
    
