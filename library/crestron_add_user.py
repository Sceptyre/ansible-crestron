#!/usr/bin/python
from ansible.module_utils.basic import *
import ansible.module_utils.crestron as crestron

def main():
    args = crestron.basic_arg_spec.copy()
    args.update({
        "new_username": {"type": "str", "required": True},
        "new_password": {"type": "str", "required": True}
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
        r = crestron.add_user(
            username=mod.params.get("new_username"),
            password=mod.params.get("new_password"),
            p=p
        )
        # Close client
        p.close()

        # Out
        mod.exit_json(changed=True, meta=r)

    except Exception as err:
        mod.fail_json(err.message)

if __name__ == '__main__':
    main()