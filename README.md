# sceptyre.ansible_crestron
This is an Ansible Collection built for managing crestron devices

---
## Authentication
All modules use the following variables for authentication
| Variable  | Type      |
| ---       | ---       |
| hostname  | string    |
| username  | string    |
| password  | string    |

## Modules
### sceptyre.ansible_crestron.add_user
Add User to Device
| Variable      | Type      |
| ---           | ---       |
| new_username  | string    |
| new_password  | string    |

### sceptyre.ansible_crestron.au_enable
Enable/Disable Auto Update
| Variable      | Type      |
| ---           | ---       |
| enabled       | bool      |


### sceptyre.ansible_crestron.au_time
Set Auto Update Time
| Variable      | Type      |
| ---           | ---       |
| time          | string    |