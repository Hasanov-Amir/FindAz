from io import BytesIO


def check_file_size(file):
    with BytesIO() as output:
        file.save(output)
        size = output.getbuffer().nbytes
        file.seek(0)
    return size
