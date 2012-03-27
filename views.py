from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from validator import HttpTest
from validator.HttpTest import Validator

def homepage(request):
	return render_to_response("homepage.html")
	
def validate(request):
	print request.GET
	url =request.GET['url'].strip()
	validator = Validator(url)
	validator.derefence()
	result =validator.result

	#info = Validator.result['info']
	isException = result['isException']
	info=Validator.result['summary']
	
	
	summaryAStatus = []
	summaryAString = []
	summaryBStatus = []
	summaryBString = []
	summaryCStatus = []
	summaryCString = []
	
	finalStatusAndURL = []
	formulaList = []
	targetURI = []
	returnedDocURI = []
	numberTriple = []
	
	if isException !=1:
		summaryAStatus = Validator.result['summaryAStatus']
		summaryAString = Validator.result['summaryAString']
		summaryBStatus = Validator.result['summaryBStatus']
		summaryBString = Validator.result['summaryBString']
		summaryCStatus = Validator.result['summaryCStatus']
		summaryCString = Validator.result['summaryCString']
	
		finalStatusAndURL = Validator.result['finalStatusAndURL']
		
		formulaList = result["formulaList"]
	
		targetURI=result['requestURI']
		returnedDocURI = result["returnedDocURI"]	
		numberTriple = len(result["relatedTriple"])

	 
	return render_to_response("homepage.html",{	"info":info,
												"isException":isException,
												"summaryAStatus":summaryAStatus,
												"summaryAString":summaryAString,
												"summaryBStatus":summaryBStatus,
												"summaryBString":summaryBString,
												"summaryCStatus":summaryCStatus,
												"summaryCString":summaryCString,
												
												"finalStatusAndURL":finalStatusAndURL,
												"formulaList":formulaList,
												
												"targetURI":targetURI,
												"returnedDocURI":returnedDocURI,
												"numberTriple":numberTriple,
												},context_instance=RequestContext(request))

