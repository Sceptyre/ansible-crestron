#!/usr/bin/python
from ansible.module_utils.basic import *
import ansible_collections.sceptyre.ansible_crestron.plugins.module_utils.crestron as crestron

def main():
    args = crestron.basic_arg_spec.copy()
    args.update({
        "time": {"type": "str", "required": True}
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
        r = crestron.au_time(
            time=mod.params.get("time"),
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