# setup.py
#
# Copyright (C) 2007 Andrew Resch ('andar') <andrewresch@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages, Extension
from distutils import cmd 
from distutils.command.build import build as _build
from distutils.command.install import install as _install
from distutils.command.install_data import install_data as _install_data
import msgfmt


import platform
import glob
import os

python_version = platform.python_version()[0:3]

# The libtorrent extension
_extra_compile_args = [
    "-Wno-missing-braces",
    "-DHAVE_INCLUDE_LIBTORRENT_ASIO____ASIO_HPP=1", 
    "-DHAVE_INCLUDE_LIBTORRENT_ASIO_SSL_STREAM_HPP=1", 
    "-DHAVE_INCLUDE_LIBTORRENT_ASIO_IP_TCP_HPP=1", 
    "-DHAVE_PTHREAD=1",
    "-DTORRENT_USE_OPENSSL=1",
    "-DHAVE_SSL=1"
]

_include_dirs = [
    './libtorrent',
    './libtorrent/include',
    './libtorrent/include/libtorrent',
    '/usr/include/python' + python_version
]
                        
_libraries = [
    'boost_filesystem',
    'boost_date_time',
    'boost_thread',
    'boost_python',
    'z',
    'pthread',
    'ssl'
]
			
_sources = glob.glob("./libtorrent/src/*.cpp") + \
                        glob.glob("./libtorrent/src/kademlia/*.cpp") + \
                        glob.glob("./libtorrent/bindings/python/src/*.cpp")

# Remove file_win.cpp as it is only for Windows builds
for source in _sources:
    if "file_win.cpp" in source:
        _sources.remove(source)
        break

libtorrent = Extension(
    'libtorrent',
    include_dirs = _include_dirs,
    libraries = _libraries,
    extra_compile_args = _extra_compile_args,
    sources = _sources
)

class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        po_dir = os.path.join(os.path.dirname(__file__), 'deluge/i18n/')
        for path, names, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:len(f) - 3]
                    src = os.path.join(path, f)
                    dest_path = os.path.join('deluge', 'i18n', lang, \
                        'LC_MESSAGES')
                    dest = os.path.join(dest_path, 'deluge.mo')
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        print 'Compiling %s' % src
                        msgfmt.make(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            print 'Compiling %s' % src
                            msgfmt.make(src, dest)

class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]
    def run(self):
        _build.run(self)

class install_data(_install_data):
    def run(self):
        _install_data.run(self)

cmdclass = {
    'build': build,
    'build_trans': build_trans,
    'install_data': install_data
}

# Build the plugin eggs
for path in glob.glob('deluge/plugins/*'):
    print path + "/setup.py"
    os.system("cd " + path + "&& python setup.py bdist_egg -d ..")

# Main setup

setup(
    name = "deluge",
    fullname = "Deluge Bittorent Client",
    version = "0.6.0.0",
    author = "Andrew Resch, Marcos Pinto",
    author_email = "andrewresch@gmail.com, markybob@dipconsultants.com",
    description = "GTK+ bittorrent client",
    url = "http://deluge-torrent.org",
    license = "GPLv2",
    include_package_data = True,
    package_data = {"deluge": ["ui/gtkui/glade/*.glade", 
                                "data/pixmaps/*.png",
                                "data/pixmaps/logo.svg",
                                "plugins/*.egg",
                                "i18n/*.pot",
                                "i18n/*/LC_MESSAGES/*.mo"]},
    data_files = [('/usr/share/deluge/icons/scalable/apps', [
                         'deluge/data/icons/scalable/apps/deluge.svg']),
                ('/usr/share/icons/hicolor/128x128/apps', [
                        'deluge/data/icons/hicolor/128x128/apps/deluge.png']),
                ('/usr/share/icons/hicolor/16x16/apps', [
                        'deluge/data/icons/hicolor/16x16/apps/deluge.png']),
                ('/usr/share/icons/hicolor/192x192/apps', [
                        'deluge/data/icons/hicolor/192x192/apps/deluge.png']),
                ('/usr/share/icons/hicolor/22x22/apps', [
                        'deluge/data/icons/hicolor/22x22/apps/deluge.png']),
                ('/usr/share/icons/hicolor/24x24/apps', [
                        'deluge/data/icons/hicolor/24x24/apps/deluge.png']),
                ('/usr/share/icons/hicolor/256x256/apps', [
                        'deluge/data/icons/hicolor/256x256/apps/deluge.png']),
                ('/usr/share/icons/hicolor/32x32/apps', [
                        'deluge/data/icons/hicolor/32x32/apps/deluge.png']),
                ('/usr/share/icons/hicolor/36x36/apps', [
                        'deluge/data/icons/hicolor/36x36/apps/deluge.png']),
                ('/usr/share/icons/hicolor/48x48/apps', [
                        'deluge/data/icons/hicolor/48x48/apps/deluge.png']),
                ('/usr/share/icons/hicolor/64x64/apps', [
                        'deluge/data/icons/hicolor/64x64/apps/deluge.png']),
                ('/usr/share/icons/hicolor/72x72/apps', [
                        'deluge/data/icons/hicolor/72x72/apps/deluge.png']),
                ('/usr/share/icons/hicolor/96x96/apps', [
                        'deluge/data/icons/hicolor/96x96/apps/deluge.png']),
                ('/usr/share/applications', [
                        'deluge/data/share/applications/deluge.desktop'])],
    ext_package = "deluge",
    ext_modules = [libtorrent],
    packages = find_packages(exclude=["plugins"]),
    cmdclass=cmdclass,
    entry_points = """
        [console_scripts]
            deluge = deluge.main:main
            deluged = deluge.main:start_daemon
    """)
