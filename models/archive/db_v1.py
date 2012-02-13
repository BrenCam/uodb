


"""
just copy paste this code into your model and replace db to something
you prefer or what is used in your code, another thing that should be known is that
this code still cannot distinguish what exactly should be in reference title - name
when you use generic appadmin so please remove all fiealds you don't need not require 
"""
"""
database class object creation
"""
#db = SQLDB("sqlite://db.db")

"""
Table definition
"""
#db.define_table("Patient",
#      SQLField("mrn", "CHAR", length=10, notnull=True, default=None),
#      SQLField("lname", "VARCHAR", length=20, notnull=True, default=None))


"""
Table definition
"""
#db.define_table("Encounter",
#      SQLField("id_Patient", db.Patient),
#      SQLField("entype", "CHAR", length=8, notnull=True, default=None),
#      SQLField("endate", "DATETIME", notnull=True, default=None))


"""
Relations between tables (remove fields you don't need from requires)
"""
#db.Encounter.id_Patient.requires=IS_IN_DB(db, 'Patient.id','Patient.mrn','Patient.lname')


