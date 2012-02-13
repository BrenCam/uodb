'''
File: dbload.py
Populate sqlitestest db with data from postgres db
initially < 100 patients

Tables to populate:
 - patient
 - psa
 - codelkp
 - followup
 
'''

import os, sys
sdir = '/home/brencam/web2py'
sys.path.append(sdir)

sdir = '/home/brencam/web2py/applications/uodb'
sys.path.append(sdir)

sdir = '/home/brencam/web2py/applications/uodb/models'
sys.path.append(sdir)

print sys.path

try:    
    from gluon import DAL, Field
except ImportError as err:
    print('gluon path not found') 
    
# Source db - postgres

dbs = DAL("postgres://postgres:@localhost:5432/uroldb")

# local def for pg table
dbs.define_table('patient',
    Field('id', type='integer'),
    Field('mhid', type='integer'),
    Field('ucsf_id', type='string', length=10),
    Field('vamc_id', type='string', length=9),
    Field('date_of_birth', type='datetime'),
    Field('fname', type='string', length=25),
    Field('mname', type='string', length=10),
    Field('lname', type='string', length=25),
    Field('ethnicity', type='string', length=8),
    Field('primary_tx', type='string', length=8),
    Field('marital_status', type='string', length=8),
    Field('education_lvl', type='string', length=8),
    Field('income_lvl', type='string', length=8),
    Field('weight', type='integer'),
    Field('height', type='integer'),
    Field('physician', type='integer'),
    Field('ref_phys', type='string', length=50),
    Field('ref_phys_phn', type='string', length=12),
    Field('ref_phys_city', type='string', length=20),
    Field('ref_phys_state', type='string', length=2),
    primarykey=['id'],
    migrate=False)

dbs.define_table('codetbl',
    Field('id', type='id'),
    Field('dispseq', type='integer'),
    Field('codetype', type='string', length=25),
    Field('codesubtype', type='string', length=25),
    Field('codeval', type='string', length=25),
    Field('codedscr', type='string', length=255),
    migrate=False)

# Code Lookup
dbs.define_table('zlkpcode',
#    Field('code_id', type='integer'),
#  define alias for id for legacy table
    Field('code_id', 'id'),
    Field('code_type', type='string', length=8),
    Field('code_sub_type', type='string', length=8),
    Field('code_val', type='string', length=8),
    Field('code_dscr', type='string', length=80),
    Field('active', type='string', length=1),
    migrate=False)

#
# psa table
#
dbs.define_table('psa',
#  define alias for psaid for legacy table
    Field('psaid', 'id'),                 
    Field('patient_id',dbs.patient),
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
    migrate=False)

# follow up table
dbs.define_table('prst_followup',
#  define alias for fuid for legacy table
    Field('fuid', 'id'),                   
#    Field('fuid', type='integer'),
    Field('patient_id', type='integer'),
    Field('tx_id', type='integer'),
    Field('follow_up_date', type='datetime'),
    Field('cpl_type', type='string', length=8),
    Field('cpl_mi', type='integer'),
    Field('cpl_dvt', type='integer'),
    Field('cpl_pneumonia', type='integer'),
    Field('cpl_sbobstruct', type='integer'),
    Field('cpl_urinary_retention', type='integer'),
    Field('cpl_wound_infect', type='integer'),
    Field('cpl_anastomotic_leak', type='integer'),
    Field('cpl_fluid_collection', type='integer'),
    Field('efstatus', type='string', length=8),
    Field('iiefscore', type='integer'),
    Field('eftreatment', type='string', length=8),
    Field('eftx_none', type='integer'),
    Field('eftx_cialis', type='integer'),
    Field('eftx_inject', type='integer'),
    Field('eftx_levitra', type='integer'),
    Field('eftx_muse', type='integer'),
    Field('eftx_prosthesis', type='integer'),
    Field('eftx_vacuum_dev', type='integer'),
    Field('eftx_viagra', type='integer'),
    Field('continence', type='string', length=8),
    Field('auascore', type='double'),
    Field('auaqol', type='double'),
    Field('dx_status', type='string', length=8),
    Field('status_date', type='datetime'),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=False)

# scheduled visits table
dbs.define_table('visits',
    Field('id', type='integer'),
    Field('patient_id', type='integer'),
    Field('date_scheduled', type='datetime'),
    Field('date_actual', type='datetime'),
    Field('visit_status', type='string', length=8),
    Field('memo', type='string', length=255),
    Field('create_date', type='datetime'),
    Field('create_uid', type='string', length=12),
    Field('modify_date', type='datetime'),
    Field('modify_uid', type='string', length=12),
    migrate=False)

