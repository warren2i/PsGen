# PsGen

Powershell script generation from the browser.

The scope of this tool is to enable novice users to generate complex powershell scripting without prior knowledge.

![alt text](https://github.com/warren2i/PsGen/blob/master/Screenshots/2022-01-06%2019_15_45-Line%20logging.png?raw=true)

Install guide.

git clone https://github.com/warren2i/PsGen

cd PsGen

pip -r requirements.txt

To run -->

flask run

visit  http://127.0.0.1:5000/ in browser

TODO ------>

Date format change to suit pshell schema dd/mm/yyyy

change

Port across powershell commands

DONE ------>

Bootstrap

Javascrip onclick events

embed github logo in header using svg help page

All generated forms in macros.html are displayed and must be removed before building a script, this page should be empty
when first viewed.

Dev notes ------>

Encoding switch case

    def encode(line, val2encode):
        if line['encoding'] is not True:
            #dont encode
            return (val2encode)
        else:
            #encode
            return (runenccommand(encodecommand(val2encode)))

    
    
    if line['command_name'] == 'Createnewuser':
        result = encode(line,Createnewuser(line['userName'], line['password']))
        line['psline'] = result