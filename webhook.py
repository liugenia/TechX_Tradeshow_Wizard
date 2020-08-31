from program import MAP_SHEET_ID
import smartsheet

smart = smartsheet.Smartsheet()
smart.errors_as_exceptions(True)

def create_hook():
    webhook = smart.Webhooks.create_webhook(
    smartsheet.models.Webhook({
        'name': 'Update TechX Map',
        'callbackUrl': 'https://www.myApp.com/webhooks',
        'scope': 'sheet',
        'scopeObjectId': MAP_SHEET_ID,
        'events': ['*.*'],
        'version': 1}))
    return webhook

def list_hookIDs():
    webhook = smart.Webhooks.list_webhooks(
        page_size=100,
        page=1,
        include_all=False)
    return webhook

def delete_hook(hook_id):
    smart.Webhooks.delete_webhook(
    hook_id) 

def delete_all():
    pass

def update_hook():
#     smartsheet_client.Webhooks.update_webhook(
#   8444254503626628,       # webhook_id
#   smartsheet_client.models.Webhook({
#     'enabled': True}))

def program(): #make a handler for all the different options listed
    print("What would you like to do?")
    print("Create, List, Update, Delete")