# target db - sqlite    
#db = DAL("sqlite://storage.sqlite")
#from models
import appdb

db =appdb.db

def poppatient(sdb,ddb):
    # populate dest db from source db
    # splitting contents of pg table into 2 separate tables
   
        # List tables defined
    #for t in ddb.tables:
    #    print '>>>> dest table: %s' %t
    
    ddict = {}
    rcnt = 0
    for row in sdb().select(sdb.patient.ALL, limitby=(11,50)):
        rcnt+= 1
        if rcnt%3 == 0:
            print '******* Processed %s patient recs *********' %rcnt
    #for row in sdb().select(sdb.patient.ALL):
        
        #print 'Patient Name: %s' %row.lname

        # ??build list of matching field names or try;catch
        # pop  patient tbl
        for fldname in sdb.patient.fields:
            #print 'sdb field name: %s' %fldname
            # build a dict for tbl insert
            if fldname == 'ucsf_id':
                #print 'ucsf_id: %s' %row[fldname]
                if row[fldname] is None:
                    print '>>> Missing MRN <<<'
                    # skip missing mrn entries
                    continue
                else:
                #ddb.patient['mrn'] = row[fldname]
                    ddict['mrn'] = row[fldname]
            else:
                # ignore non matching names
                if fldname in ddb.patient.fields:
                    #print 'matching names: %s; %s' %(fldname, row[fldname])
                    ddict[fldname] = row[fldname]
        print '>>> Insert New Row <<<'
        try:
            print 'Inserting rec for patient : %s' %ddict['mrn']
            ddb.patient.insert(**ddict)
            ddb.commit()
        except:
            ddb.rollback()
            
# Code table (this table is deprecated)           
def popcodetbl(sdb,ddb):
    # populate code table - simple copy each field
    print '>>> popcodetbl -  start <<<'
    try:
        ddb.codetbl.bulk_insert(sdb().select(sdb.codetbl.ALL).as_list())
        ddb.commit()
    except:
        print '>>> Bulk Insert Failed : error: %s <<<' %error
        ddb.rollback()
    print '>>> popcodetbl -  end <<<'
    
def zz_poplkptbl(sdb,ddb):
    # populate lookup table - simple copy each field
    print '>>> poplkptbl -  start <<<'
    try:
        ddb.codelkp.bulk_insert(sdb().select(sdb.zlkpcode.ALL).as_list())
        ddb.commit()
        print '**** Successful Copy ****'
    except:
        #print '>>> Bulk Insert Failed : error: %s <<<' %error
        #raise RuntimeError, 'Script error'
        print '**** Copy Failed ****'
        print sys.exc_info()
        ddb.rollback()
    print '>>> poplkptbl -  end <<<'
    
def poplkptbl(sdb,ddb):
    # populate dest db from source db    
    ddict = {}
    rcnt = 0
    for row in sdb().select(sdb.zlkpcode.ALL):
        rcnt+= 1
        if rcnt%100 == 0:
            print '******* Processed %s lookup recs *********' %rcnt
        for fldname in sdb.zlkpcode.fields:
            if fldname == 'zzid':
                # skip this field
                continue
            else:
                # ignore non matching names
                if fldname in ddb.codelkp.fields:
                    print 'matching names: %s; %s' %(fldname, row[fldname])
                    ddict[fldname] = row[fldname]
                else:
                    continue
        #print '>>> Insert New Row <<<'
        try:
            for (k,v) in ddict.iteritems():
                print 'Dict Key: %s; Value: %s' %(k,v)                
            print 'Inserting rec for code : %s' %ddict['code_type']
            ddb.codelkp.insert(**ddict)
            ddb.commit()
        except:
            print '**** Copy Failed ****'
            print sys.exc_info()
            ddb.rollback()
            # bail out
            break
    print '>>>> Done - Processed %s rows <<<<' %rcnt
    
# psa table - bulk insert
# fails since col names don't match
def zzpoppsa(sdb,ddb):
    # populate code table - simple copy each field
    print '>>> poppsa -  start <<<'
    try:
        ddb.psa.bulk_insert(sdb().select(sdb.psa.ALL).as_list())
        ddb.commit()
    except:
        print sys.exc_info()
        ddb.rollback()
    rcnt = ddb(ddb.psa.id>0).count()
    
    #check rec count 
    #cnt = db(db.emp.id>0).count()
    #print '>>> Emp Rec Count: %s' %cnt
    
    print '>>> poppsa -  end - created: %s psa recs<<<' %rcnt
    
    
 # psa table  - field by field (limit to PIDs < 100)           
