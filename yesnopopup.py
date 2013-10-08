from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class AskPopup(Popup):
    def __init__(self, content_class, title, text, callback, **kwargs):
        # self.size_hint = (0.4, 0.4)
        content = content_class(text)
        content.bind(on_answer=callback)
        content.bind(on_answer=self.dismiss)
        kwargs['content'] = content
        kwargs['auto_dismiss'] = False
        kwargs['title'] = title
        super(AskPopup, self).__init__(**kwargs)


class AskContent(BoxLayout):
    text = StringProperty('')

    def __init__(self, text, **kwargs):
        self.text = text
        self.register_event_type('on_answer')
        super(AskContent, self).__init__(**kwargs)

    def on_answer(self, *args):
        pass


class YesNoContent(AskContent):
    pass


class YesNoPopup(AskPopup):
    def __init__(self, title, text, callback, **kwargs):
        super(YesNoPopup, self).__init__(YesNoContent, title, text, callback, **kwargs)


class YesNoQuitContent(AskContent):
    pass


class YesNoQuitPopup(AskPopup):
    def __init__(self, title, text, callback, **kwargs):
        super(YesNoQuitPopup, self).__init__(YesNoQuitContent, title, text, callback, **kwargs)


class StringContent(AskContent):
    pass


class StringPopup(AskPopup):
    def __init__(self, title, text, callback, **kwargs):
        super(StringPopup, self).__init__(StringContent, title, text, callback, **kwargs)
