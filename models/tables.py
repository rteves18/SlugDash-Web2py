# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

# Add DATE_FORMAT... from tables.py of local_time branch here
# Add my_validator.py to models/

# Returns a string corresponding to the user
#   first and last names, given the user email.
def get_user_name_from_email(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])

# Product table.
db.define_table('product',
                Field('product_name'),
                Field('quantity', 'integer'),
                Field('price', 'float'),
                Field('image', 'upload'),
                Field('description', 'text'),
)
db.product.id.readable = db.product.id.writable = False

# Customer order table
db.define_table('customer_order',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('delivery_location', default=auth.user.address if auth.user_id else None),
                Field('order_date', default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                Field('customer_name', 'text'),
                Field('order_total', 'float'),
                #Field('customer_info', 'blob'),
                #Field('transaction_token', 'blob'),
                Field('cart', 'blob'),
                Field('assigned_driver', default=auth.user.email if auth.user_id else None),
                Field('order_location', 'text'),
                )

# Driver scheduling table
# =============================================================
db.define_table('driver_schedule',
                Field('driver_id', default=auth.user_id, readable=False, writable=False), #saves user_id with times
                Field('driver_email', default=auth.user.email if auth.user_id else None),
                Field('driver_name', default=get_user_name_from_email(auth.user.email) if auth.user_id else None),
                Field('driver_location', 'text'),
                #Field('first_interval', 'boolean', label='21:30 to 22:30'),
                #Field('second_interval', 'boolean', label='22:30 to 23:30'),
                #Field('third_interval', 'boolean', label='23:30 to 00:30'),
                Field('signup_time', default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                Field('end_shift_time', 'datetime'),
                Field('is_on_shift', 'boolean'),
                Field('is_at_safeway', 'boolean'),
                Field('is_at_ferrells', 'boolean'),
                Field('is_at_seveneleven', 'boolean'),
                )

# Requirements
#db.driver_schedule.signup_date.requires=IS_NOT_EMPTY()
# =============================================================

# Let's define a secret key for stripe transactions.
from gluon.utils import web2py_uuid
if session.hmac_key is None:
    session.hmac_key = web2py_uuid()

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

import json

def nicefy(b):
    if b is None:
        return 'None'
    obj = json.loads(b)
    s = json.dumps(obj, indent=2)
    return s