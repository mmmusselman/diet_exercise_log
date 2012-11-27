# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    response.flash = 'this is index()'
    return dict()

@auth.requires_login()
def menu():
    diet_items = db(db.diet_item.owner_id==auth.user_id).select(db.diet_item.ALL, 
        orderby=db.diet_item.type)
    return dict(diet_items=diet_items)

@auth.requires_login()
def view_logs():
    meals = db(db.meal.owner_id==auth.user_id).select(db.meal.ALL, orderby=db.meal.dt)
    return dict(meals=meals)

@auth.requires_login()
def settings():
    response.flash = 'this is settings()'
    return dict()
    
@auth.requires_login()
def add_diet_item():
    response.flash = 'this is add_diet_item()'
    import urllib, urllib2
    import json
    results = json.loads(urllib.urlopen('http://api.esha.com/foods?apikey=xck7a6d547sknsh3tuca6vdx&query=snickers').read(), encoding='UTF-8')
    items = results['items']
    
    data = {"items": [ { "id": "urn:uuid:914939fb-0571-45b2-bc98-a3a8122ceb72",
                         "quantity": 1, "unit": "urn:uuid:85562e85-ba37-4e4a-8400-da43170204a7" } ]
           }
    req = urllib2.Request('http://api.esha.com/analysis?apikey=xck7a6d547sknsh3tuca6vdx')
    req.add_header('Content-Type', 'application/json')
    f=urllib2.urlopen(req, json.dumps(data))
    broccoli = f.read()
    
    nutrients = json.loads(urllib.urlopen('http://api.esha.com/nutrients?apikey=xck7a6d547sknsh3tuca6vdx').read(), encoding='UTF-8')
    units = json.loads(urllib.urlopen('http://api.esha.com/food-units?apikey=xck7a6d547sknsh3tuca6vdx').read(), encoding='UTF-8')
    return dict(items=items, broccoli=broccoli, nutrients=nutrients, units=units)
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
