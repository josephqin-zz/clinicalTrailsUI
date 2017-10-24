import time

def run():


	#                                                 ^^^^^^
	#    embed that {{ buffer }} somewhere in your template
	#        (unless it's already long enough) to force display

	for x in range (1, 5):
		yield '<p>x = {}</p>'.format (x)

		time.sleep(1)