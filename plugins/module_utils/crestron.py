from time import sleep
import paramiko

# For defining repetitive module arguments
basic_arg_spec = {
    "hostname": {"type": "str", "required": True},
    "username": {"type": "str", "required": True},
    "password": {"type": "str", "required": False}
}

# Utility function for standardizing command execution and handling
def _exec_and_validate(c,p):
    stdin, stdout, stderr = p.exec_command(c)
    out = " ".join(stdout.readlines())

    # Check for error
    if "ERROR:" in out:
        raise paramiko.SSHException("Error occured while executing command: " + c + " Error: " + out.split("ERROR: ")[1].split("\n")[0])

    return out

# Creates a paramiko ssh client
def get_client(hostname, username, password, port = 22):
    # Init object
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect
    p.connect(
        hostname=hostname,
        username=username,
        password=password,
        port=port
    )

    # Return to function caller
    return p


#### Crestron Commands ####
def au_enable(enable, p):
    return _exec_and_validate(
        c='auenable ' + (lambda enable: "on" if enable else "off")(enable),
        p=p
    )

def au_time(time, p):
    return _exec_and_validate(
        c='autime ' + time,
        p=p
    )

def set_sntp_server(server, p):
    return _exec_and_validate(
        c='SNTP SERVER:' + server,
        p=p
    )

def set_auth(enable, username, password, p):
    # Create a shell/channel
    s = p.invoke_shell()
    sleep(.5)
    s.recv(9999)

    # Run command
    s.send("AUTHENTICATION " + (lambda enable: "on" if enable else "off")(enable) + "\n")
    sleep(.5)

    # If set to enable, fill out the prompt
    if enable:
        # Username:
        s.send(username + "\n")
        sleep(.5)
        s.recv(9999)

        # Enter + Validate Password:
        s.send(password + "\n")
        sleep(.5)
        s.recv(9999)

        s.send(password + "\n")
        sleep(10)

    # Check for errors
    out = str(s.recv(9999))
    s.close()
    
    if "ERROR: " in out:
        raise paramiko.SSHException("Error occured while enabling authentication: " + out.split("ERROR: ")[1].split("\n")[0])

    return out

def add_user(username, password, p):
    return _exec_and_validate(
        c="adduser -n:" + username + "-p:" + password,
        p=p
    )

def set_ssl(mode, p):
    return _exec_and_validate(
        c='SSL ' + mode,
        p=p
    )

def reboot(p):
    return _exec_and_validate(
        c="REBOOT",
        p=p
    )

def version(p):
    return _exec_and_validate(
        c="version",
        p=p
    )
