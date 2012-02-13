# -*- coding: utf-8 -*-

import os, sys
sdir = '/home/brencam/web2py'
sys.path.append(sdir)


try:    
    from gluon import DAL, Field
except ImportError as err:
    print('gluon path not found') 

# reference db current app db directory
#db = DAL('sqlite://storage.sqlite',folder='../databases')
#db = DAL('sqlite://storage.sqlite')

