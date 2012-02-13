from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'uodbdemo'
settings.subtitle = 'CRUD Demo App'
settings.author = 'BrendanC'
settings.author_email = 'patrickj@sonic.net'
settings.keywords = 'CRUD web2py'
settings.description = 'DB/CRUD Demo app built with Web2py framework'
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = 'dcb543ae-669c-4826-8fda-ae44fb6306af'
settings.email_server = 'localhost'
settings.email_sender = 'you@example.com'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
