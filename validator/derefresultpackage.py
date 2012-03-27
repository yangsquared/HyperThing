'''
Created on 2011-3-8
values of status code: use '-1' to denote the 'unHash'; 
                           '0' denotes empty, 
                           '-3' denotes Doc, which means a html doc returns instead of a RDF
@author: Administrator
'''
class DereferencingResult():
    statusList=[]
    statusURLList=[]
    def __init__(self):
        None

class StatusAndURL():
    def __init__(self, status=200, url=''):
        self.status = status
        self.url=url
    def __repr__(self):
        return '[status:' + str(self.status) + ', url:' + self.url +']'

class Status():
    def __init__(self, requestURI='', statusCode =0, temporaryURI=''):
        self.requestURI=requestURI
        self.statusCode = statusCode
        self.temporaryURI = temporaryURI
    def __repr__(self):
        return '[request URI:' + self.requestURI + ', status code:' + str(self.statusCode) + ', temporary URI:' + self.temporaryURI +']'
    
class ResponseResult():
    def __init__(self, statusCode=0, locationURI=''):
        self.statusCode = statusCode
        self.locationURI = locationURI