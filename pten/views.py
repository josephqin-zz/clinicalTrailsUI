from django.shortcuts import *
from validation.models import Index as ES_Index
from django.contrib.auth.decorators import login_required
from pten.forms import QueryForm,OptionsForm
from pten.ElasticSearch import normal,myargs,dis_hier,dis_hier_aas,normal_t1
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pten.serializer import TaskSerializer

def get_args(parameters):
	args = myargs()
	if parameters['disease']:
		args.disease = parameters['disease']
	if parameters['gene']:
		args.gene = parameters['gene']
	if parameters['age']:
		args.age = int(parameters['age'])
	if parameters['gender']:
		args.gender = parameters['gender']
	if parameters['aas']:
		args.aas = parameters['aas']
	if parameters['stage']:
		args.stage = parameters['stage'][6:] if parameters['stage'].lower().startswith('stage ') else parameters['stage']
	if parameters['grade']:
		args.grade = parameters['grade']
	if parameters['include_keywords']:
		args.include_keywords = parameters['include_keywords']
	if parameters['exclude_keywords']:
		args.exclude_keywords = parameters['exclude_keywords']
	return args


def ElasticSearch(query,option):
	index_file = option['ElasticSearch']
	if option['Ontology'] :
		res,count = dis_hier(query,index_file.index_name)
		hier = 'dis'
		return res,count,hier
	elif option['aas_on'] :
		res,count = dis_hier_aas (query, index_file.index_name)
		hier = 'aas'
		return res, count,hier
	else:
		if index_file.index_name == 'asco2017':
			#print('-------------------')
			res,count = normal_t1(query,index_file.index_name)

		else:
			res, count = normal(query, index_file.index_name)

		hier = ''
		return res, count,hier

def ElasticSearch_api(query,option):
	index_file = option['ElasticSearch']
	if option['Ontology'] :
		res,count = dis_hier(query,index_file)
		hier = 'dis'
		return res,count,hier
	elif option['aas_on'] :
		res,count = dis_hier_aas (query, index_file)
		hier = 'aas'
		return res, count,hier
	else:
		if index_file == 'asco2017':
			#print('-------------------')
			res,count = normal_t1(query,index_file)

		else:
			res, count = normal(query, index_file)

		hier = ''
		return res, count,hier


@api_view(['GET','POST'])
def Query_call(request):
	if request.method == 'GET':
		snippets = {'title':'test','linenos':False}
		serializer = TaskSerializer(snippets)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = TaskSerializer(data=request.data)
		if serializer.is_valid():
			query = get_args(serializer.data)
			ct_list, total_num, hier = ElasticSearch_api(query, serializer.data)
			return Response({'ctlist':ct_list,'total_num':total_num,'result':hier}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @login_required ()
def Query_view(request):
	hier = False
	ct_list = []
	profile = {}
	total_num = 0
	if request.method == 'POST':
		Qform=QueryForm(request.POST)
		Oform=OptionsForm(request.POST)
		if Qform.is_valid() and Oform.is_valid():
			query=get_args(Qform.cleaned_data)
			#print(query)
			profile={key:Qform.cleaned_data[key] for key in Qform.fields}
		#ct_list,total_num = normal(query,index_file.index_name)
			#print(profile)
			ct_list, total_num,hier = ElasticSearch(query,Oform.cleaned_data)


	else:
		Qform = QueryForm()
		Oform = OptionsForm()

	return render(request,'trialmatch.html',{'query_form':Qform,'option_form':Oform,'ctlist':ct_list,'total':total_num,'hier':hier,'profile':profile})

def Query_view_2(request):
	hier = False
	ct_list = []
	profile = {}
	total_num = 0
	if request.method == 'POST':
		Qform=QueryForm(request.POST)
		Oform=OptionsForm(request.POST)
		if Qform.is_valid() and Oform.is_valid():
			query=get_args(Qform.cleaned_data)
			print(query.gender)
			profile={key:Qform.cleaned_data[key] for key in Qform.fields}

		#ct_list,total_num = normal(query,index_file.index_name)
			ct_list, total_num,hier = ElasticSearch(query,Oform.cleaned_data)


	else:
		Qform = QueryForm()
		Oform = OptionsForm()

	return render(request,'trialmatch.html',{'query_form':Qform,'option_form':Oform,'ctlist':ct_list,'total':total_num,'hier':hier,'profile':profile})
