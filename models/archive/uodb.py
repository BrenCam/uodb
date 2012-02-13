# -*- coding: utf-8 -*-

import os, sys
sdir = '/home/brencam/web2py'
if sdir not in sys.path:
    sys.path.append(sdir)

sdir = '/home/brencam/web2py/applications/uodb/modules'
if sdir not in sys.path:
    sys.path.append(sdir)

try:    
    from gluon import DAL, Field
except ImportError as err:
    print('gluon path not found') 

#db = DAL('sqlite://storage.sqlite', folder='../databases')
db = DAL('sqlite://storage.sqlite')

migrate=True

db.define_table('patient',
    #Field('mrn', type='string', length=10, required=True, unique=True, label=T('Medical Rec #')),
    Field('mrn', type='string', length=10, required=True, unique=True),
    Field('date_of_birth', type='datetime'),
    Field('fname', type='string', length=25),
    Field('mname', type='string', length=10),
    Field('lname', type='string', length=25),
    Field('ethnicity', type='string', length=8),
    Field('primary_tx', type='string', length=8),
    Field('marital_status', type='string', length=8),
    Field('review_status', type='string', length=8),
    Field('review_date', type='datetime'),
    Field('review_uid', type='string', length=12),
    Field('memo', type='string', length=255),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=migrate)

#
# Family History for patient -  references patient tbl
# define parent reference here
#
db.define_table('fhist',
    Field('id_patient',db.patient),
    Field('fh_none', type='boolean'),
    Field('fh_unknown', type='boolean'),
    Field('fh_brother', type='boolean'),
    Field('fh_brother_count', type='integer'),
    Field('fh_father', type='boolean'),
    Field('fh_uncle_pat', type='boolean'),
    Field('fh_uncle_mat', type='boolean'),
    Field('fh_uncle_count', type='integer'),
    Field('fh_uncle_unknown', type='boolean'),
    Field('fh_gfather_pat', type='boolean'),
    Field('fh_gfather_mat', type='boolean'),
    Field('fh_gfather_unknown', type='boolean'),
    Field('fh_dx_under_sixty', type='boolean'),
    migrate=migrate)

#
# Patient Events -  references patient tbl
# define parent reference here
#
db.define_table('event',
    Field('id_patient',db.patient),
    Field('event_type', type='string', length=12),
    Field('event_date', type='datetime'),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=migrate)

#
# Code Lookup table
#
db.define_table('codetbl',
    Field('dispseq', type='integer'),
    Field('codetype', type='string', length=25),
    Field('codesubtype', type='string', length=25),
    Field('codeval', type='string', length=25),
    Field('codedscr', type='string', length=255),
    migrate=migrate)

# lookup  table
db.define_table('codelkp',
    Field('code_type', type='string', length=8),
    Field('code_sub_type', type='string', length=8),
    Field('code_val', type='string', length=8),
    Field('code_dscr', type='string', length=80),
    Field('active', type='string', length=1),
    migrate=migrate)

# patient follow up
db.define_table('followup',
    Field('id_patient',db.patient),    
    Field('followup_date', type='datetime'),
    Field('continence', type='string', length=8),
    Field('dx_status', type='string', length=8),
    Field('status_date', type='datetime'),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=migrate)

# scheduled visits table
db.define_table('visit',
    Field('id_patient', db.patient),
    Field('date_scheduled', type='datetime'),
    Field('date_actual', type='datetime'),
    Field('visit_status', type='string', length=8),
    Field('memo', type='string', length=255),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=migrate)

#
# psa table
#
db.define_table('psa',
    Field('id_patient',db.patient),
    Field('psadate', type='datetime'),
    Field('psaval', type='double'),
    Field('psagleq', type='string', length=1),
    Field('psaupper', type='double'),
    Field('free_psa', type='double'),
    Field('free_psapct', type='double'),
    Field('assay_type', type='string', length=8),
    Field('ucsflab', type='string', length=1),
    Field('psasrc', type='string', length=8),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=migrate)


# ??Move this code to the model file - we're really building a model here
#@cache(request.env.path_info, time_expire=None, cache_model=cache.ram)
def get_status_dict():
    '''
    Build cache object for pt summary status
    keep in cache (avoid db refresh)

    ?? Build 2 dicts to support substring search 
    2nd dict has key = name + list of reletad id's in dict 1
    Apply dictlookup by name to dict 2, then search this 
    when user does a lookup
    Will need a class (DictLookupBySubstr(object): which builds a searchable list of strings
    '''

    print '>>> uodb: get_status_dict '
    #import uodbutils
    #from modules.uodbutils import DictLookupBySubstr
    #from uodbutils import DictLookupBySubstr
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
    now = datetime.now()
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

    return rdict, ludict
