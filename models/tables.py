# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('register',
                Field('first_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
                Field('last_name', requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC()]),
                Field('email', requires=[IS_NOT_EMPTY(), IS_EMAIL()])
                )

# I don't want to display the user email by default in all forms.
#db.post.user_email.readable = db.post.user_email.writable = False
#db.post.post_content.requires = IS_NOT_EMPTY()
#db.post.created_on.readable = db.post.created_on.writable = False
#db.post.updated_on.readable = db.post.updated_on.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
