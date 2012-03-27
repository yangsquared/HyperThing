'''
Created on 2011-5-23

@author: Administrator
'''

import urllib2
from urllib2 import URLError

import derefresultpackage
import rdflib
from rdflib import Graph
from rdflib import ConjunctiveGraph
'''
   when using urllib2, instead of using httplib.HTTPConnection.debuglevel=0
   directly, you should first define a handler as:
   h = urllib2.HTTPHandler(debuglevel=1)
   then:
   opener = urllib2.build_open(h)
'''
class Validator:
    result = {}
    result["dereference result"] = []
    result["isBad"] = 0
    result["is400"] =0
    result["statusList"] = []
    result["statusCodeList"] = []
    result["statusURLList"] = []
    result['summary']=''
    result['finalStatusAndURL']=[]
    result['summaryAStatus']=0
    result['summaryAString']=''
    result['summaryBStatus']=0
    result['summaryBString']=''
    result['summaryCStatus']=0
    result['summaryCString']=''
    def __init__(self, uri):
        self.result = {}
        Validator.result = {}
        Validator.result["dereference result"] = []
        Validator.result["isBad"] = 0
        Validator.result["is400"] = 0
        self.result["requestURI"] = uri
        self.result["targetURI"] = uri
        self.result["returnedDocURI"] = uri
        Validator.result["statusList"] = []
        self.result["currStatus"] = derefresultpackage.Status(uri, 0, uri)
        Validator.result["statusList"].append(self.result["currStatus"])
        self.result["isValid"] = 1
        self.result["isRightImp"] = 1
        self.result["foundRequest"] = 0
        self.result["isRDF"] = 0
        self.result["isDocURI"] = 0
        self.result["isRightImp"] = 0
        self.result["redirect303Num"] = 0
        self.result["formulaList"] = []
        self.result["isHash"] = 0
        self.result["isSlash"] =0
        self.result["isComplyModel"] = 1
        self.result['relatedTriple'] = []
        self.result['isThing'] = 0
        self.result['info'] =''
        self.result['isException'] = 0
        self.result['exceptionMsg'] = ''
        self.result['exceptionType']=''
        self.result['exitFrom8']=0
        self.result['format']=''
        self.result['returnFormat']='' # application/rdf+xml, application/rdf+n3, text/xml, text/html,
     
        Validator.result["statusCodeList"] = []
        Validator.result["statusURLList"] = []
        Validator.result['finalStatusAndURL']=[]
     
        
    def generateInfo(self):
        
        if self.result['isException']:
            print 'Exception! Type:' + self.result['exceptionType'] + '. ' + self.result['exceptionMsg']
      
        info = " Formula used:"
        for formu in self.result['formulaList']:
            info = info + ' ' + formu 
        info = info + "\n Status List:"
        for status in Validator.result['statusCodeList']:
            info = info + ' ' + str(status)
        info += '\n Status+URL List:'
        for statusAndURL in Validator.result['finalStatusAndURL']:
            info = info + repr(statusAndURL)+ '\n'
        
        info = info + '\n The requested URI '
        if Validator.result['isBad'] and Validator.result['is400']:
            info = info + " returns 400 Error."
        elif Validator.result['isBad']:
            info = info + " returns 4XX/5XX Error."
        else:
            if self.result['isThing']==1:
                info = info +  "identifies a Thing.\n"
            elif self.result['isDocURI']:
                info = info + "identifies a Doc.\n"
            if self.result['isRDF'] ==0 and self.result['returnFormat']!='text/html':
                info = info + " A " + self.result['returnFormat'] + " returns instead of a RDF.\n"
                if self.result['foundRequest']:
                    info =info + " The targetURI:" + self.result["targetURI"] + " is found in the returned file.\n"
                else:
                    info = info + " But the target URI:" + self.result["targetURI"] + " isn't found in the returned file.\n"
            elif self.result['isRDF']==0 and self.result['returnFormat']== 'text/html':
                info = info + " A html returns instead of a RDF.\n"
            elif self.result['isRDF']==1:
                info = info + " Returns a RDF:'" + self.result['returnedDocURI'] + "'.\n"
                if self.result['foundRequest']:
                    info =info + " The targetURI:" + self.result["targetURI"] + " is found in the returned RDF.\n"
                else:
                    info = info + " But the target URI:" + self.result["targetURI"] + " isn't found in the returned RDF.\n"
            if self.result['isRightImp']==1:
                info = info + " Its implementation follows the 303/Hash guidance.\n"
            else:
                info = info + " Its implementation doesn't follow the 303/Hash guidance.\n"
            if self.result['isValid']:
                info = info + " It is valid.\n"
            else:
                info = info+ " It isn't valid.\n"
            
      
      
        self.result['info'] = info
     

    def generateSummary(self):
        
        if self.result['isException']:
            Validator.result['summary']= 'Exception! ' + self.result['exceptionMsg']
        else:
              ##part2:
            '''
        Validator.result['finalStatusAndURL']=[(status, URL)] list of derefresultpackage.StatusAndURL (status, URL)
        values of status:200, 30X, 4XX-5XX, unhash, 0:denotes the initiate status
        URL: 1)redirected url if status is 30X
             2)returned URI if status is 200
             3)unhashed URI if status is unhash
             4)'empty' if status is 4XX-5XX
            '''
            '''
            for statusURL in Validator.result['statusURLList']:
                if statusURL.status ==200:
                    Validator.result['finalStatusAndURL'].append(derefresultpackage.StatusAndURL(200, self.result['returnedDocURI']))
                else:
                    Validator.result['finalStatusAndURL'].append(statusURL)
            
            '''
            
        ##part1
            if Validator.result['isBad']:
                summaryString = Validator.result['BadMessage']
                if Validator.result['is400']:
                    summaryString += '. No anchor is found in the returned file.'
            else:
                summaryString = 'The requested URI ' + self.result['requestURI'] + ' identifies '
                if self.result['isThing']:
                    summaryString = summaryString + 'a Real World Object (a Thing).'
                else :
                    summaryString = summaryString + 'an Information Resource (a Document).'
            
            Validator.result['summary'] = summaryString
            
            if not Validator.result['isBad']:
                if self.result['isRDF']:
                    statusA =0 #right
                    stringA = 'The requested URI is described by document (' \
                                    + self.result['returnFormat'] + ') located under '\
                                                 + self.result["returnedDocURI"]
                else:
                    statusA = 1#warning
                    stringA = 'When request URI with http head "Accept: application/rdf+xml", no RDF has been found. A ' + self.result['returnFormat'] + ' file is found instead.'
        
                Validator.result['summaryAStatus']= statusA
                Validator.result['summaryAString']= stringA
        
                if self.result['redirect303Num']==0 and not self.result['isHash']:
                    statusB = 1 #warning
                    stringB = 'There is no hash tag or 303 redirection has been detected.'
                elif self.result['redirect303Num']!=0:
                    statusB = 0 # right
                    stringB = 'A 303 redirection has been detected.'
                elif self.result['isHash']:
                    statusB = 0 # right
                    stringB = 'A URI hash tag has been detected.'
                Validator.result['summaryBStatus']= statusB
                Validator.result['summaryBString']= stringB
        
                if self.result['foundRequest']:
                    statusC = 0 # right
                    stringC = 'We found ' + str(len (self.result['relatedTriple']))+ \
                           ' RDF triples describing this Real World Object.'
                else:
                    statusC = 1 #warning
                    stringC = 'No relevant triple has been found in returned RDF file which describes the request URI.'
                Validator.result['summaryCStatus']= statusC
                Validator.result['summaryCString']= stringC
        
      
        ##part3
        '''
        if not self.result['isDocURI'] and self.result['isRDF'] and self.result['foundRequest']:
            Validator.result['ThirdPartValue'] = 1
        else:
            Validator.result['ThirdPartValue'] = 0
        ''' 
                                   
    def judgeThing(self):
        if not Validator.result['isBad']:
            if self.result['exitFrom8'] and self.result['isRDF']:
                if self.result['foundRequest']:
                    self.result['isThing']=1
                else:
                    self.result['notFoundRequest']=1
                    self.result ["isValid"] = 0
            else:
                self.result['isDocURI']=1        
    
    def derefence(self):
        if self.result["requestURI"].rfind('#')!=-1:
            self.result["isHash"] = 1
        else:
            self.result["isSlash"] = 1
        try:
            
      
            #h = urllib2.HTTPHandler(debuglevel=1)
            request = urllib2.Request(self.result["requestURI"],headers={"Accept" : "application/rdf+xml"})
            #opener = urllib2.build_opener(h, SmartRedirectHandler(), DefaultErrorHandler())
            opener = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())
            f = opener.open(request)
            Validator.result["statusCodeList"].reverse()
            Validator.result["statusURLList"].reverse()
            Validator.result["dereference result"].reverse()
            initStatusAndURL = derefresultpackage.StatusAndURL(0, self.result['requestURI'])
            Validator.result['finalStatusAndURL'] = [initStatusAndURL]
            if Validator.result["isBad"]!=1:
                if len(Validator.result["statusCodeList"])!=0:
                    Validator.result["statusCodeList"].append(200)
                else:
                    Validator.result["statusCodeList"] = [200]
                if len(Validator.result["statusURLList"])!=0:
                    Validator.result["statusURLList"].append(derefresultpackage.StatusAndURL())
                else:
                    Validator.result["statusURLList"] = [derefresultpackage.StatusAndURL()]
           
                f.headers.dict["status code"] = str(200)
                if len (Validator.result["dereference result"])!=0:
                    Validator.result["dereference result"].append(f.headers.dict)
                else:
                    Validator.result["dereference result"]=[f.headers.dict]
                if f.info().getheader('Content-Type').startswith('application/rdf+xml'):
                    self.result["isRDF"] = 1
                    self.result['format']= 'xml'
                    self.result['returnFormat'] = 'application/rdf+xml'
                elif f.info().getheader('Content-Type').startswith('application/rdf+n3'):
                    self.result["isRDF"] = 1
                    self.result['format']= 'n3'
                    self.result['returnFormat'] = 'application/rdf+n3'
                elif f.info().getheader('Content-Type').startswith('text/xml'):
                    self.result["isRDF"] = 0
                    self.result['format']= 'xml'
                    self.result['returnFormat'] = 'text/xml'
                elif f.info().getheader('Content-Type').startswith('text/plain'):
                    self.result["isRDF"] = 0
                    self.result['format']= 'xml'
                    self.result['returnFormat'] = 'text/plain'
                else:
                    self.result["isRDF"] = 0
                    self.result['returnFormat'] = 'text/html'
            self.check()
      #      self.generateInfo()
         #   self.generateSummary()
           
       # except URLError, e:
        except ValueError, e:
            self.result['isException'] = 1
            self.result['exceptionType']= 'unknown url type'
        except URLError, e:
            self.result['isException'] = 1
            self.result['exceptionType']= 'URL open exception'
          #  self.result['exceptionMsg']=repr(e)
            if hasattr(e, 'reason'):
             #   print 'We failed to reach a server.'
             #   print 'Reason: ', e.reason
                self.result['exceptionMsg']= 'We failed to reach a server.' + ' Reason:' + repr(e.reason)
            elif hasattr(e, 'code'):
              #  print 'The server couldn\'t fulfill the request.'
              #  print 'Error code: ', e.code
                self.result['exceptionMsg']= 'The server couldn\'t fulfill the request.' + ' Error code:' + str(e.code)
        except Exception, e:
            self.result['isException'] = 1
            self.result['exceptionType']= 'Uncertain exception'
        '''
        except Exception, e:
            self.result['isException'] = 1
            self.result['exceptionType']= 'URL open exception'
            self.result['exceptionMsg']=repr(e)
            print e
        '''
        self.judgeThing()
        self.generateSummary()
     #   self.generateInfo()
        
        self.__displayResult2()
        
    
    def check(self):
       
        isFirstFormula6 = 0
        if self.result["isHash"]:
            
            #apply formula 6
            defragURI = self.result["requestURI"].split('#')[0]
            currResponse = derefresultpackage.StatusAndURL(-1, defragURI)
            self.result["currStatus"] = self.__applyFormula6(self.result["currStatus"], currResponse)
            Validator.result["statusList"].append(self.result["currStatus"])
            tempResponse = derefresultpackage.StatusAndURL('unHash', defragURI)
            Validator.result['finalStatusAndURL'].append(tempResponse)
            isFirstFormula6 = 1
            
        
        
        for statusURL in Validator.result["statusURLList"]:
            
            
            if  not isFirstFormula6 and self.result['currStatus'].requestURI.rfind('#')!=-1:
                #apply formula 6
                defragURI = self.result['currStatus'].requestURI.split('#')[0]
                currResponse = derefresultpackage.StatusAndURL(-1, defragURI)
                self.result["currStatus"] = self.__applyFormula6(self.result["currStatus"], currResponse)
                Validator.result["statusList"].append(self.result["currStatus"])
                tempResponse = derefresultpackage.StatusAndURL('unHash', defragURI)
                Validator.result['finalStatusAndURL'].append(tempResponse)
            if statusURL.status>= 400 and statusURL.status<600:
                self.result["currStatus"] = self.__applyFormula5(self.result["currStatus"], statusURL)
                Validator.result["statusList"].append(self.result["currStatus"])
                break
            elif self.result["currStatus"].statusCode ==0: # 0 means empty
                code = statusURL.status
                if code == 200:
                    self.result["currStatus"] = self.__applyFormula2(self.result["currStatus"], statusURL)
                    Validator.result["statusList"].append(self.result["currStatus"])
                elif code == 301:
                    self.result["currStatus"] = self.__applyFormula3(self.result["currStatus"], statusURL)
                    Validator.result["statusList"].append(self.result["currStatus"])
                elif code ==302 or code == 307:
                    self.result["currStatus"] = self.__applyFormula3(self.result["currStatus"], statusURL)
                    Validator.result["statusList"].append(self.result["currStatus"])
                elif code == 303:
                    self.result["currStatus"] = self.__applyFormula4(self.result["currStatus"], statusURL)
                    Validator.result["statusList"].append(self.result["currStatus"])
            elif self.result["currStatus"].statusCode == 303 or self.result["currStatus"].statusCode == -1:
                    # -1 means 'unhash'
                code = statusURL.status
                if code == 200:
                    self.result["currStatus"] = self.__applyFormula7(self.result["currStatus"], statusURL)
                    Validator.result["statusList"].append(self.result["currStatus"])
                elif code == 301 or code == 302 or code == 303 or code == 307:
                    self.result["currStatus"] = self.__applyFormula8(self.result["currStatus"], statusURL)
                    Validator.result["statusList"].append(self.result["currStatus"])
            else:
                # doesn't comply the model
                self.result["isValid"] = 0
                self.result["isComplyModel"] = 0
                break;
            isFirstFormula6=0
            if statusURL.status ==200:
                Validator.result['finalStatusAndURL'].append(derefresultpackage.StatusAndURL(200, self.result['returnedDocURI']))
            else:
                Validator.result['finalStatusAndURL'].append(statusURL)
            
        self.result["isRightImp"] = self.__checkImpl()
        '''
        If self.isValid, then Check whether the target URI could be found in the
        returned rdf doc.
        '''
        if not Validator.result["isBad"] and self.result['returnFormat']!='text/html':
   #     if self.result["isValid"] and self.result["isRDF"] and not self.result["isDocURI"]:
            if self.__isIncluded(self.result["targetURI"], self.result["returnedDocURI"]):
                self.result["foundRequest"] = 1
            else:
                self.result ["foundRequest"] = 0
                self.result ["isValid"] = 0
        return self.result["isValid"]
   
    def __isIncluded(self, targetURI, returnedDocURI):
        try:
            g = ConjunctiveGraph()
            g.parse(returnedDocURI, format=self.result['format'])
            subList = list(g.triples((rdflib.URIRef(targetURI), None, None)))
            preList = list(g.triples((None, rdflib.URIRef(targetURI), None)))
            objList = list(g.triples((None, None , rdflib.URIRef(targetURI)))) 
            if len(subList)==0 and len(preList)==0 and len(objList)==0:
                return 0
            else:
                subList.extend(preList)
                subList.extend(objList)
                self.result['relatedTriple']= subList
                return 1
        except Exception, e:
            print e
            self.result['isException'] = 1
            self.result['exceptionType']= 'RDF Graph Load Exception'
            self.result['exceptionMsg']=repr(e)
            return 0
    def __checkImpl(self):
        if self.result["isHash"] and self.result["redirect303Num"]>0:
            return 0
        elif self.result["isSlash"] and self.result["redirect303Num"]!=1:
            return 0
        else:
            return 1    
    
    def __applyFormula2(self, currStatus, currResponse):
        requestURI = currStatus.requestURI
        status = currResponse.status
        returnedURI = currStatus.temporaryURI
        newStatus = derefresultpackage.Status(requestURI, status, returnedURI)
        self.result["formulaList"].append("formula(2)")
        self.result["returnedDocURI"] = returnedURI
        #self.result["isDocURI"] = 1
        return newStatus
    
    def __applyFormula3(self, currStatus, currResponse):
        targetURI = currResponse.url
        newStatus = derefresultpackage.Status(targetURI, 0, targetURI)
        self.result["formulaList"].append("formula(3)")
        self.result["targetURI"] = targetURI
        self.result["returnedDocURI"] = targetURI
        return newStatus
    '''
    def __applyFormula4(self, currStatus, currResponse):
        
        requestURI = currStatus.requestURI
        returnURI = currResponse.url
        newStatus = derefresultpackage.Status(requestURI, 0, returnURI)
        self.result["formulaList"].append("formula(4)")
        self.result["targetURI"] = requestURI
        self.result["returnedDocURI"] = returnURI
        return newStatus
        
        
        targetURI = currResponse.url
        newStatus = derefresultpackage.Status(targetURI, 0, targetURI)
        self.result["formulaList"].append("formula(4)")
        self.result["targetURI"] = targetURI
        self.result["returnedDocURI"] = targetURI
        return newStatus
    '''
    def __applyFormula4(self, currStatus, currResponse):
        targetURI = currStatus.requestURI
        returnedURI = currResponse.url
        status = currResponse.status
        newStatus = derefresultpackage.Status(targetURI, status, returnedURI)
        self.result["targetURI"] = targetURI
        self.result["returnedDocURI"] = returnedURI
        self.result["formulaList"].append("formula(4)")
        self.result["redirect303Num"]+=1
        return newStatus
        
    def __applyFormula5(self, currStatus, currResponse):
        targetURI = currStatus.requestURI
        newStatus = derefresultpackage.Status(targetURI, -2, "empty")
        self.result["targetURI"]= targetURI
        self.result["returnedDocURI"] = "empty"
        self.result["formulaList"].append("formula(5)")
        Validator.result["isBad"] = 1
        '''
        self.result["isValid"] = 0
        self.result['isRDF'] = 0
        self.result['isThing'] = 0
        '''
        return newStatus
     
    def __applyFormula6(self, currStatus, currResponse):
        requestURI = currStatus.requestURI
        newStatus = derefresultpackage.Status(requestURI, -1, currResponse.url);
        self.result["formulaList"].append("formula(6) ")
        self.result["returnedDocURI"] = currResponse.url
        return newStatus
    
    def __applyFormula7(self, currStatus, currResponse):
        targetURI = currStatus.requestURI
        status = currStatus.statusCode
        returnURI = currStatus.temporaryURI
        newStatus = derefresultpackage.Status(targetURI, status, returnURI)
        self.result["targetURI"] = targetURI
        self.result["returnedDocURI"] = returnURI
        self.result["formulaList"].append("formula(7)")
        '''
        if self.result['isHash'] and not self.result['isRDF']:
            self.result['isDocURI']=1
        '''
        '''
        self.result['isDocURI']=0
        if self.result['isRDF']:
            self.result['isThing']=1
        '''
        self.result['exitFrom8']=1
        return newStatus
    
    def __applyFormula8(self, currStatus, currResponse):
        targetURI = currStatus.requestURI
        status = currStatus.statusCode
        returnURI = currResponse.url
        newStatus = derefresultpackage.Status(targetURI, status, returnURI)
        self.result["targetURI"] = targetURI
        self.result["returnedDocURI"] = returnURI
        self.result["formulaList"].append("formula(8)")
        if currResponse.status ==303:
            self.result["redirect303Num"] += 1
        return newStatus
    
    def __displayResult2(self):
        spacing = 15
        print "\n".join(["%s=%s" % (k.ljust(spacing), repr(v)) for k, v in self.result.items()]) 
        print "Global variable values"
        print "\n".join(["%s=%s" % (k.ljust(spacing), repr(v)) for k, v in Validator.result.items()])
        print self.result['info']+'\n\n'
    def __displayResult(self):
        print ""
        print "Result of dereferencing uri:" + self.result["requestURI"] + " is as follows:"
        if self.result["isHash"]:
            print "    It is a Hash uri."
        else:
            print "    It is a Slash uri."
            
        print "    status code list is:"
        for statusCode in Validator.result["statusCodeList"]:
            print "     " + repr(statusCode)
        print "    formula list is:"
        for s in self.result["formulaList"]:
            print "     " + s
        print "    status+URL list is:   "
        for statusURL in Validator.result["statusURLList"]:
            print "      " + repr(statusURL)
        print "    status list is:    "
        for status in Validator.result["statusList"]:
            print "      " + repr(status)
           
        if self.result["isValid"]:
            
            print "    dereferencing is valid."
            
            if self.result["isDocURI"]:
                print "    It is a document URI."
            else:
                print "    It is a resource URI."
            
            print "    The returned doc is:  " + self.result["returnedDocURI"]
            if self.result["isRDF"]:
                print "    The returned doc is a rdf document."
            else:
                print "    The returned doc is a html document."
            print "    The target uri is:    " + self.result["targetURI"]
            if not self.result["isRightImp"]:
                print "The implementation of this uri doesn't comply with the guidance"
            else:
                print "The implementation of this uri complies with the guidance"
        else:
            print "    dereferencing is not valid."
            if self.result["isBad"]:
                print ("    4XX/5XX returned.")

