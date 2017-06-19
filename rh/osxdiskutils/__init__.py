# Copyright (c) 2017 Ranger Harke
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from ctypes import cast

import rh.osx.basetypes as bt
import rh.osx.corefoundation as cf
import rh.osx.diskarbitration as da
import rh.osx.iokit as io

def find_devices(device_class):
    device_iterator = io.io_iterator_t().autorelease()
    master_port = bt.mach_port_t()
    io.IOMasterPort(bt.MACH_PORT_NULL, master_port)
    classes_to_match = io.IOServiceMatching(device_class)
    # NB: consumes classes_to_match
    io.IOServiceGetMatchingServices(master_port, classes_to_match, device_iterator)
    device_iterator.object_type = io.io_registry_entry_t
    return io.IOIterator(device_iterator)

def find_block_devices():
    return find_devices(io.kIOBlockStorageDeviceClass)

def find_cd_block_devices():
    return find_devices(io.kIOCDBlockStorageDeviceClass)

def find_media(block_device):
    children_iterator = io.io_iterator_t().autorelease()
    io.IORegistryEntryCreateIterator(block_device, io.kIOServicePlane,
        io.kIORegistryIterateRecursively, children_iterator)
    return io.IOIterator(children_iterator, lambda x: io.IOObjectConformsTo(x, io.kIOMediaClass))

def get_bsd_name(media):
    return str(cast(io.IORegistryEntryCreateCFProperty(
        media, io.kIOBSDNameKey, cf.kCFAllocatorDefault, 0), cf.CFStringRef).autorelease())

def get_mount_point(bsd_name):
    # DADiskCreateFromBSDName does not take an encoding;
    # all BSD names are assumed to be ASCII
    path = ('/dev/' + bsd_name).encode('ascii')
    session = da.DASessionCreate(cf.kCFAllocatorDefault).autorelease()
    disk = da.DADiskCreateFromBSDName(cf.kCFAllocatorDefault, session, path).autorelease()
    if not disk: return None
    desc = da.DADiskCopyDescription(disk).autorelease()
    if not desc: return None
    volume_path = cast(cf.CFDictionaryGetValue(
        desc, da.kDADiskDescriptionVolumePathKey), cf.CFURLRef)
    if not volume_path: return None
    return str(cf.CFURLCopyFileSystemPath(volume_path, cf.kCFURLPOSIXPathStyle).autorelease())
