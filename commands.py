def schedprocess ( name, proc, when ):
    """https://docs.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtask?view=windowsserver2022-ps
    name = schedule task name
    proc = process name ie calc.exe
    when = -At <DateTime>,-AtLogOn, -AtStartup, -Daily, -DaysInterval [<Int32>], -Once, -RandomDelay [num],

    idle info The Task Scheduler service will check if the computer is in an idle state every 15 minutes. A computer is considered to be in an idle state when a screen saver is running. If a screen saver is not running, then the computer is considered to be in an idle state if there is 0% CPU usage and 0% disk input or output for 90% of the past fifteen minutes and if there is no keyboard or mouse input during this period of time. Once the Task Scheduler service detects that the computer is in an idle state, the service only waits for user input to mark the end of the idle state.
    """
    return (
            'Register-ScheduledTask ' + name + ' -InputObject (New-ScheduledTask -Action (New-ScheduledTaskAction -Execute "' + proc + '") -Trigger (New-ScheduledTaskTrigger -At ' + when + ' -Once) -Settings (New-ScheduledTaskSettingsSet))')


def runenccommand ( enc ):
    """runs encoded commands in powershell
    Useage example // runenccommand(encodecommand('ping google.com')) to generate // powershell -E cABpAG4AZwAgAGcAbwBvAGcAbABlAC4AYwBvAG0A
    """
    return ("powershell -E '" + enc + "'")


def encodecommand ( command ):
    """encodes a powershell command"""
    return (base64.b64encode(command.encode("UTF-16LE", "ignore"))).decode('utf-8')
