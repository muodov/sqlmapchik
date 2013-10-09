#!/usr/bin/env python

"""
Copyright (c) 2013 muodov (muodov[monkey]gmail.com)
"""

from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty, StringProperty
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
import thread
from functools import partial

import sys
from Queue import Queue
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sqlmap'))
import chik_init_settings
import chik_hook


FORBIDDEN_FLAGS = [
    '--update',
    '--beep',
    '--udf-inject',
    '--shared-lib',
    '--os-pwn',
    '--os-smbrelay',
    '--os-bof',
    '--priv-esc',
    '--msf-path',
    '--tmp-path',
    '--alert',
    '--threads'
    ]


def doit():
    """start sqlmap"""
    import time
    Logger.debug(time.ctime())
    Logger.debug('importing sqlmap')
    import sqlmap
    Logger.debug('imported sqlmap')
    from lib.core.data import (
        paths,
        cmdLineOptions,
        mergedOptions,
        conf,
        kb,
        queries
        )

    # force sqlmap config reinitialization
    Logger.debug('clearing config...')

    # sqlmap paths
    paths.clear()
    # object to store original command line options
    cmdLineOptions.clear()
    # object to store merged options (command line, configuration file and default options)
    mergedOptions.clear()
    # object to share within function and classes command
    # line options and settings
    conf.clear()
    # object to share within function and classes results
    kb.clear()
    # object with each database management system specific queries
    queries.clear()
    Logger.debug('starting sqlmap')
    try:
        sqlmap.main()
    finally:
        App.get_running_app().running = False


class FileChooseButton(Button):
    pass


class UrlDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class TargetDialog(BoxLayout):

    def set_target(self, target_type, filename):
        app = App.get_running_app()
        app.target_type = target_type
        app.target = filename[0] if isinstance(filename, list) else filename
        self._dialog.dismiss()
        app.root._target_dialog.dismiss()
        app.main()

    def cancel_load(self):
        self._dialog.dismiss()

    def url_dialog(self):
        self._dialog = Popup(
            title='Enter URL',
            content=UrlDialog(
                load=partial(self.set_target, 'URL'),
                cancel=self.cancel_load
                )
            )
        self._dialog.open()

    def log_dialog(self):
        self._dialog = Popup(
            title='Choose a file',
            content=LoadDialog(
                load=partial(self.set_target, 'logfile'),
                cancel=self.cancel_load
                )
            )
        self._dialog.open()

    def bulk_dialog(self):
        self._dialog = Popup(
            title='Choose a file',
            content=LoadDialog(
                load=partial(self.set_target, 'bulkfile'),
                cancel=self.cancel_load
                )
            )
        self._dialog.open()

    def request_dialog(self):
        self._dialog = Popup(
            title='Choose a file',
            content=LoadDialog(
                load=partial(self.set_target, 'request file'),
                cancel=self.cancel_load
                )
            )
        self._dialog.open()

    def ini_dialog(self):
        self._dialog = Popup(
            title='Choose a file',
            content=LoadDialog(
                load=partial(self.set_target, 'INI config'),
                cancel=self.cancel_load
                )
            )
        self._dialog.open()


class Sqlmapchik(BoxLayout):
    manager = ObjectProperty()
    menu_screen = ObjectProperty()
    log_screen = ObjectProperty()
    current_target_widget = ObjectProperty(None)
    _target_dialog = ObjectProperty()
    log_widget = ObjectProperty()
    log_buffer = ObjectProperty(Queue())

    def update_log(self, dt):
        i = 0
        buff = ''
        while not self.log_buffer.empty() and i < 20:
            buff += self.log_buffer.get() + '\n'
            i += 1
        self.log_widget.text += buff

    def launch_dialog(self):
        self._target_dialog = Popup(title="Choose target type", content=TargetDialog())
        self._target_dialog.open()

    def on_current_target_widget(self, instance, value):
        anim = Animation(pos_hint={'y': 0}, d=0.2)
        anim.start(value)


def switch_to_menu(*args, **kwargs):
    App.get_running_app().root.manager.current = 'menu'


