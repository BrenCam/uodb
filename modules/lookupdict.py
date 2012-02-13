# -*- coding: utf-8 -*-
import os, sys
#sdir = '/home/brencam/web2py/applications/uodb/models'
#if sdir not in sys.path:    
#    sys.path.append(sdir)

#sdir = '/home/brencam/web2py/applications/uodb/modules'
#if sdir not in sys.path:    
#    sys.path.append(sdir)

#        from gluon import *

# Note: restart server if you change these else no effect
try:
    #from gluon import *
    from gluon.html import TD,TR,TABLE, LI
except:
    print sys.exc_info()

    
'''
    Find pt summary data for selected pt;
    Build formatted display of results
    Requires construction of a pair of dicts
    which are used as a partial key search
    Uses web2py helpers extensively to display results

    Dependencies: DictLookupBySubstr; dbload; 
    Need unit tests as ajax request errors fail silently
'''

def findmatches(findstr, rdict, ludict):
    '''
    return results of matching dict entries for specified search
    (build list of searchable key values from dictionary?)
    result is returned as a formatted html page
    '''
    #print '>>> (FindMatches): Find partial matches for: %s <<<' %findstr

    # Search ludict for matches, then return matching entries in the results dict
    try:    
        from uodbutils import DictLookupBySubstr
    except ImportError as err:
        print('>>>> uodbutils not found')

#    try:    
#        #import HTML helpers
#        from gluon import *
#        #from gluon import html

#    except ImportError as err:
#        print('gluon path not found') 
 
    # create dlu object with searchable the list of keys  
    # cache this for future reference ??
    mydlu = DictLookupBySubstr(ludict)
    #rlist = mydlu.search(findstr)
    # Assume Proper Case for name search
    rlist = mydlu.search(findstr.capitalize())

    if len(rlist) == 0:
        return LI('No matching records found')
      
    opr  = []   # op array - row list
    #print '>>> List of matching rec ids: %s\n' %rlist
    for item in rlist:
        #print 'Process Rec ID: %s' %item
        # build a row
        opd = []    # output array - td list
        opdict ={}  
        rowdict = rdict[item]
        #print rowdict.keys()
        # retrieve source data
        for k in rowdict.iterkeys():
            #print '>>>>> Key Order: %s' %k
            if k =='mrn':
                tdstr = TD(rowdict['mrn']).xml()
                opd.append(tdstr)
                opdict['mrn'] = tdstr
            elif k =='lname':
                tdstr = TD(rowdict['lname']).xml()
                opd.append(tdstr)
                opdict['lname'] = tdstr
            elif k == 'lastpsa':
            # assign style dynamically 
                tdstr = TD(rowdict['lastpsa'][0:10], \
                        _class = (lambda x: 'red' if x==True else 'green') (rowdict['psastale'])).xml()
                #print tdstr
                opd.append(tdstr)
                opdict['lastpsa'] = tdstr

            elif k == 'lastfu':
            # assign style 
                tdstr = TD(rowdict['lastfu'], \
                        _class = (lambda x : 'red' if x==True else 'green') (rowdict['fustale'])).xml()
                opd.append(tdstr)
                opdict['lastfu'] = tdstr
            elif k == 'fustale':
                tdstr = TD(rowdict['fustale']).xml()
                opd.append(tdstr)
                opdict['fustale'] = tdstr
            elif k == 'psastale':
                tdstr = TD(rowdict['psastale']).xml()
                opd.append(tdstr)
                opdict['psastale'] = tdstr
            else:
                continue
        # note: join only works for strings
        #for item in opd:  print 'opditem: %s' %item
        try:
            #trdata = TR(''.join(opd).xml())
            #trdata = '<TR>' + ''.join(opd) + '</TR>'
            #build result from a dictionary
            trdata = '<TR>' + \
                     opdict['lname'] + opdict['mrn'] + opdict['lastpsa'] + opdict['lastfu'] + \
                     '</TR>'
        except:
            print sys.exc_info()
        #print '\n opdstring: %s\n' %trdata
        # add current row to array
        opr.append(trdata)
    # return computed result
    #print '*** result count: %s' %len(opr)
    #for item in opr:
        #print 'Res Row: %s' %item
    #return TABLE(opr)

    stylestr = '<style> \
    table,th,td {border:1px solid black;} \
    .green {background-color: #00FFFF; } \
    .yellow {background-color: yellow; } \
    .red {background-color: red; }  \
    </style>'

    # define col headers
    hdlist = ['Last Name', 'MRN','Last PSA', 'Last FU']
    #thdr = ([TH(*h) for h in hdlist]).xml()
    thdr = []    
    for item in hdlist:
        shdr = '<th>' + item + '</th>'
        thdr.append (shdr) 
    strhdr = ''.join(thdr)
    #print '>>> Tbl Header: %s' %thdr
    tstr = '<table>' + strhdr + (''.join(opr)) + '</table>'

    #return TABLE(*[TR(*rows) for rows in opr])
    #return TABLE(*[TR(*rows) for rows in res])
    return stylestr + tstr

