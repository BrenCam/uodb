# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

def search():
    '''
    Ajax search page
    display a search box and 
    (via callback) return HTML to display results 
    '''
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword',
            _onkeyup="ajax('callback2', ['keyword'], 'target');")),
            target_div=DIV(_id='target'))

def callback2():
    # new callback fn
      # build requisite dictionaries and pass to search

    #print('>>>> Callback2: Sys Path: %s') %sys.path 

    # Search ludict for matches, then return matching entries in the results dict
#    try:    
#        #from models.uodb import get_status_dict
#        from models import uodb
#        #from uodb import get_status_dict
#        #import uodb
#    except ImportError as err:
#        print sys.exc_info()
#        print('>>>> Callback2: Import Error: uodb not found') 

    datadict, ludict = get_status_dict()
    #print datadict
    searchstr = search(request.vars.keyword)
    htmlpage = findmatches(searchstr, datadict, ludict)  
    return htmlpage

def callback():
    '''
    return results of matching dict entries for specified search
    (build list of searchable key values from dictionary?)
    '''
    rdict, ludict =get_status_dict()
    print '>>>Processing Latest Callback Request: <<<'

    # Search ludict for matches, then return matching entries in the results dict

    mydict ={}
    # populate dictionary with test keys
    mydict['joe'] = 1
    mydict['jon'] = 2
    mydict['john'] = 3
    mydict['jona'] = 4
    mydict['jonah'] = 5

    from uodbutils import DictLookupBySubstr

    mydlu = DictLookupBySubstr(ludict)
    #print 'call enter'
    #mydlu = DictLookupBySubstr(mydict)
    #r = mydlu.search('jon')
    #rlist = mydlu.search('S')
    rlist = mydlu.search(request.vars.keyword)
    
    #print 'call return'    
    #rlist =[1,2,3]
    print type(rlist)
    print rlist
    #return LI(*rlist)  
    res  = []
    for item in rlist:
        print 'list item: %s' %item
        #build table with matching results
        crec = rdict[item]
        r = []
        r.append(crec['lname'])
        r.append(crec['mrn'])
        s =",".join(r)
        #res.append(crec['lname'])
        res.append(s) 
    print 'result: %s' %res  
    #return LI(*res)   
    #return TABLE(*[TR(*rows) for rows in res])

    opr  = []   # op row list
    print rlist
    print rdict[19]
    for item in rlist:
        print 'Process Rec ID: %s' %item
        # build a row
        opd = []    # td list  
        rowdict = rdict[item]
        print rowdict.keys()
        # retrieve source data
        for k in rowdict.iterkeys():
            print '>>> process key: %s' %k
            if k == 'lastpsa':
            # assign style 
                tdstr = TD(rowdict['lastpsa'][0:10], _class = (lambda x: 'red' if x==True else 'green') (rowdict['psastale'])).xml()
                #tdstr = XML(TD(rowdict['lastpsa'], _class = 'red'))
                #tdstr = TD(rowdict['lastpsa'][0:10], _class = 'red').xml()
                print tdstr
                opd.append(tdstr)
            elif k == 'lastfu':
            # assign style 
                tdstr = TD(rowdict['lastfu'], _class = (lambda x : 'red' if x==True else 'green') (rowdict['fustale'])).xml()
                #tdstr = XML(TD(rowdict['lastfu'], _class = 'green'))                
                #tdstr = TD(rowdict['lastfu'], _class = 'green').xml()                
                opd.append(tdstr)
            elif k == 'fustale':
                tdstr = TD(rowdict['fustale']).xml()
                opd.append(tdstr)
            elif k == 'psastale':
                tdstr = TD(rowdict['psastale']).xml()
                opd.append(tdstr)
            elif k =='mrn':
                tdstr = TD(rowdict['mrn']).xml()
                print '>>>>> mrn: %s' %tdstr
                opd.append(tdstr)
            elif k =='lname':
                tdstr = TD(rowdict['lname']).xml()
                opd.append(tdstr)
            else:
                continue
                #pass
        # return result
        #print '>>>> processed dict <<<<<'
        print '*** processed dict <<<<< : %s' %opd
        # note: join only works for strings
        for item in opd:  print 'opditem: %s' %item

        try:
            #trdata = TR(''.join(opd).xml())
            trdata = '<TR>' + ''.join(opd) + '</TR>'
        except:
            print sys.exc_info()
        print 'opdstring: %s' %trdata
        #trdata = XML(''.join(opd))
        #print '>>>> processed dict <<<<< : %s' %trdata

        opr.append(trdata)
    # return computed result
    print '*** result count: %s' %len(opr)
    for item in opr:
        print 'Res Row: %s' %item
    #return TABLE(opr)

    #stylestr = STYLE(XML('.green {background-color: green;}, .red {background-color: red;}'))
    #stylestr = STYLE(XML('.red {background-color: red}'))

    stylestr = '<style> \
.green {background-color: #00FFFF; } \
.yellow {background-color: yellow; } \
.red {background-color: red; }  \
</style>'

    #<style>
    #.green {background-color: #00FFFF; }
    #.yellow {background-color: yellow; }
    #.red {background-color: red; }

    #table,th,td
    #{
    #border:1px solid black;
    #}

    #</style>

    print stylestr

    tstr = '<table>' + (''.join(opr)) + '</table>'

    return stylestr + tstr
    #return TABLE(*[TR(*rows) for rows in opr])

    #return TABLE(*[TR(*rows) for rows in res])


    
    #return rdict[1]
