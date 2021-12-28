#!/usr/bin/python3 -d

# Copyright (C) 2021 Johannes Findeisen <you@hanez.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from gi.repository import AppIndicator3
from gi.repository import Notify

import os
import json
import signal
import subprocess
import time
import urllib.request
import xmltodict

from pathlib import Path
from threading import Thread


APP_VERSION = '0.0.1'
APPINDICATOR_ID = 'fritztray'


def get_state_icon(state):
    """
    Look up the state msg and return the icon name.
    """
    install_path = '/usr/share/icons/hicolor/scalable/status'
    icon_name = 'network-fritz-connected-symbolic.svg'

    fallback_dict = {
        'CONNECTED': 'network-vpn-symbolic',
        'WAITING': 'network-vpn-no-route-symbolic',
        'CONFIG': 'network-vpn-acquiring-symbolic',
        'ERROR': 'network-error-symbolic',
        'STARTING': 'network-vpn-acquiring-symbolic',
        'UPGRADE': 'network-offline-symbolic',
        'NONE': 'network-offline-symbolic'
    }

    fritztray_dict = {
        'CONNECTED': 'network-freepn-connected-key2-symbolic',
        'WAITING': 'network-freepn-no-route-symbolic',
        'CONFIG': 'network-freepn-acquiring-symbolic',
        'ERROR': 'network-freepn-error-symbolic',
        'STARTING': 'network-freepn-acquiring-symbolic',
        'UPGRADE': 'network-freepn-offline-symbolic',
        'NONE': 'network-freepn-offline-symbolic'
    }

    state_dict = fritztray_dict
    connected_icon = Path(install_path).joinpath(icon_name)
    if not connected_icon.exists():
        state_dict = fallback_dict

    return state_dict.get(state, state_dict['NONE'])


def fetch_geoip():
    """
    Fetch location info from ubuntu.com geoip server and transform the
    xml payload to json.
    """
    request = urllib.request.Request('https://geoip.ubuntu.com/lookup')
    response = urllib.request.urlopen(request)
    payload = xmltodict.parse(response.read())
    return json.dumps(payload, indent=4, separators=(',', ': '))


class Indicator:
    def __init__(self):
        self.app_id = APPINDICATOR_ID
        icon_name = get_state_icon('NONE')
        self.indicator = AppIndicator3.Indicator.new(
            self.app_id,
            icon_name,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        # self.indicator.set_attention_icon_full('indicator-messages-new',
        #                                            'State update')
        self.indicator.set_menu(self.create_menu())
        # setup the state updater thread
        self.update = Thread(target=self.check_for_phone_state)
        self.update.daemon
        self.update.start()

    def check_for_phone_state(self):
        """
        Check for new state msg and update icon if new.
        """
        #old_state = 'NONE'
        #new_state = 'NONE'
        #guide = '999999999'

        #while True:
            #if state_file.exists():
            #    msg_queue = get_status(str(state_file))
            #    new_state = msg_queue.pop().strip()
            # if there is a change in state, update the icon
            #if old_state != new_state:
            #    if new_state == 'UPGRADE':
            #        Notify.Notification.new("Version Error!!", "Wuhhuuuuu", None).show()
            #    self.indicator.set_icon_full(get_state_icon(new_state), new_state)
            #    # Notify.Notification.new(new_state, None, None).show()
            #    # note the second label arg should be the longest possible label str
            #    self.indicator.set_label(new_state.format().center(9), guide)
            #old_state = new_state
            #time.sleep(1)

    def create_menu(self):
        menu = Gtk.Menu()

        #item_separator = Gtk.SeparatorMenuItem()
        #menu.append(item_separator)

        item_about = Gtk.MenuItem(label='About Fritz!Tray')
        item_about.connect('activate', self.about)
        menu.append(item_about)

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def about(self, source):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_name('About...')
        about_dialog.set_program_name('Fritz!Tray')
        about_dialog.set_version(APP_VERSION)
        about_dialog.set_copyright('© 2021 Johannes Findeisen')
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_logo_icon_name('fritztray')
        about_dialog.set_website('https://git.unixpeople.org/hanez/uplink')
        about_dialog.set_website_label('https://git.unixpeople.org/hanez/uplink')
        about_dialog.set_comments("""
Fritz!Box control and status tool.
                         """)
        about_dialog.set_authors(['Johannes Findeisen <you@hanez.org>'])
        about_dialog.set_artists(['Foo Bar <foo@example.com>'])
        about_dialog.run()
        about_dialog.hide()

    def quit(self, source):
        Notify.uninit()
        Gtk.main_quit()

def main():
    Indicator()
    Notify.init(APPINDICATOR_ID)
    Gtk.main()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
