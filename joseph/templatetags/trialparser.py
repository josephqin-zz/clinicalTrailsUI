from django import template

register = template.Library()
@register.filter(name = 'txt')
def txt(value):
	return value['#text']

@register.filter(name = 'dis_annotation')
def dis_annotation(value):
	if len(value) == 1:
		return value[0]
	else:
		return ",".join(value)

@register.filter(name = 'InclusionCriteria')
def InclusionCriteria(value):
	if value:
		return value['Inclusion Criteria']
	else:
		return ''

@register.filter(name = 'ExclusionCriteria')
def ExclusionCriteria(value):
	if value:
		return value['Exclusion Criteria']
	else:
		return ''

@register.filter(name = 'years')
def years(value):
	if value:
		return int(value/525600)
	else:
		return ''

@register.filter(name = 'ct_num')
def ct_num(value):
	return str(value)[:-4]

@register.filter(name = 'eligibility')
def eligibility(value):
	if value:
		return 'Eligible'
	else:
		return 'Not Eligible'

@register.filter(name = 'profile_sentence')
def profile_sentence(value):
	rs=[]
	for key,val in value.items():
		if val:
			rs.append(val)
	return ' | '.join(rs)
