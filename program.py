import smartsheet

smart = smartsheet.Smartsheet('YOUR API KEY AS A STRING')
smart.errors_as_exceptions(True)

#creates the smartsheet for ETS Tradeshow Map in the TechX workspace
def create_sheet(name):
    sheet_spec = smartsheet.models.Sheet({
    'name': name,
    'columns': [{
        'title': 'Show Name',
        'primary': True,
        'type': 'CHECKBOX',
        'symbol': 'STAR'
        }, {
        'title': 'Setup Start Date',
        'type': 'CHECKBOX',
        'symbol': 'STAR'
        }, {
        'title': 'Show Live Date',
        'type': 'TEXT_NUMBER'
        }, {
        'title': 'Tear Down Date',
        'type': 'TEXT_NUMBER'
        }, {
        'title': 'Program Manager',
        'type': 'TEXT_NUMBER'
        }, {
        'title': 'Venue Name',
        'type': 'TEXT_NUMBER'
        }, {
        'title': 'Location',
        'type': 'TEXT_NUMBER'
        }, {
        'title': 'Booth Size',
        'type': 'TEXT_NUMBER'
        }]
    })
    response = smart.Home.create_sheet(sheet_spec)
    return response.result.id


#implement fiscal year separations per Cisco calendar

#sort additions by 'Show Live' date

#on click transfer of new row/information of a show, 
# check if checbox is clicked (means show=requested)

if __name__ == '__main__':
    my_sheet = create_sheet('VLAN Example')