def findall(rdict):
    # find all recs and format result
    #print '>>> findall <<<'
    #rdict is a dict of dictionaries (unsorted) - How to sort?
    # convert to a list of dicts
    #print rdict
    dictlist =[]
    [dictlist.append(d) for d in rdict.itervalues()]
    #for d in rdict.itervalues():
    #    dictlist.append(d)
    
    # first compute the sort order (by ascending name)
    import operator
    idlist =[]
    # get sort ids order by name
    try:
        for item in sorted(dictlist, key=operator.itemgetter('lname')):
            idlist.append(item['id'])
    except:
        print 'idlist error'        
            
    #print '>>> lodict: findall: idlist: %s' %idlist
    
    opr  = []   # op array - row list
    # iterate over dict set (already sorted)
    for dictid in idlist:
        rowdict = rdict[dictid]
    #for rowdict in rdict.itervalues():
        #opr  = []   # op array - row list 
        opdict = {}    # output dict - col list
        # retrieve source data - build a dict record
        for k in rowdict.iterkeys():
            #print type(k)
            #print rowdict['lname']
            #print '(lookupdict:findall)>>>>> Key Order: %s' %k
            if k =='mrn':
                tdstr = TD(rowdict['mrn']).xml()
                opdict['mrn'] = tdstr
                #print '>>> tdstr: %s' %tdstr
            elif k =='lname':
                tdstr = TD(rowdict['lname']).xml()
                opdict['lname'] = tdstr
            elif k == 'lastpsa':
                # assign style dynamically 
                tdstr = TD(rowdict['lastpsa'][0:10], \
                        _class = (lambda x: 'red' if x==True else 'green') (rowdict['psastale'])).xml()
                opdict['lastpsa'] = tdstr
            elif k == 'lastfu':
                # assign style 
                tdstr = TD(rowdict['lastfu'], \
                        _class = (lambda x : 'red' if x==True else 'green') (rowdict['fustale'])).xml()
                opdict['lastfu'] = tdstr
            elif k == 'fustale':
                tdstr = TD(rowdict['fustale']).xml()
                opdict['fustale'] = tdstr
            elif k == 'psastale':
                tdstr = TD(rowdict['psastale']).xml()
                opdict['psastale'] = tdstr
            else:
                continue
        #build display result from a dictionary
        #print '>>>> [format row data and add to o/p array'
        #try:    
        #    print opdict
        #except:
        #    print sys.exc_info()
        try:
            trdata = '<TR>' + \
                     opdict['lname'] + opdict['mrn'] + opdict['lastpsa'] + opdict['lastfu'] + \
                     '</TR>'
        except:
            print sys.exc_info()
        #print '\n opdstring: %s\n' %trdata
        # add current row to array
        opr.append(trdata)
 
    stylestr = '<style> \
    table,th,td {border:1px solid black;} \
    .green {background-color: #00FFFF; } \
    .yellow {background-color: yellow; } \
    .red {background-color: red; }  \
    </style>'

    # define col headers
    hdlist = ['Last Name', 'MRN','Last PSA', 'Last FU']
    thdr = []    
    for item in hdlist:
        shdr = '<th>' + item + '</th>'
        thdr.append (shdr) 
    strhdr = ''.join(thdr)
    tstr = '<table>' + strhdr + (''.join(opr)) + '</table>'
    return stylestr + tstr

if __name__ == "__main__":
    
    import datetime

    dtstart = datetime.datetime.now()
    print '\n>>>>Starting at: %s <<<<\n' %dtstart.ctime() 
    #print sys.path

    # Search ludict for matches, then return matching entries in the results dict
    try:    
        #from models.uodb import get_status_dict
        from uodb import get_status_dict
        #import uodb
    except ImportError as err:
        print('>>>> Import Error: uodb not found') 

    try:    
        #import HTML helpers
        from gluon import *
    except ImportError as err:
        print('gluon path not found') 
         
    #print '\n>>>>DB Trace Info: Db uri: %s; DB Name: %s\n' %(db._uri, db._dbname)
    #searchstr = 'Du'
    searchstr = 'Sh'

    # build requisite dictionaries and pass to search
    datadict, ludict = get_status_dict()
    #print datadict
    htmlpage = findmatches(searchstr, datadict, ludict)
    #print '\n ******* HTML Results  Start ****** \n %s' %htmlpage

    #print ' ******* HTML Results  End ****** '

    dtstop = datetime.datetime.now()
    print '\n>>>>Stopping at: %s <<<<\n' %dtstop.ctime()