def poppsa(sdb,ddb):
    # populate code table - simple copy each field
    print '>>> poppsa -  start <<<'   
        # populate dest db from source db    
    ddict = {}
    rcnt = 0
    #for row in sdb().select(sdb.psa.ALL, limitby=(0,1)):
    for row in sdb().select(sdb.psa.ALL, orderby=sdb.psa.patient_id):        
        # ignore recs for pids > 100
        if row.patient_id > 50:
            break
        # pop  patient tbl
        for fldname in sdb.psa.fields:
            #print 'sdb field name: %s' %fldname
            # build a dict for tbl insert
            # handle renamed fields
            if fldname == 'patient_id':
                    ddict['id_patient'] = row[fldname]
            else:
                # ignore non matching names
                if fldname in ddb.psa.fields:
                    #print 'matching names: %s; %s' %(fldname, row[fldname])
                    ddict[fldname] = row[fldname]
        print '>>> Insert New Row <<<'
        try:
            #print 'Inserting rec for psa : %s' %ddict['id_patient']
            rcnt+= 1
            ddb.psa.insert(**ddict)
            ddb.commit()
        except:
            print sys.exc_info()
            ddb.rollback()

    #check rec count     
    rcnt = ddb(ddb.psa.id>0).count()
    print '>>> poppsa -  end - created: %s psa recs<<<' %rcnt
    
# follow up table (subset of postgres files)
# note: tbl name change from prst_followup -> followup
def popfu(sdb,ddb):
    # populate code table - simple copy each field
    print '>>> popfu -  start <<<'   
        # populate dest db from source db    
    ddict = {}
    rcnt = 0
    for row in sdb().select(sdb.prst_followup.ALL, orderby=sdb.prst_followup.patient_id):        
        # ignore recs for pids > 100
        if row.patient_id > 50:
            break
        # pop  patient tbl
        for fldname in sdb.prst_followup.fields:
            #print 'sdb field name: %s' %fldname
            # build a dict for tbl insert
            # handle renamed fields
            if fldname == 'patient_id':
                    ddict['id_patient'] = row[fldname]
            else:
                # ignore non matching names
                if fldname in ddb.followup.fields:
                    #print 'matching names: %s; %s' %(fldname, row[fldname])
                    ddict[fldname] = row[fldname]
        print '>>> Insert New Row <<<'
        try:
            #print 'Inserting rec for psa : %s' %ddict['id_patient']
            rcnt+= 1
            ddb.followup.insert(**ddict)
            ddb.commit()
        except:
            print sys.exc_info()
            ddb.rollback()

    #check rec count     
    rcnt = ddb(ddb.followup.id>0).count()
    print '>>> popfu -  end - created: %s followup recs<<<' %rcnt
    
# note: tbl name change from visits -> visit   
def popvisit(sdb,ddb):
    # populate code table - simple copy each field
    print '>>> popvisit -  start <<<'   
        # populate dest db from source db    
    ddict = {}
    rcnt = 0
    for row in sdb().select(sdb.visits.ALL, orderby=sdb.visits.patient_id):        
        # ignore recs for pids > 100
        if row.patient_id > 50:
            break
        # pop  patient tbl
        for fldname in sdb.visits.fields:
            #print 'sdb field name: %s' %fldname
            # build a dict for tbl insert
            # handle renamed fields
            if fldname == 'patient_id':
                    ddict['id_patient'] = row[fldname]
            else:
                # ignore non matching names
                if fldname in ddb.visit.fields:
                    #print 'matching names: %s; %s' %(fldname, row[fldname])
                    ddict[fldname] = row[fldname]
        print '>>> Insert New Row <<<'
        try:
            #print 'Inserting rec for psa : %s' %ddict['id_patient']
            rcnt+= 1
            ddb.visit.insert(**ddict)
            ddb.commit()
        except:
            print sys.exc_info()
            ddb.rollback()

    #check rec count     
    rcnt = ddb(ddb.visit.id>0).count()
    print '>>> popvisit -  end - created: %s visit recs<<<' %rcnt
    
