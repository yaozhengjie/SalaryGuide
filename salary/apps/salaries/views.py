from django.http import HttpResponse
from django.template import Context, loader
from apps.salaries.models import *
from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext
#this isn't working
from django.core.context_processors import csrf

import simplejson as json
from django.http import HttpResponse
from haystack.query import SearchQuerySet


import numpy

def landing(request):
	campuses = Campus.objects.all()
	return render_to_response('landing.html', {'campuses':campuses})

def campus(request, campus_id):
	p = get_object_or_404(Campus, pk = campus_id)
	colleges = College.objects.filter(campus = p)
	chancellor = EmployeeDetail.objects.filter(position__title = 'CHANCELLOR')
	return render_to_response('campus.html', {'campus':p, 'colleges':colleges, 'chancellor':chancellor})

def employeeSuper(request, employeeSuper_id):
	p = get_object_or_404(EmployeeSuper, pk = employeeSuper_id)
	primary = p.get_primary_employment()

#	college_employees = Employee.objects.filter(primary.employment
#	college_employee_array = []
#	for e in employees

	return render_to_response('employeeSuper.html', {'employee':p, 'primary':primary})

def college(request, college_id):
	p = get_object_or_404(College, pk = college_id)
	
	employees = p.employeedetail_set.all

	deans = EmployeeDetail.objects.filter(college = p, position__title = 'DEAN')

	
	return render_to_response('college.html', {'employees':employees, 'college':p, 'deans':deans})

def department(request, department_id):
	p = get_object_or_404(Department, pk = department_id)
	employees = p.employeedetail_set.all
	heads = EmployeeDetail.objects.filter(department = p, position__title__contains = 'HEAD')

	return render_to_response('department.html', {'employees':employees, 'department':p, 'heads':heads})

def position(request, position_id):
	p = get_object_or_404(Position, pk = position_id)
	employees = p.employeedetail_set.all

	return render_to_response('position.html', {'employees':employees, 'position':p})

def bubbles(request):
	colleges = College.objects.all()
	return render_to_response('bubbles.html', {'colleges':colleges})


def autocomplete(request):
	sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:6]
	##### Return these fuckers with keys #####
	#suggestions = []


	data = []

	for result in sqs:
		data.append({
			'name': str(result.full_name), 
			'id': result.object.id
			}
			)


	full_response =  json.dumps(data) 

#    	suggestions.append([{'name': str(result.full_name), 'id':result.object.id},])
    
 #   the_data = suggestions
##### Don't know. #####
	#suggestions = [result.full_name for result in sqs]
	#suggestion_ids = [result.object.id for result in sqs]
	#data = json.dumps({
	#	'results': suggestions,
		#'ids':suggestion_ids

	#})
	
	return HttpResponse(full_response, content_type='application/json')
