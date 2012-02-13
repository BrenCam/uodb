# -*- coding: utf-8 -*-

# for ide web2py support
# see: http://kollerie.wordpress.com/2009/04/07/setting-up-your-ide-for-web2py-development/
if 0:
    from gluon.globals import *    
    from gluon.html import *
    from gluon.http import *
    from gluon.tools import *
    from gluon.sql import *
    from gluon.validators import *
    from gluon.languages import translator as T 
    from gluon.sqlhtml import SQLFORM, SQLTABLE, form_factory
    
    session = Session()
    request = Request()
    response = Response()
    crud = Crud()
#    db = DAL(‘sqlite://storage.sqlite’)
#    auth=Auth(globals(),None)    
    
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()
    
    
def custom_form():
    '''
    patient registration form creation - ??use custom sql form??
    '''
    print '>>> process ptreg form <<<'
    #form = SQLFORM(db.patient)
    
    labels ={'lname':'Last Name', 'mrn': 'MRN'}
    
    form = SQLFORM(db.patient,
                   0,
                   fields=['mrn','lname', 'ethnicity', 'date_of_birth'],
                   labels = labels,
                   #formstyle="divs",
                   showid=False,
                   #hideerror=True,
                   submit_button='Add New')    
    
    #if form.process(session=None, formname='patient_reg').accepted:
    if form.process(session=None, formname=None, hideerror=True).accepted:
        response.flash = 'form accepted'
        # redirect after entry
        redirect(URL('status'))
    elif form.errors:
        response.flash = ' form has errors'
    else:
        response.flash = 'please enter form data'
    
    return dict(form = form)
    # use manual form - don't pass form to view form
    #return dict()    
    

def search():
    '''
    Ajax search page
    display a search box and 
    (via callback) return HTML to display results
    <input class='search_box' id='search' name='query' placeholder='Search' type='text'>
    <input class='search_submit' type='submit' value=''>
    '''
    return dict(form=FORM(INPUT(_id='keyword',_name='keyword', 
            _placeholder='Enter search string or enter \'*\' to show all recs',
            _onkeyup="ajax('callback', ['keyword'], 'target');")),
            target_div=DIV(_id='target'))

def callback():
    # new callback fn
      # build requisite dictionaries and pass to search

    #print('>>>> Callback2: Sys Path: %s') %sys.path 

    # AJAX BUG - Shift key triggers a request
    # Allow user to specify '*' to  see all recs

    try:
        if not request.vars.keyword:
            #print '****** No Search Key - bail out ****'
            return LI('No Search Specified')
        searchstr = request.vars.keyword
        #print('>>>> Callback - Search for: %s <<<<') %searchstr
        datadict, ludict = get_status_dict()
        #print datadict
        from lookupdict import findmatches, findall
        if searchstr == '*':
            allpage = findall(datadict)
            return allpage
        #htmlpage = lookupdict.findmatches(searchstr, datadict, ludict)  
        htmlpage = findmatches(searchstr, datadict, ludict)  
        #return htmlpage

    except :
        print sys.exc_info()
        return 'No data found'

    return htmlpage

