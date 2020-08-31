from program import REQUEST_SHEET_ID, smart
import smartsheet

def create_hook(name, url): #http://d0995f8bf79e.ngrok.io/webhooks'
    webhook = smart.Webhooks.create_webhook(
    smartsheet.models.Webhook({
        'name': name,
        'callbackUrl': url,
        'scope': 'sheet',
        'scopeObjectId': REQUEST_SHEET_ID,
        'events': ['*.*'],
        'version': 1}))
    return webhook


def list_hooks():
    hooks = smart.Webhooks.list_webhooks(
        page_size=100,
        page=1,
        include_all=False).data
    for hook in hooks:
        print(hook.id, hook.name, hook.status, hook.callback_url)
    return hooks


def delete_hook(hook_id):
    smart.Webhooks.delete_webhook(
    hook_id)


def delete_all():
    for hook in list_hooks():
        smart.Webhooks.delete_webhook(
        hook.id)


def update_hook(hook_id):
    smart.Webhooks.update_webhook(
        hook_id,
        smart.models.Webhook({
            'enabled': True}))


def program(): #make a handler for all the different options listed
    while True:
        print("What would you like to do?")
        response = input("Create, List, Update, Delete, All Delete? ")
        if response.lower()[0] == 'c':
                create_hook(input("Hook name: "), input("Hook url: "))
        elif response.lower()[0] == 'l':
                list_hooks()
        elif response.lower()[0] == 'd':
            delete_hook(input('Hook ID: '))
        elif response.lower()[0] == 'a':
            delete_all()
        elif response.lower()[0] == 'u':
            update_hook(input("Hook ID: "))
        elif response.lower()[0] == 'q':
            break
        else:
            print("Not a valid response!")

if __name__ == "__main__":
    program()