import cutie
import smartsheet
from colorama import deinit, init
from termcolor import colored

from program import column_name_to_id_map, REQUEST_SHEET_ID, smart

column_id = column_name_to_id_map(REQUEST_SHEET_ID)['ETS Status']

MAIN_MENU = ['****WEBHOOK MENU****',
             'Create webhook',
             'Print webhooks',
             'Delete webhook',
             'Delete all',
             'Update webhook',
             'Quit']


def create_hook(name, url):  # http://d0995f8bf79e.ngrok.io/webhooks'
    hook = smart.Webhooks.create_webhook(
        smartsheet.models.Webhook({'name': name,
                                   'callbackUrl': url,
                                   'scope': 'sheet',
                                   'scopeObjectId': REQUEST_SHEET_ID,
                                   'events': ['*.*'],
                                   'version': 1,
                                   'subscope': smartsheet.models.WebhookSubscope({'column_ids': column_id})})).result
    print_hook(hook)
    return hook


def list_hooks():
    return smart.Webhooks.list_webhooks(include_all=True).data


def format_hooks(hook_list=None):  # lists hook ID, name, status, URL
    if hook_list is None:
        hook_list = list_hooks()
    elif not isinstance(hook_list, list):
        hook_list = [hook_list]
    init()
    result = ['   '.join([str(hook.id), hook.name, status_colorizer(hook), hook.callback_url]) for hook in hook_list]
    deinit()
    return result


def status_colorizer(hook):
    color = 'red'
    if hook.enabled:
        color = 'green'
    elif hook.status == 'NEW_NOT_VERIFIED':
        color = 'yellow'
    return colored(hook.status, color)


def print_hooks():  # prints out the formatted webhooks
    for hook in format_hooks():
        print(hook)


def print_hook(hook):
    print(format_hooks(hook)[0])


def delete_hook(hook_id):  # deletes the selected webhook
    smart.Webhooks.delete_webhook(hook_id)


def delete_all():  # deletes all the webhooks
    for hook in list_hooks():
        delete_hook(hook.id)


def update_hook(hook_id):
    hook = smart.Webhooks.update_webhook(hook_id,
                                         smart.models.Webhook({'enabled': True})).result
    print_hook(hook)
    return hook


def select_hook():  # returns the hook object selected, can be passed onto other methods
    hooks = list_hooks()
    choices = format_hooks()
    selection = cutie.select(choices)
    return hooks[selection]


def main_menu():  # handler for all the different options listed
    while True:
        print("What would you like to do?")
        choice = cutie.select(MAIN_MENU, caption_indices=[0])
        if choice == 1:
            create_hook(input("Hook name: "), input("Hook url: "))
        elif choice == 2:
            print_hooks()
        elif choice == 3:
            print('**Select webhook to delete:**')
            delete_hook(select_hook().id)
        elif choice == 4:
            delete_all()
        elif choice == 5:
            print('**Select webhook to update:**')
            update_hook(select_hook().id)
        elif choice == 6:
            break
        else:
            print("Not a valid response!")


if __name__ == "__main__":
    main_menu()
