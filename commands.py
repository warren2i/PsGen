import base64


def cd ( directory ):
    """Sets the current working location to a specified location."""
    return ("cd" + " " + directory)


def chdir ( directory ):
    """Sets the current working location to a specified location."""
    return ("cd" + " " + directory)


def copyfile ( fromloc, toloc ):
    """Copies an item from one location to another. Usage copy('c://file.txt', 'c://toloc') copy('c://folder', 'c://newfolder')"""
    return ("Copy-Item" + " " + fromloc + " " + toloc)


def erase ( target ):
    """Deletes files and folders. Usage erase('c:/file.txt') erase('c:/folder')"""
    return ("Remove-Item" + " " + target)


def curl ( url ):
    """Gets content from a webpage on the Internet."""
    return ("curl" + " " + url)


def InvokeWebRequest ( url ):
    return ("Invoke-WebRequest" + " " + url)


def decodecommand ( command ):
    """decodes a encoded powershell command"""
    return base64.b64decode(command).decode('UTF-16LE')


def encodecommand ( command ):
    """encodes a powershell command"""
    return (base64.b64encode(command.encode("UTF-16LE", "ignore"))).decode('utf-8')


def b64encodestr ( command ):
    """encodes commands in base64 example command = "dir c:\" = ZABpAHIAIABjADoAXAA="""
    return ('[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes(' + '"' + command + '"' + '))')


def b64decodestr ( command ):
    """decodes commands from base64 example = ZABpAHIAIABjADoAXAA= = 'dir c:\'"""
    return (
            '[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(' + '"' + command + '"' + '))')


def b64encodete ( text ):
    """encodeds text in base64"""
    return ('[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes(' + '"' + text + '"' + '))')


def b64decodete ( text ):
    """decodes base64 text"""
    return ('[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String(' + '"' + text + '"' + '))')


def runenccommand ( enc ):
    """runs encoded commands in powershell
    Useage example // runenccommand(encodecommand('ping google.com')) to generate // powershell -E cABpAG4AZwAgAGcAbwBvAGcAbABlAC4AYwBvAG0A
    """
    return ('powershell -E ' + enc + '')


def ping ( url ):
    return ('ping ' + url)


def getfile ( url, toloc ):
    """download file to location
    Usage exmaple // getfile('https://i.imgur.com/P0Qa9QS.jpeg','C:/temp/test2.jpg') to generate // Invoke - WebRequest https://i.imgur.com/P0Qa9QS.jpeg - OutFile C:/temp/test2.jpg
    """
    return ('Invoke-WebRequest ' + url + ' -OutFile ' + toloc)


def StartProcess ( proc ):
    """
Starts one or more processes on the local computer.
Usage Example // StartProcess('calc.exe')"""
    return ('Start-Process ' + proc)


def Createnewuser ( Name, Pass ):
    """creates new local windows user"""
    return ('New-LocalUser -Name ' + Name + ' -Password (ConvertTo-SecureString "' + Pass + '" -AsPlainText -Force)')


def setdate ( date ):
    """changes windows date format must be 01/01/2022"""
    return ('Set-Date -Date ' + date)


def schedprocess ( name, proc, when ):
    """https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtask?view=windowsserver2022-ps
    name = schedule task name
    proc = process name ie calc.exe
    when = -At <DateTime>,-AtLogOn, -AtStartup, -Daily, -DaysInterval [<Int32>], -Once, -RandomDelay [num],

    idle info The Task Scheduler service will check if the computer is in an idle state every 15 minutes. A computer is considered to be in an idle state when a screen saver is running. If a screen saver is not running, then the computer is considered to be in an idle state if there is 0% CPU usage and 0% disk input or output for 90% of the past fifteen minutes and if there is no keyboard or mouse input during this period of time. Once the Task Scheduler service detects that the computer is in an idle state, the service only waits for user input to mark the end of the idle state.
    """
    return (
            'Register-ScheduledTask ' + name + ' -InputObject (New-ScheduledTask -Action (New-ScheduledTaskAction -Execute "' + proc + '") -Trigger (New-ScheduledTaskTrigger -At ' + when + ' -Once) -Settings (New-ScheduledTaskSettingsSet))')
