import paramiko

# For defining repetitive module arguments
basic_arg_spec = {
    "hostname": {"type": "string", "required": True},
    "username": {"type": "string", "required": True},
    "password": {"type": "string", "required": False}
}

# Utility function for standardizing command execution and handling
def _exec_and_validate(c,p):
    stdin, stdout, stderr = p.exec_command(c)
    out = " ".join(stdout.readlines())

    # Check for error
    if "ERROR:" in out:
        raise paramiko.SSHException("Error occured while executing command: " + c + " Error: " + out.split("ERROR: ")[1].split("\n")[0])

    return out

def _parse_response(r):
    pass

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

def sntp_server(server, p):
    return _exec_and_validate(
        c='SNTP SERVER:' + server,
        p=p
    )

def version(p):
    return _exec_and_validate(
        c="version",
        p=p
    )

def main():
    p = get_client("10.254.103.239" ,"crestron", "")
    print(version(p))

    p.close()

if __name__ == '__main__':
    main()