def list_status():
    # display data from v_summary view
    # list recs
    #table = 'v_summary'
    #table = db.v_summary
    #query = request.vars.query
    
    table, dummy = validate('v_summary')
    
    import math

    if request.vars.page:
        current_page = int(request.vars.page)
    else:
        current_page = 1
    
    # default query
    query = table.id > 0

    #recs = db().select(db.v_summary.ALL)
    cols =['lname', 'mrn', 'lastpsa', 'lastfu']
    #cols =['lname', 'mrn', 'lastpsa', 'lastfu', 'pstale', 'fstale']
         
        # Handle User specified search
    if request.vars.query:
        print '>>>> Status Query: %s' %request.vars.query
        query_str = request.vars.query
        query = table.id == 0
        for field in cols:
            # search all text fields for specified string
            if table[field].type in ('string', 'text'):
                query = query | table[field].contains(query_str)
    
    
    #return dict(recs= recs)
    # Sorting
    #orderby = table['id']
    #orderby = table['name']
    #if request.vars.sort:
    #    sort_by = request.vars.sort
    #    sort_by in table.fields or die()
    #
    #    # GAE does not allow sorting by text fields
    #    if request.env.web2py_runtime_gae and table[sort_by].type is 'text':
    #        response.flash = "GAE does not allow sorting by text fields"
    #        request.vars.sort = 'id'
    #    else:
    #        orderby = table[sort_by]
    #if request.vars.sort_reverse == 'true':
    #    orderby = ~orderby

    number_of_items = db(query).count()
    #items_per_page = plugins.instant_admin.items_per_page
    items_per_page = 10
    number_of_pages = int(math.ceil(number_of_items / float(items_per_page)))
    pages = get_pages_list(current_page, number_of_pages)
    limitby=((current_page-1)*items_per_page,current_page*items_per_page)
    
    # just show a few fields     
    fields = [field for field in cols if table[field].readable and table[field].type is not 'blob']
    # list of table fields (include  virtual ??)
    print '>>> table field list:'
    for field in table.fields:
        print field,  type(field)
    
    #pdiff = 2500
    #fdiff = 365
    #db.v_summary.pstale =Field.Virtual(lambda row, diff=pdiff:
    #        True if (now - row.v_summary.lastpsa).days > diff else False)
    #db.v_summary.fstale =Field.Virtual(lambda row, diff = fdiff:
    #        True if (row.v_summary.lastfu is None or (now - row.v_summary.lastfu).days > fdiff) else False)
    #
    
    print '>>>> list_status: virtual fields'
    # build dicts of stale data
    psadict ={}
    fudict ={}
    
    #fields.append('psastale')
    #fields.append('fustale')
    
    
    for item in db(db.v_summary).select():
        #print item
        #print 'Mrn: %s; Lname: %s; PSAStale: %s; FUStale: %s' %(item.mrn, item.lname, item.pstale, item.fstale)
        #print item.mrn, item.lname
        psadict[item.id] = item.pstale
        fudict[item.id] = item.fstale

    #data = db(query).select(db.table.mrn, db.table.name, limitby=limitby, orderby=orderby)
    #data = db(query).select(limitby=limitby)
    #print '>>> list_status -  data : %s' %data
    
    recs = db(query).select(db.v_summary.ALL, limitby=limitby)
    # display data contents
    print '>>> list_status - recs: %s' %recs

    # extract desired cols only and identify stale recs
    # sdict['fustale'] = (lambda d1,d2,diff: True if (d1-d2).days > diff else False) (now, fudt, 365)
     # 
    #for row in data:
    #return dict(recs=  data)
    #print '>>> PSA Dict'
    #print psadict
        
    return dict(table=table,
                fields= fields,
                current_page=current_page,
                pages=pages,
                number_of_items=number_of_items,
                number_of_pages=number_of_pages,
                psadict = psadict,
                fudict = fudict,
                data=recs)      

def status():
    '''
    get patient summary info (last psa, last fu etc)
    return a dictionary
    '''
    #print '>>> process status request <<<'
    rdict, lulist  = get_status_dict() 
    #print lulist  
    return dict(dict=rdict)
    
#@auth.requires_login()    
def patient_form():
    
    #form = SQLFORM(db.patient)
    
    rec = db.patient(request.args(0)) or redirect(URL('index'))
    # specify custom labels
    labels ={'lname':'Last Name', 'mrn': 'MRN'}
    form = SQLFORM(db.patient, rec,
                   fields=['mrn','lname', 'ethnicity'],
                   labels = labels,
                   showid=False)
    #form = SQLFORM(db.patient, fields=['mrn','lname', 'ethnicity'])
    #if form.process(session=None, formname='patient_reg').accepted:
    if form.process().accepted:
        response.flash = 'form accepted'
        # redirect after entry
        redirect(URL('status'))
    elif form.errors:
        response.flash = ' form has errors'
    else:
        response.flash = 'please enter form data'
    
    return dict(form = form)
    
#@auth.requires_login()    
def zznew():
    '''
    patient registration form creation - ??use custom sql form??
    '''
    print '>>> process ptreg form <<<'
    #form = SQLFORM(db.patient)
    
    labels ={'lname':'Last Name', 'mrn': 'MRN'}
    
    form = SQLFORM(db.patient,
                   0,
                   fields=['mrn','lname', 'ethnicity', 'date_of_birth'],
                   labels = labels,
                   #formstyle="divs",
                   showid=False,    
                   submit_button='Add New')    
    
    #if form.process(session=None, formname='patient_reg').accepted:
    if form.process(session=None, formname=None).accepted:
        response.flash = 'form accepted'
        # redirect after entry
        redirect(URL('status'))
    elif form.errors:
        response.flash = ' form has errors'
    else:
        response.flash = 'please enter form data'
    
    return dict(form = form)
    # use manual form - don't pass form to view form
    #return dict()
    
    
def new():
    #table, dummy = validate(request.args(0))
    
    table = db.patient

    labels ={'lname':'Last Name', 'mrn': 'MRN'}
    #form = SQLFORM(table, formstyle="divs", showid=False, submit_button='Add')

    
    form = SQLFORM(table,
                   fields=['mrn','lname', 'ethnicity', 'date_of_birth'],
                   labels = labels,
                   #formstyle="divs",
                   showid=False,    
                   submit_button='Add New')
    
    if form.accepts(request.vars, session):
        session.flash = '%s %s successfully created.' % (singular(table), form.vars.id)
        redirect(URL('status', args=table))
    elif form.errors:
        response.flash = 'Error. Please correct the issues marked in red below.'

    return dict(table=table,
                form=form)
        