#    if rdict.haskey(request.vars.keyword):
#      return UL(rdict[keyword])
#    else:
#      return UL('No matches found') 
#    query = db.page.title.contains(request.vars.keyword)
#    pages = db(query).select(orderby=db.page.title)
#    links = [A(p.title, _href=URL('show',args=p.id)) for p in pages]
#    return UL(*links)

# pt summary status
# retrieve from multiple tables and display as a grid
# ?? support paging here (20 per page) ??

# define current date
import datetime
now = datetime.datetime.now()

def status():
    '''
    get patient summary info (last psa, last fu etc)
    return a dictionary
    '''
    print '>>> process status request <<<'
    rdict, lulist  = get_status_dict() 
    print lulist  
    return dict(dict=rdict)

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

# ??Move this code to the model file - we're really building a model here
#@cache(request.env.path_info, time_expire=None, cache_model=cache.ram)
def zz_get_status_dict():
    '''
    Build cache object for pt summary status
    keep in cache (avoid db refresh)

    ?? Build 2 dicts to support substrign search 
    2nd dict has key = name + list of reletad id's in dict 1
    Apply dictlookup by name to dict 2, then search this 
    when user does a lookup
    Will need a class (DictLookupBySubstr(object): which builds a searchable list of strings
    '''

    #import uodbutils
    from uodbutils import DictLookupBySubstr

    # results dictionary
    rdict = {}
    # lookup/search dictionary
    ludict = {}
        
    # get last psa date
    lastpsa = db.psa.psadate.max()
    rows = db(db.psa).select(db.psa.id_patient, lastpsa, groupby=db.psa.id_patient)
    psadict = {}
    for r in rows:
        tdict = {}
        pid = r.psa.id_patient
        tdict['lastpsa'] = r[lastpsa]
        tdict['id_patient'] = pid
        psadict[pid] = tdict      

    # get last fu date 
    lastfu = db.followup.followup_date.max()
    rows = db(db.followup).select(db.followup.id_patient, lastfu, groupby=db.followup.id_patient)
    #fudict = rows.as_dict(key='followup.id_patient')
    fudict = {}
    #build a list of dictionaries for each id found
    for r in rows:
        tdict = {}
        pid = r.followup.id_patient
        tdict['lastfu'] = r[lastfu]
        tdict['id_patient'] = pid
        fudict[pid] = tdict      

    # result patient data as a list of dictionaries
    plist = db(db.patient).select().as_list()
    
    # Build dictionary from intermetiate dicts
    # ?? How to sort in asc pt order ??
    from datetime import datetime
    for  ddict in plist:        
        sdict={}
        id = sdict['id'] = ddict['id']
        
        # populate pt fields
        sdict['mrn'] = ddict['mrn']
        lname = sdict['lname'] = ddict['lname']
        #id = ddict['id']
        # Set stale default value   
        sdict['fustale'] =  True 
        if fudict.has_key(id):
            tdict = fudict[id]
            sdate = tdict['lastfu'] 
            sdict['lastfu'] = sdate 
            print '****** %s ' %sdate
            fudt = datetime.strptime(sdate, '%Y/%m/%d')
            sdict['fustale'] = (lambda d1,d2,diff: True if (d1-d2).days > diff else False) (now, fudt, 365)
#            if (now - fudt).days <= 365:
#              sdict['fustale'] =  False
        else:
            sdict['lastfu'] = 'None'
         
        # Set stale default value   
        sdict['psastale'] =  True        
        if psadict.has_key(id):
            tdict = psadict[id]
            sdate = tdict['lastpsa'] 
            sdict['lastpsa'] = sdate 
            psadt = datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S')
            # ??lambda fn to set stale value for psa based on date
            sdict['psastale'] = (lambda d1,d2,diff: True if (d1-d2).days > diff else False) (now, psadt, 2500)
            # convert string to date time value
            #if (now - psadt).days <= 2500:
            #  sdict['psastale'] =  False
        else:
            sdict['lastpsa'] = 'None'            
            
        rdict[id] = sdict
        # update search dict
        if ludict.has_key(lname):
            # append pk to list
            ludict[lname].append(id)
        else:
            # add list entry
            ludict[lname] = id

    #print rdict
    # return dicts + lulist
    # Search ludict for matches, then return matching entries in the results dict
    #lulist = DictLookupBySubstr(ludict)

#    for item in lulist:
#        print '>>>>> Lulist: %s' %item

    return rdict, ludict
    

