# Ansible role `tftp`

An Ansible role for installing a TFTP (Trivial File Transfer Protocol) server on RHEL/CentOS 7. Specifically, the responsibilities of this role are to:

- install the necessary packages
- manage the configuration
- manage SELinux settings

For more relevant documentation on TFTP, see:

- [`tftpd(8)` man page](http://linuxmanpages.net/manpages/fedora21/man8/tftpd.8.html)
- [`tftp_selinux(8)` man page](http://linuxmanpages.net/manpages/fedora21/man8/tftpd_selinux.8.html)

## Requirements

- SELinux is expected to be enabled.

## Role Variables

The following variables can be set by the administrator:

| Variable                      | Default             | Comments (type)                                                      |
| :---                          | :---                | :---                                                                 |
| `tftp_root_directory`         | `/var/lib/tftpboot` | The path to the root directory served by TFTP.                       |
| `tftp_server_args`            | `--secure`          | Arguments to be passed to the server (except root directory)         |
|                               |                     | See the `tftpd` man page for details                                 |
| `tftp_server_foreman_support` | false               | Enable Foreman support by creating suitable tftpd.map                |
| `tftp_setype`                 | `tftpdir_rw_t`      | Default SELinux context for the root directory.                      |
|                               |                     | Set to `public_content_rw_t` to allow access through other services  |
| `tftp_anon_write`             | no                  | When set to "yes", `tftp` can modify public files.                   |
| `tftp_home_dir`               | no                  | When set to "yes", `tftp` can modify files in user home directories. |

The following variables usually should be left alone:

| Variable           | Default              | Comments (type)                           |
| :---               | :---                 | :---                                      |
| `tftp_cps`         | 100 2                |                                           |
| `tftp_disable`     | no                   | When set to 'yes', TFTP will be disabled. |
| `tftp_flags`       | IPv4                 |                                           |
| `tftp_group`       | root                 | Group of `tftp_root_directory`            |
| `tftp_mode`        | 0755                 | Permissions of `tftp_root_directory`      |
| `tftp_per_source`  | 11                   |                                           |
| `tftp_protocol`    | udp                  |                                           |
| `tftp_server`      | `/usr/sbin/in.tftpd` |                                           |
| `tftp_socket_type` | dgram                |                                           |
| `tftp_user`        | root                 |                                           |
| `tftp_wait`        | yes                  |                                           |

## Dependencies

No dependencies.

## Example Playbook

See the [test playbook](tests/test.yml)

## Testing

Tests for this role are provided in the form of a Vagrant environment that is kept in a separate branch, [tests](https://github.com/bertvv/ansible-role-tftp/tree/tests). I use [git-worktree(1)](https://git-scm.com/docs/git-worktree) to include the test code into the working directory. Instructions for running the tests:

1. Fetch the tests branch: `git fetch origin tests`
2. Create a Git worktree for the test code: `git worktree add tests tests` (remark: this requires at least Git v2.5.0). This will create a directory `tests/`.
3. `cd tests/`
4. `vagrant up` will then create a VM and apply the second of the two available testing playbooks enumerated below.

The test playbooks:

- [`test-minimal.yml`](https://github.com/bertvv/ansible-role-tftp/blob/tests/test-minimal.yml) applies the role to a VM, with default settings (no role variables are set).
- [`test.yml`](https://github.com/bertvv/ansible-role-tftp/blob/tests/test.yml) applies the role to a VM, changing some default values. The playbook also puts a file named README into the TFTP root directory. After applying this playbook, you should be able to fetch that file from your host system (assuming the `tftp` client is installed):

    ```ShellSession
    $ tftp 127.0.0.1 6969 -c get README
    ```

The TFTP port (69) on the VM is forwarded through the NAT interface to port 6969 on your host system, hence the 127.0.0.1 and port number in the command line.

You may want to change the base box into one that you like. The current one, [bertvv/centos71](https://atlas.hashicorp.com/bertvv/boxes/centos71) was generated using a Packer template from the [Boxcutter project](https://github.com/boxcutter/centos) with a few modifications.

## Contributing

Issues, feature requests, ideas are appreciated and can be posted in the Issues section. Pull requests are also very welcome. Preferably, create a topic branch and when submitting, squash your commits into one (with a descriptive message).

## License

BSD

## Author Information

Bert Van Vreckem (bert.vanvreckem@gmail.com)

Contributions by:

- [@kostyrevaa ](https://github.com/kostyrevaa): Foreman support (v1.2.0)
