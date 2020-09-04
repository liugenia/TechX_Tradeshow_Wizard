import cutie
import smartsheet

from program import column_name_to_id_map, REQUEST_SHEET_ID, smart

subscope_column_id = column_name_to_id_map(REQUEST_SHEET_ID)['ETS Status']

MAIN_MENU = ['****WEBHOOK MENU****',
            'Create webhook',
            'List webhooks',
            'Delete webhook',
            'Delete all',
            'Update webhook',
            'Quit']

def create_hook(name, url):  # http://d0995f8bf79e.ngrok.io/webhooks'
    webhook = smart.Webhooks.create_webhook(
        smartsheet.models.Webhook({'name': name,
                                   'callbackUrl': url,
                                   'scope': 'sheet',
                                   'scopeObjectId': REQUEST_SHEET_ID,
                                   'events': ['*.*'],
                                   'version': 1}))
    return webhook


def list_hooks():
    hooks = smart.Webhooks.list_webhooks(page_size=100,
        page=1,
        include_all=False).data
    return hooks


def format_hooks(hook_list=None): #lists hook ID, name, status, URL
    if hook_list == None:
        hook_list = list_hooks()
    elif not isinstance(hook_list, list):
        hook_list = list(hook_list)
    return [f"{hook.id}    {hook.name}    {hook.status}    {hook.callback_url}" for hook in hook_list]


def print_hooks(): #prints out the formatted webhooks
    for hook in format_hooks():
        print(hook)


def print_webhook(hook):
    print(format_hooks(hook)[0])


def delete_hook(hook_id): #deletes the selected webhook
    smart.Webhooks.delete_webhook(hook_id)


def delete_all(): #deletes all the webhooks
    for hook in list_hooks():
        delete_hook(hook.id)


def update_hook(hook_id): #enables the selected webhook
    smart.Webhooks.update_webhook(
        hook_id,smart.models.Webhook({'enabled': True}))


def select_hook(): #returns the hook object selected, can be passed onto other methods
    hooks = list_hooks()
    choices = format_hooks()
    selection = cutie.select(choices)
    return hooks[selection]


def main_menu(): #handler for all the different options listed
    while True:
        print("What would you like to do?")
        choice = cutie.select(MAIN_MENU, caption_indices=[0])
        if choice == 1:
            create_hook(input("Hook name: "), input("Hook url: "))
        elif choice == 2:
            print_hooks()
        elif choice == 3:
            delete_hook(select_hook().id)
        elif choice == 4:
            delete_all()
        elif choice == 5:
            update_hook(select_hook().id)
        elif choice == 6:
            break
        else:
            print("Not a valid response!")


if __name__ == "__main__":
    main_menu()
