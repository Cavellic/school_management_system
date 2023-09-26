def handle_uploaded_file(f):
    with open('main/static/files/upload'+ f.name, 'wb+') as destinaton:
        for chunk in f.chunks():
            destination.write(chunk)