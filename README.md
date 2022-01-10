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

**TODO ------>**

When powershell command is retreived from database all rich text formatting is lost, this prevents the script from
running when copied directly. options.... Hard code formatting prior to database submit, but this will require secondary
output to file or the strip the formatting tags for exportable versions of the scripts.

add tool tips to each field

copy to clipboard line by line option

Port across powershell commands

add PowerRemoteDesktop by DarkCoderSc, amazing work btw!

**Dev notes ------>**

How to Invoke encoded shell

`$var = 'encoded payload' $var2 = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($var))
Invoke-Expression $var2`

****

from wtforms.fields.html5 ##Seems to be depreciated... use this now. from wtforms.fields import TimeField

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