def edit():
    
    table, row = validate(request.args(0), request.args(1))
    
    #row = db.patient(request.args(0)) or redirect(URL('index'))
        # specify custom labels
    labels ={'lname':'Last Name', 'mrn': 'MRN'}
    
    form = SQLFORM(db.patient,
                   record = row,
                   fields=['mrn','lname', 'ethnicity', 'date_of_birth'],
                   labels = labels,
                   #formstyle="divs",
                   showid=False,    
                   submit_button='Save')
    

    if form.accepts(request.vars, session):
        session.flash = '%s %s successfully updated.' % (singular(table), row['id'])
        redirect(URL('list_patient', args=table))
    elif form.errors:
        response.flash = 'Error. Please correct the issues marked in red below.'

    return dict(table=table,
                row=row,
                form=form)
        
    
def list_recs():
    # list recs
    table = request.args(0)
    query = request.vars.query
    recs = db(query).select(db(table).ALL)
    return dict(recs= recs)
    
def die():
    raise HTTP(404)
    
    
def get_pages_list(current_page, number_of_pages):
    """Returns the list of page numbers for pagination
    """
    # taken from http://pypi.python.org/pypi/django-pure-pagination

    PAGE_RANGE_DISPLAYED = 8
    MARGIN_PAGES_DISPLAYED = 2

    result = []
    if number_of_pages <= PAGE_RANGE_DISPLAYED:
        return range(1, number_of_pages+1)


    left_side = PAGE_RANGE_DISPLAYED/2
    right_side = PAGE_RANGE_DISPLAYED - left_side

    if current_page > number_of_pages - PAGE_RANGE_DISPLAYED/2:
        right_side = number_of_pages - current_page
        left_side = PAGE_RANGE_DISPLAYED - right_side
    elif current_page < PAGE_RANGE_DISPLAYED/2:
        left_side = current_page
        right_side = PAGE_RANGE_DISPLAYED - left_side

    for page in xrange(1, number_of_pages+1):
        if page <= MARGIN_PAGES_DISPLAYED:
            result.append(page)
            continue
        if page > number_of_pages - MARGIN_PAGES_DISPLAYED:
            result.append(page)
            continue
        if (page >= current_page - left_side) and (page <= current_page + right_side):
            result.append(page)
            continue
        if result[-1]:
            result.append(None)

    return result    
      
def validate(table_name, id=None):
    """
    Verifies that table and id exists in db
    and returns corresponding Table and Row objects.
    """
    #table_name in tables or die()
    table = db[table_name]

    if id:
        try:
            id = int(id)
        except ValueError:
            die()

        row = table[id] or die()
    else:
        row = None

    return table, row    
    
def list_patient():
    
    # the list can self submit it's own search criteria
    # see the list html file for search ctrl definition
    print '**** processing list patient request ****'
    
    table, dummy = validate('patient')
    
    import math
    
    #table = db.patient
    fldlist =['mrn', 'date_of_birth', 'fname', 'lname', 'ethnicity']

    #fields = [field for field in table.fields if table[field].readable and table[field].type is not 'blob']
    # just show a few fields     
    fields = [field for field in fldlist if table[field].readable and table[field].type is not 'blob']

    #handle_delete(table, request.vars.bulk_ids)
      
    # Set page#
    if request.vars.page:
        current_page = int(request.vars.page)
    else:
        current_page = 1

    query = table.id > 0

    # Handle User specified search
    if request.vars.query:
        print '>>>> Query: %s' %request.vars.query
        query_str = request.vars.query

        query = table.id == 0
        for field in table.fields:
            # search all text fields for specied string
            if table[field].type in ('string', 'text'):
                query = query | table[field].contains(query_str)

    # Sorting
    #orderby = table['id']
    orderby = table['lname']
    if request.vars.sort:
        sort_by = request.vars.sort
        sort_by in table.fields or die()

        # GAE does not allow sorting by text fields
        if request.env.web2py_runtime_gae and table[sort_by].type is 'text':
            response.flash = "GAE does not allow sorting by text fields"
            request.vars.sort = 'id'
        else:
            orderby = table[sort_by]
    if request.vars.sort_reverse == 'true':
        orderby = ~orderby

    number_of_items = db(query).count()
    #items_per_page = plugins.instant_admin.items_per_page
    items_per_page = 10
    number_of_pages = int(math.ceil(number_of_items / float(items_per_page)))
    pages = get_pages_list(current_page, number_of_pages)

    limitby=((current_page-1)*items_per_page,current_page*items_per_page)

    data = db(query).select(limitby=limitby, orderby=orderby)
    

    return dict(table=table,
                fields=fields,
                current_page=current_page,
                pages=pages,
                number_of_items=number_of_items,
                number_of_pages=number_of_pages,
                data=data)