class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self,req, fp, code, msg, headers):
        result = urllib2.HTTPError(
                                   req.get_full_url, code, msg, headers, fp)
        result.status = code
        headers.dict["status code"] = str(code)
        Validator.result["dereference result"].append(headers.dict)
        if code>=400 and code<600:
            if len(Validator.result["statusCodeList"])!=0:
                Validator.result["statusCodeList"].append(code)
            else:
                Validator.result["statusCodeList"] = [code]
            a = derefresultpackage.StatusAndURL(code, "empty")
            if len(Validator.result["statusURLList"])!=0:
                Validator.result["statusURLList"].append(a)
            else:
                Validator.result["statusURLList"] = [a]
            Validator.result["isBad"] = 1
            Validator.result['BadMessage'] = str(code)+ ':' + msg
            if code == 400:
                Validator.result["is400"] =1
        return result

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(
                self, req, fp, code, msg, headers)
        headers.dict["status code"] = str(code)
        Validator.result["dereference result"].append(headers.dict)
        a = derefresultpackage.StatusAndURL(code, headers.dict['location'])
        if len(Validator.result["statusURLList"])!=0:
            Validator.result["statusURLList"].append(a)
        else:
            Validator.result["statusURLList"] = [a]
        if len(Validator.result["statusCodeList"])!=0:
            Validator.result["statusCodeList"].append(code)
        else:
            Validator.result["statusCodeList"] = [code]
        result.status = code
        return result
    def http_error_303(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_303(
                self, req, fp, code, msg, headers)
        
        headers.dict["status code"] = str(code)
        Validator.result["dereference result"].append(headers.dict)
        a = derefresultpackage.StatusAndURL(code, headers.dict['location'])
        if len(Validator.result["statusURLList"])!=0:
            Validator.result["statusURLList"].append(a)
        else:
            Validator.result["statusURLList"] = [a]
        if len(Validator.result["statusCodeList"])!=0:
            Validator.result["statusCodeList"].append(code)
        else:
            Validator.result["statusCodeList"] = [code]
        result.status = code
        return result
    
    
    def http_error_307(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_307(
                self, req, fp, code, msg, headers)
        headers.dict["status code"] = str(code)
        Validator.result["dereference result"].append(headers.dict)
        a = derefresultpackage.StatusAndURL(code, headers.dict['location'])
        if len(Validator.result["statusURLList"])!=0:
            Validator.result["statusURLList"].append(a)
        else:
            Validator.result["statusURLList"] = [a]
        if len(Validator.result["statusCodeList"])!=0:
            Validator.result["statusCodeList"].append(code)
        else:
            Validator.result["statusCodeList"] = [code]
        result.status = code
        return result
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        headers.dict["status code"] = str(code)
        Validator.result["dereference result"].append(headers.dict)
        a = derefresultpackage.StatusAndURL(code, headers.dict['location'])
        if len(Validator.result["statusURLList"])!=0:
            Validator.result["statusURLList"].append(a)
        else:
            Validator.result["statusURLList"] = [a]
        if len(Validator.result["statusCodeList"])!=0:
            Validator.result["statusCodeList"].append(code)
        else:
            Validator.result["statusCodeList"] = [code]
        result.status = code
        return result


# some test cases
uri = 'http://purl.org/dc/elements/1.1/publisher' # doc uri
uri = 'http://dublincore.org/usage/terms/history/#type-006' # get a html file
uri = 'http://www.w3.org/2004/02/skos/core#note' #303, 301, 200
uri = 'http://xmlns.com/foaf/0.1/geekcode'  #303, 200 valid implementation
uri = 'http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a' #302, 200 wrong implementation
uri = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#_4'
uri = 'http://purl.org/goodrelations/v1#PartsAndLabor-BringIn'
uri = 'http://dublincore.org/usage/terms/history/#type-006'
uri = 'http://dublincore.org/usage/terms/history/#hasVersion-003'
uri = 'http://purl.org/dc/elements/1.1/' # 302, 200 doc uri
uri = 'http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a' #302, 200 wrong implementation
uri ='http://www.w3.org/2000/01/rdf-schema#seeAlso' #200
uri = 'http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#ClassA'  #302, 303, 200 wrong implementation
uri = 'http://dublincore.org/usage/terms/history/#type-006' # get a html file
uri = 'http://xmlns.com/foaf/0.1/family_name' #303, 200 valid, rdf
uri = 'http://purl.org/NET/c4dm/event.owl'  # 302, 303, 200 , get a html file.can not find the uri in the returned doc
uri = 'http://xmlns.com/foaf/0.1/Agent' # 200 doc uri
uri = 'http://purl.org/ontology/bibo/status/draft'  #302, 400
uri = 'http://purl.org/NET/c4dm/event.owl'
uri = 'http://www.geonames.org/ontology' #301, 303, 200
uriList = [ #Recipe 1
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1#ClassA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1#ClassB",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1#propA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1#propB",
                
             #Recipe 2
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example2/",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example2/ClassA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example2/ClassB",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example2/propA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example2/propB",
                
              #Recipe 1a
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a#ClassA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a#ClassB",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a#propA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a#propB",
                
               #Recipe 2a
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example2a/",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example2a/ClassA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example2a/ClassB",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example2a/propA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example2a/propB",
                
               #Recipe 3
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example3",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example3#ClassA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example3#ClassB",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example3#propA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example3#propB",
                
                #Recipe 4
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example4/",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example4/ClassA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example4/ClassB",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example4/propA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example4/propB",
                
               #Recipe 3a
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#ClassA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#ClassB",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#propA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#propB",
                
                #Recipe 4a
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example4a/",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example4a/ClassA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example4a/ClassB",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example4a/propA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example4a/propB",
                
                #Recipe 5
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example5/",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example5/ClassA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example5/ClassB",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example5/propA",
                "http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example5/propB",
                
                #Recipe 5a
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example5a/",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example5a/ClassA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example5a/ClassB",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example5a/propA",
                "http://purl.oclc.org/NET/SWD/recipes/examples-A/example5a/propB",]

uriList = [
           'http://sadkfjasjfkas;lfjkasfjdkjl;fdklj;as.com', #exception
           'http://www.bbc.co.uk#hashtag', #exception
           'http://bbc.co.uk', #301, 200 doc uri
           'http://dbpedia.org/resource/Paris',#303, 200, thing uri
           'http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1#propB', # unhash, 200, thing uri
           'http://purl.org/dc/elements/1.1/publisher', # 302,200, doc uri, rdf found
      
           ]
'''
  'http://purl.org/ontology/bibo/status/draft',
 'http://www.geonames.org/ontology',
           'http://dublincore.org/usage/terms/history/#type-006' ,
           'http://xmlns.com/foaf/0.1/Agent',
           'http://purl.org/NET/c4dm/event.owl',
           'http://xmlns.com/foaf/0.1/family_name',
           'http://www.w3.org/2000/01/rdf-schema#seeAlso',
           'http://purl.oclc.org/NET/SWD/recipes/examples-A/example1a',
           'http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#ClassA',
          
'''
'''
for uri in uriList:
    validator = Validator(uri)
    validator.derefence()
   # validator.check()

'''

uri = 'http://sadkfjasjfkas;lfjkasfjdkjl;fdklj;as.com'
uri = 'http://bbc.co.uk' #301, 200 doc uri


uri = 'http://www.bbc.co.uk#hashtag'

uri ='http://www.w3.org/2000/01/rdf-schema#seeAlso' #200

uri = 'http://dublincore.org/usage/terms/history/#type-006' #html


uri= 'http://purl.org/ontology/bibo/status' #302 400

uri = 'http://umbel.org/umbel#' # n3
uri = 'http://purl.org/goodrelations/v1#' #xml
uri = 'http://www.aktors.org/ontology/portal#' # 'text/plain'
uri = 'http://d3e.open.ac.uk/akt/2002/ref-onto.html'
uri = 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger' # 406
uri = 'http://www.geonames.org/ontology' #301, 303, 200 not found requested uri

uri = 'http://purl.org/ontology/bibo/status/draft'  #302, 400
uri = 'http://dbpedia.org/resource/Paris'#303, 200, thing uri


uri = 'http://purl.oclc.org/NET/SWD/recipes/examples-A/example3a#ClassA'
uri = 'http://www.w3.org/2006/07/SWD/recipes/examples-20080421/example1#propB' # unhash, 200, thing uri
uri = 'http://purl.org/dc/elements/1.1/publisher' # 302,200, doc uri, rdf found
uri = 'www.dbpedia.com'
validator = Validator(uri)
validator.derefence()
