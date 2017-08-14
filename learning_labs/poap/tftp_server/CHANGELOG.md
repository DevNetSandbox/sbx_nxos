# Change log

This file contains al notable changes to the tftp Ansible role.

This file adheres to the guidelines of [http://keepachangelog.com/](http://keepachangelog.com/). Versioning follows [Semantic Versioning](http://semver.org/).

## 1.2.1 - 2016-08-23

### Changed

- Fixed package selection, added `xinetd` (was broken in CentOS 7.2)
- Fixed Ansible 2.0 deprecation warnings and errors
- Prepared code to enable support of other Linux distributions
- Moved hard coded values in playbook into vars/

## 1.2.0 - 2015-08-15

### Added

- Support for setting up a TFTP server for use with Foreman (contributed by [@kostyrevaa](https://github.com/kostyrevaa)).

### Removed

- The client package `tftp` is no longer installed as part of this role.

## 1.1.0 - 2015-05-07

### Added

- The group and permissions of `tftp_root_directory` can now be set

## 1.0.0 - 2015-05-02

First release!

### Added

- Install TFTP
- Manage configuration
- Manage SELinux settings