def getpt_summary(ddb):
    '''
    get patient summary info (last psa, last fu etc)
    return a dictionary
    '''
    rdict = {}
    
    # List tables defined in target
    #for t in ddb.tables:
    #    print '   **** dest table (sqlite): %s' %t
    
    # get last psa date
    lastpsa = ddb.psa.psadate.max()
    rows = ddb(ddb.psa).select(ddb.psa.id_patient, lastpsa, groupby=ddb.psa.id_patient)
    #psadict = rows.as_dict(key='psa.id_patient')
    psadict = {}
    for r in rows:
        tdict = {}
        pid = r.psa.id_patient
        tdict['lastpsa'] = r[lastpsa]
        tdict['id_patient'] = pid
        psadict[pid] = tdict      
        #t.strftime("%Y-%m-%d 
        #print 'Patient ID: %s, Last PSA: %s' %(r.psa.id_patient, r[lastpsa].strftime("%Y-%m-%d"))
        #print 'Patient ID: %s, Last PSA: %s' %(r.psa.id_patient, r[lastpsa][0:10])
    #print ddb._lastsql
    #print psadict

    # get last fu date 
    lastfu = ddb.followup.followup_date.max()
    rows = ddb(ddb.followup).select(ddb.followup.id_patient, lastfu, groupby=ddb.followup.id_patient)
    #fudict = rows.as_dict(key='followup.id_patient')
    fudict = {}
    #build a list of dictionaries for each id found
    for r in rows:
        tdict = {}
        pid = r.followup.id_patient
        tdict['lastfu'] = r[lastfu]
        tdict['id_patient'] = pid
        fudict[pid] = tdict      
        #t.strftime("%Y-%m-%d 
        #print 'Patient ID: %s, Last PSA: %s' %(r.psa.id_patient, r[lastpsa].strftime("%Y-%m-%d"))
        #print 'Patient ID: %s, Last FU: %s' %(r.followup.id_patient, r[lastfu][0:10])
    #print ddb._lastsql

    # result patient data as a list of dictionaries
    plist = ddb(ddb.patient).select().as_list()
    #print type(plist)   
    #print fudict
    
    # Build dictionary from intermetiate dicts
    # ?? How to sort in asc pt order ??
    for  ddict in plist:        
        #print type(ddict)
        sdict={}
        #print 'Current Pt: %s' %ddict['id']
        id = sdict['id'] = ddict['id']
        
        # populate pt fields
        sdict['mrn'] = ddict['mrn']
        sdict['lname'] = ddict['lname']
        #id = ddict['id']
        if fudict.has_key(id):
            tdict = fudict[id]
            sdict['lastfu'] = tdict['lastfu'] 
        else:
            sdict['lastfu'] = 'None'
            
        if psadict.has_key(id):
            tdict = psadict[id]
            sdict['lastpsa'] = tdict['lastpsa'] 
        else:
            sdict['lastpsa'] = 'None'            
            
        rdict[id] = sdict
    #print sdict
    return rdict
    
    
if __name__ == "__main__":
    
    # Connect to SQLite db
    import datetime
    dtstart = datetime.datetime.now()
    print '\n>>>>Starting at: %s <<<<\n' %dtstart.ctime()
    
    #rows = mdb()._select(mdb,patient.ALL, limitby=(0,10))
    
    print 'Source DB: Db uri: %s; DB Name: %s' %(dbs._uri, dbs._dbname)    
    print 'Dest DB: Db uri: %s; DB Name: %s' %(db._uri, db._dbname)
        
    # List tables defined in source
    for t in dbs.tables:
        print 'source pgtable (postgres): %s' %t
        
    # List tables defined in target
    for t in db.tables:
        print 'target table (sqlite): %s' %t
        
    #poppatient(dbs,db)
    #poplkptbl(dbs,db)
    
    #poppsa(dbs,db)
    #follow up 
    #popfu(dbs,db)
    #popvisit(dbs,db)
    
    # get list of critical dates etc per patient using DAL
    # id, lname, mrn, last psa, last fu, next/scheduled visit
    
    ptsummary =getpt_summary(db)
    
    #print ptsummary
    for rec in ptsummary.itervalues():
        #print rec
        print 'Pid: %s, Mrn: %s, Name: %s, Last PSA: %s, Last FU: %s' %(rec['id'], rec['mrn'], rec['lname'], rec['lastpsa'][0:10], rec['lastfu'])
               
    dtstop = datetime.datetime.now()
    print '\n>>>>Stopping at: %s <<<<\n' %dtstop.ctime()
