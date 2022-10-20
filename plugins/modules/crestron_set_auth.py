#!/usr/bin/python
from ansible.module_utils.basic import *
import ansible_collections.ansible_crestron.ansible_crestron.module_utils.crestron as crestron

def main():
    args = crestron.basic_arg_spec.copy()
    args.update({
        "enabled": {"type": "bool", "required": True},
        "new_username": {"type": "str"},
        "new_password": {"type": "str"}
    })

    mod = AnsibleModule(argument_spec=args)

    try:
        # Get ssh client for crestron panel
        p = crestron.get_client(
            hostname=mod.params.get("hostname"),
            username=mod.params.get("username"),
            password=mod.params.get("password")
        )
        # Execute command
        r = crestron.set_auth(
            enable=mod.params.get("enabled"),
            username=mod.params.get("new_username"),
            password=mod.params.get("new_password"),
            p=p
        )
        # Close client
        p.close()

        # Out
        mod.exit_json(changed=True, meta=r)

    except Exception as err:
        mod.fail_json(msg=err.message)

if __name__ == '__main__':
    main()