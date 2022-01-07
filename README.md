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

**HOW TO USE**

****

**Click the dropdown box to select a command**

**Click 'Generate command'**

The command will be added below.

Enter values into fields & select required arguments.

Repeat this line by line until you have built your script.

Click Generate to create your Pshell script.

![alt text](https://github.com/warren2i/PsGen/blob/master/Screenshots/generating_script.png?raw=true)

****

**Click 'Select PowerShell Script'**

**Select the script you just made**

![alt text](https://github.com/warren2i/PsGen/blob/master/Screenshots/select_script.png?raw=true)

****

![alt text](https://github.com/warren2i/PsGen/blob/master/Screenshots/psscrip.png?raw=true)

****

TODO ------>

copy to clipboard line by line option

Port across powershell commands

DONE ------>

Date format change to suit pshell schema dd/mm/yyyy

Added copy to clipboard function to scripts page

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