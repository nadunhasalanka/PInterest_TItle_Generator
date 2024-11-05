

def writing(project_folder, mode):
    from modules.writer import Writer


    table_id = '' 
    # go to README.md to see how to set up the google sheet and get the table id
    
    writer = Writer(project_folder)

    data = writer.open_data(mode, google_sheet=True, table_id=table_id)

    for row in data:
        writer.write(row, mode)



if __name__ == '__main__':
    project_name = 'Keto'

    writer_mode = 'image'
    writing(project_name, writer_mode)
