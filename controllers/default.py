# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# Sample shopping cart implementation.
# -------------------------------------------------------------------------

import traceback

def index():
    sched = db().select(db.driver_schedule.ALL)

    return dict(sched=sched,)

def set_timezone():
    """Ajax call to set the timezone information for the session."""
    tz_name = request.vars.name
    # Validates the name.
    from pytz import all_timezones_set
    if tz_name in all_timezones_set:
        session.user_timezone = tz_name
        # If the user is logged in, sets also the timezone for the user.
        # Otherwise, it can happen that a user expires a cookie, then click on edit.
        # When the user is presented the edit page, the translation is done according to UTC,
        # but when the user is done editing, due to autodetection, the user is then in
        # it's own time zone, and the dates of an assignment change.
        # This really happened.
        if auth.user is not None:
            db.auth_user[auth.user.id] = dict(user_timezone = tz_name)
        logger.info("Set timezone to: %r" % tz_name)
    else:
        logger.warning("Invalid timezone received: %r" % tz_name)

""" Old code to get product from local
def get_products():
    #Gets the list of products, possibly in response to a query.
    t = request.vars.q.strip()
    if request.vars.q:
        q = ((db.product.name.contains(t)) |
             (db.product.description.contains(t)))
    else:
        q = db.product.id > 0
    products = db(q).select(db.product.ALL)
    # Fixes some fields, to make it easy on the client side.
    # Add fields to products here.
    for p in products:
        p.image_url = URL('download', p.image)
        p.desired_quantity = min(1, p.quantity)
        p.cart_quantity = 0
    return response.json(dict(
        products=products,
    ))
"""


# Fetch products from server
def get_products():
    import requests
    r = requests.get('http://bookswap-rark.appspot.com/')
    result = r.json()
    products = result['products']
    for p in products:
        p['desired_quantity'] = min(1, p['quantity'])
        p['cart_quantity'] = 0
    logged_in = auth.user_id is not None
    return response.json(dict(products=products, logged_in=logged_in))


# Fetch orders from server
@auth.requires_login()
def get_orders():
    orders = db(db.customer_order.user_email == auth.user.email).select(db.customer_order.ALL,
                         orderby=~db.customer_order.order_date) # sort by order_date
    for order in orders:
        #order.customer_info = json.loads(order.customer_info)
        order.cart = json.loads(order.cart)

    return response.json(dict(orders=orders, ))


# Returns a string corresponding to the user
#   first and last names, given the user email.
def get_user_name_from_email(email):
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


@auth.requires_login()
def purchase():
    """Ajax function called when a customer orders and pays for the cart."""
    if not URL.verify(request, hmac_key=session.hmac_key):
        raise HTTP(500)

    ds = db().select(db.driver_schedule.ALL)
    co = db().select(db.customer_order.ALL)

    #for d in db(db.driver_schedule.driver_location == db.customer_order.order_location).select():
    #    print("Ferrells" + d.driver_email)

    db.customer_order.insert(
        #customer_info=request.vars.customer_info,
        delivery_location=request.vars.delivery_location,
        #transaction_token=request.vars.transaction_token,
        order_total=request.vars.order_total,
        customer_name=get_user_name_from_email(auth.user.email),
        #user_email=request.vars.user_email,
        #transaction_token=json.dumps(token),
        order_location=request.vars.order_location,
        cart=request.vars.cart)

    assign_driver()

    #print(request.vars.cart)

    #for order in orders:
    #    order.cart = json.loads(order.cart)
    #    for item in order.cart:
    #       print(item['location'])

    #get_driver(db.customer_order.order_location)

    return "ok"

def assign_driver():
    ds = db().select(db.driver_schedule.ALL)
    co = db().select(db.customer_order.ALL)
    for d in ds:
        for c in co:
            if c.order_location == d.driver_location:
                db(db.customer_order.id == c.id).update(assigned_driver=d.driver_email)

    return "ok"

""" Get Driver at location ========================================================================
def get_driver(location):
    drivers = db.driver_schedule.ALL





 =============================================================================================== """