class SqlmapchikApp(App):

    use_kivy_settings = False
    current_settings = ListProperty()
    target_type = StringProperty('URL')
    target = ObjectProperty(None)
    running = BooleanProperty(False)

    def on_running(self, instance, value):
        print 'on_running', instance, value
        if not value:
            self.root.log_screen.add_widget(self.menu_button)
        else:
            pass

    def on_target(self, instance, value):
        self.construct_argv()

    def _construct_argv_section(self, section):
        result = []
        for flag, value in self.config.items(section):
            if value and value != 'False':
                if len(flag) > 1:
                    val = '--' + flag
                    if value != 'True':
                        val += '=' + value
                    result.append(val)
                else:
                    result.append('-' + flag)
                    if value != 'True':
                        result.append(value)
        return result

    def construct_argv(self):
        result = []
        # target
        if self.target_type == 'URL':
            result.append('-u')
        elif self.target_type == 'logfile':
            result.append('-l')
        elif self.target_type == 'bulkfile':
            result.append('-m')
        elif self.target_type == 'request file':
            result.append('-r')
        elif self.target_type == 'INI config':
            result.append('-c')
        result.append(self.target)

        # config sections
        result += self._construct_argv_section('General')
        result += self._construct_argv_section('Request options')
        result += self._construct_argv_section('Optimization')
        result += self._construct_argv_section('Injection')
        result += self._construct_argv_section('Detection')
        result += self._construct_argv_section('Techniques')
        result += self._construct_argv_section('Fingerprint, Enumeration and Bruteforce')
        result += self._construct_argv_section('File system and OS')
        result += self._construct_argv_section('Miscellaneous')

        self.current_settings = result

    def build(self):
        self.menu_button = Button(text='Back to menu', size_hint=(1, 0.1), on_press=switch_to_menu)
        root = Sqlmapchik()
        Clock.schedule_interval(root.update_log, 0.1)
        return root

    def _strip_forbidden_args(self, flaglist):
        for forbidden in FORBIDDEN_FLAGS:
            while forbidden in flaglist:
                if forbidden.startswith('--'):
                    flaglist.remove(forbidden)
                else:
                    #TODO: intelligently strip short arguments
                    pass
                self.root.log_buffer.put('Sorry, %s flag is not supported in sqlmapchik. Ignoring.' % forbidden)

    def main(self, additional_flags=''):
        """
        Main function of sqlmap when running from command line.
        """

        if additional_flags:
            pass
        else:
            sys.argv = [sys.argv[0], '--disable-col'] + self.current_settings
        import time
        Logger.warning('starting at %s' % time.ctime())
        self.root.log_screen.remove_widget(self.menu_button)
        self.root.manager.current = 'log'
        self.running = True
        thread.start_new_thread(doit, ())

    def build_config(self, config):
        chik_init_settings.init_defaults(config)

    def on_start(self):
        # self.config.set('kivy', 'keyboard_mode', 'dock')
        self.construct_argv()

    def build_settings(self, settings):
        settings.add_json_panel('General', self.config, 'chik_res/settings_general.json')
        settings.add_json_panel('Request options', self.config, 'chik_res/settings_request_options.json')
        settings.add_json_panel('Optimization', self.config, 'chik_res/settings_optimization.json')
        settings.add_json_panel('Injection', self.config, 'chik_res/settings_injection.json')
        settings.add_json_panel('Detection', self.config, 'chik_res/settings_detection.json')
        settings.add_json_panel('Techniques', self.config, 'chik_res/settings_techniques.json')
        settings.add_json_panel('Fingerprint, Enumeration and Bruteforce', self.config, 'chik_res/settings_enumeration.json')
        settings.add_json_panel('File system and OS', self.config, 'chik_res/settings_file_system_access.json')
        settings.add_json_panel('Miscellaneous', self.config, 'chik_res/settings_miscellaneous.json')
        super(SqlmapchikApp, self).build_settings(settings)

    def on_config_change(self, config, section, key, value):
        Logger.debug('config changed: %s.%s = %s' % (section, key, value))
        self.construct_argv()

    def on_pause(self):
        return True

    def on_resume(self):
        return True


class ButtonWithDisable(Button):
    activeColor = ListProperty([1, 1, 1, 1])
    inactiveColor = ListProperty([2, .5, .5, 1])
    active = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super(ButtonWithDisable, self).__init__(*args, **kwargs)
        self.color = self.activeColor

    def on_active(self, who, what):
        if (what):
            self.color = self.activeColor
        else:
            self.color = self.inactiveColor

    def on_touch_down(self, touch):
        if (self.active):
            return super(ButtonWithDisable, self).on_touch_down(touch)


if __name__ == '__main__':
    SqlmapchikApp().run()
