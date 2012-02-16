response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description


#response.menu = [
#(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
#(T('View Patients'),URL('default','list patients')==URL(),URL('default','list_patient'),[]),
#(T('Register Patient'),URL('default','register patient')==URL(),URL('default','new'),[]),
#(T('Patient Status'),URL('default','status')==URL(),URL('default','status'),[]),
#(T('Patient Summary'),URL('default','search')==URL(),URL('default','search'),[]),
#(T('Patient Aggregate'),URL('default',' aggregate')==URL(),URL('default','list_status'),[]),
#(T('Custom Form'),URL('default','custom form')==URL(),URL('default','custom_form'),[]),
#]
#

response.menu = [
    (T('Home'), False, URL('default','index'), []),
    (T('Patients'), False, URL('default','list_patient'), [
        (T('Register'), False, URL('default','new'), []),        
        (T('Search'), False, URL('default','list_status'), []),
        (T('Status'), False, URL('default','status'), []),       
    ]),   
    (T('Reports'), False, URL('default','index'), [
        (T('Aggregate'), False, URL('default','custom_form'), []),        
        (T('Ajax Status'), False, URL('default','search'), []),
    ]),
    
    (T('PtCrud'), False, URL('ptcrud','index'), []),
    
    (T('CrudTest'), False, URL('default','crud_patient'), []),
    (T('CrudManage'), False, URL('default','crud_manage'), [],
    ),
    ]
    

    
        