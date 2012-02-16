# -*- coding: utf-8 -*-
'''
Crud Controlled for web2py test application - use for handling patient related data
'''
#########################################################################
## This is a crud patient controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


if 0:
    # for ide web2py support
    # see: http://kollerie.wordpress.com/2009/04/07/setting-up-your-ide-for-web2py-development/    
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
    
PATIENT_SHOW_COUNT = 5

def index():
    response.files.append(URL(request.application, 'static/css', 'index.css'))
    # Return the most recent X patients to display on the page.
    # sort by desc dob
    allPatients = db().select(db.patient.ALL, orderby =~ db.patient.date_of_birth)
    recentPatients = allPatients[:PATIENT_SHOW_COUNT ]
    return dict(patients = recentPatients)    

def edit_patient():
    """ Allows for editing of the selected patient record. Post id passed as a query
    parameter. 
    """
    patient_id = request.vars['patient']
    update_form = crud.update(db.patient, patient_id, next=URL('index'))
    return dict(form=update_form)

def data():
    """                                      
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

def create_patient():
    """ Write a pt rec. """
    makePatient = crud.create(db.patient, next=URL('index'))
    return dict(form=makePatient)