# Normally here we would check that the user is an admin, and do programmatic
# APIs to add and remove products to the inventory, etc.
#@auth.requires_membership('super_admin')
def product_management():
    q = db.product # This queries for all products.
    form = SQLFORM.grid(
        q,
        editable=True,
        create=True,
        user_signature=True,
        deletable=True,
        details=True,
    )
    return dict(form=form)


""" Viewing orders
Need to work on:
    + Display what/when they ordered
    + Display if a payment for that order is successful
    + Create group authentication to prevent certain users from accessing this page
    + Maybe work on improving the UI
"""
#@auth.requires_membership('super_admin')
#@auth.requires(auth.has_membership(group_id='driver'))
def view_orders():
    q = db.customer_order # This queries for all products.
    #db.customer_order.customer_info.represent = lambda v, r: nicefy(v)
    #db.customer_order.transaction_token.represent = lambda v, r: nicefy(v)
    db.customer_order.cart.represent = lambda v, r: nicefy(v)

    orders = db().select(db.customer_order.ALL,
                         orderby=~db.customer_order.order_date) # sort by order_date

    #db().select(db.customer_order.order_total)
    for order in orders:
        #order.customer_info = json.loads(order.customer_info)
        order.cart = json.loads(order.cart)

    form = SQLFORM.grid(
        q,
        editable=True,
        create=True,
        user_signature=True,
        deletable=True,
        details=True,
        orderby=~db.customer_order.order_date,
    )
    return dict(form=form, orders=orders)



# Interface for managing schedule for drivers
@auth.requires(auth.has_membership('super_admin') or auth.has_membership('driver'))
def manage_schedule():
    q = db.driver_schedule
    o = db.customer_order

    orders = db(db.customer_order.assigned_driver == auth.user.email).select(db.customer_order.ALL,
                                                                        orderby=~db.customer_order.order_date)

    for order in orders:
        order.cart = json.loads(order.cart)

    sched = db().select(db.driver_schedule.ALL)

    form = SQLFORM.grid(
        q,
        editable=True,
        create=True,
        user_signature=True,
        deletable=True,
        details=True,
    )

    form2 = SQLFORM.grid(
        o,
        editable=True,
        create=True,
        user_signature=True,
        deletable=True,
        details=True,
    )

    return dict(form=form, sched=sched, orders=orders)


start_shift_id = 0

@auth.requires(auth.has_membership('super_admin') or auth.has_membership('driver'))
def start_shift():

    t = datetime.datetime.now()
    if t.hour < 23:
        new_t = t.replace(hour=t.hour+1)
    elif t.hour == 23: #t.hour cannot go above 23, therefore I need to reset to 0 and add a new day
        new_t = t.replace(hour=0, day=t.day+1)
    else:
        print("post_schedule else reached")

    #db(db.driver_schedule.driver_email == auth.user.email).delete

    db.driver_schedule.insert(
        is_on_shift=request.vars.is_on_shift,
        driver_location=request.vars.driver_location,
        end_shift_time=new_t,
        is_at_safeway=request.vars.is_at_safeway,
        is_at_ferrells=request.vars.is_at_ferrells,
        is_at_seveneleven=request.vars.is_at_seveneleven,
    )

    start_shift_id = db().select(db.driver_schedule.id)
    #print(type(driver_id))
    return "ok"



@auth.requires(auth.has_membership('super_admin') or auth.has_membership('driver'))
def end_shift():
    db(db.driver_schedule.driver_email==auth.user.email).update(is_on_shift=False)
    db(db.driver_schedule.driver_email == auth.user.email).update(is_at_safeway=False)
    db(db.driver_schedule.driver_email == auth.user.email).update(is_at_seveneleven=False)
    db(db.driver_schedule.driver_email == auth.user.email).update(is_at_ferrells=False)

    ds = db().select(db.driver_schedule.ALL)
    for d in ds:
        if db.driver_schedule.id == start_shift_id:
            db(db.driver_schedule.driver_email == auth.user.email).update(
                end_shift_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return "ok"



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
