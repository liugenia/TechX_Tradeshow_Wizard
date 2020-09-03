import smartsheet
from colorama import deinit, init
from termcolor import colored

from program import column_name_to_id_map, REQUEST_SHEET_ID, smart

subscope_column_id = column_name_to_id_map(REQUEST_SHEET_ID)['ETS Status']


def create_hook(name, url):  # http://d0995f8bf79e.ngrok.io/webhooks'
    hook = smart.Webhooks.create_webhook(
        smartsheet.models.Webhook({'name': name,
                                   'callbackUrl': url,
                                   'scope': 'sheet',
                                   'scopeObjectId': REQUEST_SHEET_ID,
                                   'events': ['*.*'],
                                   'version': 1})).result
    print_webhook(hook)
    return hook


def list_hooks():
    return smart.Webhooks.list_webhooks(include_all=True).data


def print_webhooks():
    hooks = list_hooks()
    for hook in hooks:
        print_webhook(hook)
    return hooks


def print_webhook(hook):
    init()

    color = 'red'
    if hook.enabled:
        color = 'green'
    elif hook.status == 'NEW_NOT_VERIFIED':
        color = 'yellow'

    print(hook.id,
          hook.name,
          colored(hook.status, color),
          hook.callback_url,
          sep='   ')

    deinit()


def delete_hook(hook_id):
    smart.Webhooks.delete_webhook(hook_id)


def delete_all():
    for hook in list_hooks():
        delete_hook(hook.id)


def update_hook(hook_id):
    hook = smart.Webhooks.update_webhook(hook_id,
                                         smart.models.Webhook({'enabled': True})).result
    print_webhook(hook)
    return hook


def program():  # make a handler for all the different options listed
    while True:
        print("What would you like to do?")
        response = input("Create, Print, Update, Delete, All Delete, Quit? ")
        if response.lower()[0] == 'c':
            create_hook(input("Hook name: "), input("Hook url: "))
        elif response.lower()[0] == 'p':
            print_webhooks()
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
