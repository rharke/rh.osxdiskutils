Utilities to work with disks on macOS

Specifics
=========

This library provides some functions for working with disks and mountpoints on macOS. It can
enumerate block devices and look up the mount points for attached media.

The code is tested with Python 2.7 and 3.6.

Requirements
============

My macOS API binding library ``rh.osx`` is required.

Examples
========

    >>> import rh.osxdiskutils
    >>> all_drives = rh.osxdiskutils.find_block_devices()
    >>> for drive in all_drives:
    ...     all_media = rh.osxdiskutils.find_media(drive)
    ...     for media in all_media:
    ...         bsd_name = rh.osxdiskutils.get_bsd_name(media)
    ...         mount_point = rh.osxdiskutils.get_mount_point(bsd_name)
    ...         if mount_point:
    ...             print(bsd_name, mount_point)
    ...
    disk1 /
    disk6 /Volumes/Storage
    disk8 /Volumes/Storage2
    disk7 /Volumes/Storage3

License
=======

This library is distributed under the MIT license, as described in the LICENSE file.
