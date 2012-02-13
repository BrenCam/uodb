# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

# for ide web2py support
# see: http://kollerie.wordpress.com/2009/04/07/setting-up-your-ide-for-web2py-development/
if 0:
    from gluon.sql import *
    from gluon.validators import *


# 2/7/2012 - auto track module changes 
from gluon.custom_import import track_changes; track_changes(True)

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    ##db = DAL('sqlite://storage.sqlite', folder='../databases')
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables

########################################
db.define_table('auth_user',
    Field('username', type='string',
          label=T('Username')),
    Field('first_name', type='string',
          label=T('First Name')),
    Field('last_name', type='string',
          label=T('Last Name')),
    Field('email', type='string',
          label=T('Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
    Field('created_on','datetime',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','datetime',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('registration_key',default='',
          writable=False,readable=False),
    Field('reset_password_key',default='',
          writable=False,readable=False),
    Field('registration_id',default='',
          writable=False,readable=False),
    format='%(username)s',
    migrate=settings.migrate)


db.auth_user.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
db.auth_user.password.requires = CRYPT(key=auth.settings.hmac_key)
db.auth_user.username.requires = IS_NOT_IN_DB(db, db.auth_user.username)
db.auth_user.registration_id.requires = IS_NOT_IN_DB(db, db.auth_user.registration_id)
db.auth_user.email.requires = (IS_EMAIL(error_message=auth.messages.invalid_email),
                               IS_NOT_IN_DB(db, db.auth_user.email))
auth.define_tables(migrate = settings.migrate)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login


migrate=True

# lookup  table
db.define_table('codelkp',
    Field('code_type', type='string', length=8),
    Field('code_sub_type', type='string', length=8),
    Field('code_val', type='string', length=8),
    Field('code_dscr', type='string', length=80),
    Field('active', type='string', length=1),
    migrate=migrate)

# build lookup/code list for dropdown lists
ethlst = []
for item in (db(db.codelkp.code_type=='ETHNCTY ').select(db.codelkp.code_val) ):
    ethlst.append(item['code_val'])

db.define_table('patient',
    #Field('mrn', type='string', length=10, required=True, unique=True, label=T('Medical Rec #')),
    Field('mrn', type='string', length=10, required=True, unique=True),
    Field('date_of_birth', type='datetime', requires = IS_EMPTY_OR(IS_DATE()),required=True),
    Field('fname', type='string', length=25),
    Field('mname', type='string', length=10),
    Field('lname', type='string', length=25, requires=IS_NOT_EMPTY()),
    #Field('ethnicity', type='string', length=8),
    #Field('ethnicity', type='string', requires= IS_IN_SET(['White','Asian', 'AfAmer'])),
    #Field('ethnicity', type='string',                  \
    #        requires= IS_IN_SET (db(db.codelkp.code_type=='ETHNCTY ').select(db.codelkp.code_val) )),
    Field('ethnicity', type='string', requires= IS_IN_SET (ethlst)),        
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


##################
#
# db view testing
# define some virtual fields here (psa stale, fustale)
#
##################
db.define_table('v_summary',
    Field('mrn', type='string'),
    Field('lname', type='string', length=25),
    Field('lastpsa', type='datetime'),
    Field('lastfu', type='datetime'),
    migrate=False)

import datetime
now = datetime.datetime.now()
# define some virtual fields
pdiff = 2500
fdiff = 365
db.v_summary.pstale =Field.Virtual(lambda row, diff=pdiff:
    True if (now - row.v_summary.lastpsa).days > diff else False)
db.v_summary.fstale =Field.Virtual(lambda row, diff = fdiff:
    True if (row.v_summary.lastfu is None or (now - row.v_summary.lastfu).days > fdiff) else False)
    
            
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

    #print '>>> (models:db.py) uodb: get_status_dict '
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
            #print '****** %s ' %sdate
            #fudt = datetime.strptime(sdate, '%Y/%m/%d')
            fudt = datetime.strptime(sdate, '%Y-%m-%d %H:%M:%S')
            
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

    #print rdict, ludict
    return rdict, ludict

def pretty(s):
    s = str(s).replace('_',' ').title()
    if s.endswith(' Id'):
        s = s.replace(' Id', '')
    return s


def plural(name):
    """Minimal and stupid"""
    name=pretty(name)

    if name.endswith('s'):
        return name
    else:
        return name + 's'


def singular(name):
    """Minimal and stupid"""
    name=pretty(name)

    if name.endswith('s'):
        return name[:-1]
    else:
        return name

