#!/usr/bin/env python

"""
Copyright (c) 2013 muodov (muodov[monkey]gmail.com)

Hook sqlmap's I/O and redirect transparently to Kivy widgets.
This file must be imported before any sqlmap imports.
"""

import threading
import logging
import os
import re
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from yesnopopup import YesNoPopup, YesNoQuitPopup, LogMessage


tlocal = threading.local()
tlocal.pending_question = 'If you see this, something went wrong'


# Hook version check
def customGetRevisionNumber():
    """
    slightly patched getRevisionNumber() without trying to execute `git` command
    """

    retVal = None
    filePath = None
    _ = os.path.join(os.path.dirname(__file__), 'sqlmap')

    while True:
        filePath = os.path.join(_, ".git", "HEAD")
        if os.path.exists(filePath):
            break
        else:
            filePath = None
            if _ == os.path.dirname(_):
                break
            else:
                _ = os.path.dirname(_)

    while True:
        if filePath and os.path.isfile(filePath):
            with open(filePath, "r") as f:
                content = f.read()
                filePath = None
                if content.startswith("ref: "):
                    filePath = os.path.join(_, ".git", content.replace("ref: ", "")).strip()
                else:
                    match = re.match(r"(?i)[0-9a-f]{32}", content)
                    retVal = match.group(0) if match else None
                    break
        else:
            break

    return retVal[:7] if retVal else None

import lib.core.revision
lib.core.revision.getRevisionNumber = customGetRevisionNumber


# Hook output
import lib.core.common

def print_on_ui_thread(value, dt):
    App.get_running_app().root.scrolled_window.add_widget(LogMessage(text=value))

def print_on_widget(value):
    Clock.schedule_once(partial(print_on_ui_thread, value.replace('\r', '')), 0.2)


def output_wrapper(data, forceOutput=False, bold=False, content_type=None, status=None):
    print_on_widget(data)

def clearConsoleLineStub(arg=None):
    pass

lib.core.common.dataToStdout = output_wrapper
lib.core.common.clearConsoleLine = clearConsoleLineStub

# Hook input
originalReadInput = lib.core.common.readInput

def readInputWrapper(message, default=None, checkBatch=True):
    tlocal.pending_question = message
    """
    possible question formats:

    [Y/n]
    [(S)kip current test/(e)nd detection phase/(n)ext parameter/(q)uit]
    [y/N]
    [(C)ontinue/(s)tring/(r)egex/(q)uit]
    please enter value for parameter 'string':

    [0] aalala
    [1] dldld
    [q] Quit

    [Y/n/q]
    Edit POST data [default: %s]%s:
    Edit GET data [default: %s]:

    orrect [%s (default)/%s]
    document root locations [Enter for None]:
    Please enter full target URL (-u):
    number of threads? [Enter for %d (current)]
    what is the back-end DBMS address? [%s]
    functions now? [Y/n/q]

    """
    res = originalReadInput(message, default, checkBatch)
    tlocal.pending_question = 'If you see this, something went wrong'
    print_on_widget('answer is %s' % res)
    return res

lib.core.common.readInput = readInputWrapper


def create_yesnopopup(title, question, callback, *args, **kwargs):
    popup = YesNoPopup(title, question, callback, auto_dismiss=False)
    popup.open()

def create_yesnoquitpopup(title, question, callback, *args, **kwargs):
    popup = YesNoQuitPopup(title, question, callback, auto_dismiss=False)
    popup.open()

def create_stringpopup(callback, *args, **kwargs):
    input_widget = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
    text_input = TextInput(text_hint='type here', multiline=False)
    input_widget.add_widget(text_input)
    enter_button = Button(text='Enter', size_hint=(None, 1), width=100)
    def close_input(instance):
        callback(instance, text_input.text)
        App.get_running_app().root.log_screen.remove_widget(input_widget)
    enter_button.bind(on_press=close_input)
    input_widget.add_widget(enter_button)
    App.get_running_app().root.log_screen.add_widget(input_widget)


# Hook raw_input for fancy user interaction
def user_interact(msg=''):
    lock = threading.Lock()
    lock.acquire()
    context = {}

    def my_callback(instance, answer):
        context['answer'] = answer
        lock.release()

    if 'pending_question' not in tlocal.__dict__:
        Clock.schedule_once(partial(create_stringpopup, my_callback), 0)
    elif '[y/n]' in tlocal.pending_question.lower():
        Clock.schedule_once(partial(create_yesnopopup, 'What next?', tlocal.pending_question, my_callback), 0)
    elif '[y/n/q]' in tlocal.pending_question.lower():
        Clock.schedule_once(partial(create_yesnoquitpopup, 'What next?', tlocal.pending_question, my_callback), 0)
    else:
        Clock.schedule_once(partial(create_stringpopup, my_callback), 0)

    lock.acquire()
    return context['answer']

import __builtin__
__builtin__.raw_input = user_interact


# Hook logs
class WidgetHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            print_on_widget(msg)
        except:
            self.handleError(record)

from lib.core.data import logger
widget_handler = WidgetHandler()
widget_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"))
# widget_handler.setLevel(logging.DEBUG)
logger.addHandler(widget_handler)


from kivy.logger import Logger
# disable os._exit to forbid exiting in multithreading mode
original_exit = os._exit
def exit_wrapper(status):
    Logger.warning('%s attempted to call os._exit(%d), ignoring' % (threading.current_thread().name, status))
os._exit = exit_wrapper
