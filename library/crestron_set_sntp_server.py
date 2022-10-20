#!/usr/bin/python
from ansible.module_utils.basic import *
import ansible.module_utils.crestron as crestron

def main():
    mod = AnsibleModule(
        argument_spec={
            **crestron.basic_arg_spec,
            "server": {"type": "string", "required": True}
        }
    )

    try:
        # Get ssh client for crestron panel
        p = crestron.get_client(
            hostname=mod.params.get("hostname"),
            username=mod.params.get("username"),
            password=mod.params.get("password")
        )
        # Execute command
        r = crestron.set_sntp_server(
            server=mod.params.get("server"),
            p=p
        )
        # Close client
        p.close()

        # Out
        mod.exit_json(changed=True, meta=r)

    except Exception as err:
        mod.fail_json(err)

if __name__ == '__main__':
    main()