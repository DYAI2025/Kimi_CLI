import types, sys
from unittest import mock

# Create dummy playsound module if not installed
sys.modules.setdefault('playsound', types.SimpleNamespace(playsound=lambda *a, **k: None))

from kimi_gui_modern import play_elevenlabs_tts

class DummyResp:
    def __init__(self, status=200, content=b'abc'):
        self.status_code = status
        self.content = content
    def raise_for_status(self):
        if self.status_code != 200:
            raise RuntimeError('bad status')

def test_play_elevenlabs_tts_success(monkeypatch):
    monkeypatch.setattr('kimi_gui_modern.requests.post', lambda *a, **k: DummyResp())
    called = []
    monkeypatch.setattr('kimi_gui_modern.playsound.playsound', lambda *a, **k: called.append(True))
    assert play_elevenlabs_tts('hi', 'voice', 'key')
    assert called

def test_play_elevenlabs_tts_fail(monkeypatch):
    monkeypatch.setattr('kimi_gui_modern.requests.post', lambda *a, **k: DummyResp(500))
    called = []
    monkeypatch.setattr('kimi_gui_modern.playsound.playsound', lambda *a, **k: called.append(True))
    assert not play_elevenlabs_tts('hi', 'voice', 'key')
    assert called == []
