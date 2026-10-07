from __future__ import annotations

from pathlib import Path
import sys

root = Path(sys.argv[1])
main_path = root / "main.py"
choc_path = root / "chocolate_rain.py"
ach_path = root / "achievements.py"


def insert_once(text: str, anchor: str, replacement: str, marker: str) -> str:
    if marker in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"Required anchor not found: {anchor!r}")
    return text.replace(anchor, replacement, 1)


main = main_path.read_text(encoding="utf-8")

main = insert_once(
    main,
    "from cw_engine import CWEngine\n",
    "from cw_engine import CWEngine\nfrom achievements import ACHIEVEMENTS, unlock as achievement_unlock, count_unlocked as achievement_count\n",
    "from achievements import ACHIEVEMENTS",
)

main = insert_once(
    main,
    "        self._build_cw_tab()\n",
    "        self._build_cw_tab()\n        self._build_achievements_tab()\n",
    "self._build_achievements_tab()",
)

ACH_METHODS = r'''

    # ---------- Achievements ----------
    def _achievement_unlock(self, key):
        try:
            item = achievement_unlock(self.cfg, key)
            if not item:
                return False
            save_config(self.cfg)
            self._notify(
                f"🏆 Achievement unlocked · {item['title']}",
                item['description'],
                "success",
                cooldown_key=f"achievement-{key}",
                cooldown=1.0,
            )
            self._refresh_achievements_page()
            return True
        except Exception:
            return False

    def _build_achievements_tab(self):
        page = QWidget()
        self.achievements_page = page
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        hero = QLabel("ACHIEVEMENTS")
        hero.setObjectName("hero")
        layout.addWidget(hero)
        self.achievement_progress = QLabel("")
        self.achievement_progress.setObjectName("muted")
        layout.addWidget(self.achievement_progress)

        self.achievement_list = QScrollArea()
        self.achievement_list.setWidgetResizable(True)
        self.achievement_list_host = QWidget()
        self.achievement_list_layout = QVBoxLayout(self.achievement_list_host)
        self.achievement_list_layout.setSpacing(8)
        self.achievement_list.setWidget(self.achievement_list_host)
        layout.addWidget(self.achievement_list, 1)
        self.tabs.addTab(page, "Achievements")
        self._refresh_achievements_page()

    def _refresh_achievements_page(self):
        if not hasattr(self, "achievement_list_layout"):
            return
        while self.achievement_list_layout.count():
            item = self.achievement_list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        store = self.cfg.get("achievements", {}) if isinstance(self.cfg.get("achievements", {}), dict) else {}
        unlocked = achievement_count(self.cfg)
        total = len(ACHIEVEMENTS)
        self.achievement_progress.setText(f"{unlocked} / {total} unlocked")
        for key, meta in ACHIEVEMENTS.items():
            card = QFrame()
            card.setObjectName("card")
            row = QVBoxLayout(card)
            earned = key in store
            title = QLabel(("🏆 " if earned else "🔒 ") + meta["title"])
            title.setStyleSheet("font-size:15px;font-weight:800;")
            desc = QLabel(meta["description"] if earned else "???")
            desc.setWordWrap(True)
            desc.setObjectName("muted")
            row.addWidget(title)
            row.addWidget(desc)
            if earned:
                stamp = QLabel(f"Unlocked · {store[key]}")
                stamp.setObjectName("muted")
                row.addWidget(stamp)
            self.achievement_list_layout.addWidget(card)
        self.achievement_list_layout.addStretch(1)
'''

main = insert_once(
    main,
    "    # ---------- RR AI ----------\n",
    ACH_METHODS + "\n\n    # ---------- RR AI ----------\n",
    "# ---------- Achievements ----------",
)

main = insert_once(
    main,
    '        badge = "RR AI · AUTO" if origin == "auto" else "RR AI"\n',
    '''        if origin != "auto":\n            caps_words = re.findall(r"\\b[A-Z]{3,}\\b", clean)\n            chaos_score = clean.count("!") + clean.count("?!") + clean.count("!?") + len(caps_words)\n            if chaos_score >= 8 or len(clean) >= 1800:\n                self._achievement_unlock("ai_freakout")\n\n        badge = "RR AI · AUTO" if origin == "auto" else "RR AI"\n''',
    'self._achievement_unlock("ai_freakout")',
)

main = insert_once(
    main,
    "            dialog.exec()\n",
    "            dialog.exec()\n            if getattr(dialog, \"completed\", False):\n                self._achievement_unlock(\"chocolate_complete\")\n",
    'self._achievement_unlock("chocolate_complete")',
)

main = insert_once(
    main,
    '''    def _append_cw_text(self, text):\n        if not text:\n            return\n''',
    '''    def _append_cw_text(self, text):\n        if not text:\n            return\n        if re.search(r"[A-Za-z0-9]", str(text)):\n            self._achievement_unlock("cw_contact")\n''',
    'self._achievement_unlock("cw_contact")',
)

main = insert_once(
    main,
    '        mode_name = "PREVIEW" if preview else "VOX TX"\n',
    '        mode_name = "PREVIEW" if preview else "VOX TX"\n        if not preview:\n            self._achievement_unlock("vox_first")\n',
    'mode_name = "PREVIEW" if preview else "VOX TX"\n        if not preview:',
)

main = insert_once(
    main,
    '            self.audio_status.setText("Microphone active")\n',
    '            self.audio_status.setText("Microphone active")\n            if (self.backend.currentData() or "vox") == "vox" and self._tx_unlocked():\n                self._achievement_unlock("vox_first")\n',
    'self._tx_unlocked():\n                self._achievement_unlock("vox_first")',
)

main = insert_once(
    main,
    '''    def _append_transcript(self, text):\n        stamp = datetime.now().strftime("%H:%M:%S")\n''',
    '''    def _append_transcript(self, text):\n        if len(re.findall(r"[A-Za-z0-9']+", str(text))) >= 3:\n            self._achievement_unlock("rx_contact")\n        stamp = datetime.now().strftime("%H:%M:%S")\n''',
    'self._achievement_unlock("rx_contact")',
)

main = insert_once(
    main,
    '        self._notify("UTC announcement", display, "info", cooldown_key="utc-announcement", cooldown=45.0)\n',
    '        self._notify("UTC announcement", display, "info", cooldown_key="utc-announcement", cooldown=45.0)\n        self._achievement_unlock("utc_tts")\n',
    'self._achievement_unlock("utc_tts")',
)

main = insert_once(
    main,
    '        elif band == "cb":\n',
    '        elif band == "cb":\n            self._achievement_unlock("baited")\n',
    'self._achievement_unlock("baited")',
)

main = insert_once(
    main,
    '            self.ptt.setText("TRANSMITTING")\n',
    '            self.ptt.setText("TRANSMITTING")\n            self._achievement_unlock("serial_ptt_first")\n',
    'self._achievement_unlock("serial_ptt_first")',
)

main_path.write_text(main, encoding="utf-8")

choc = choc_path.read_text(encoding="utf-8")
choc = insert_once(
    choc,
    "        self.setWindowTitle('Rosco Radio · Unexpected chocolate event')\n",
    "        self.setWindowTitle('Rosco Radio · Unexpected chocolate event')\n        self.completed = False\n",
    "self.completed = False",
)
choc = insert_once(
    choc,
    "        if status == QMediaPlayer.EndOfMedia:\n",
    "        if status == QMediaPlayer.EndOfMedia:\n            self.completed = True\n",
    "self.completed = True",
)
choc_path.write_text(choc, encoding="utf-8")

ACHIEVEMENTS_PY = '''from __future__ import annotations\n\nfrom datetime import datetime, timezone\n\nACHIEVEMENTS = {\n    "baited": {\n        "title": "Baited",\n        "description": "Tried to use a CB radio with RR when no support will ever go live for it... hehe",\n    },\n    "vox_first": {\n        "title": "Transmitted through VOX for the first time",\n        "description": "Transmission is glory! Transmission is life! YOU SHALL TRANSMIT MORE!!",\n    },\n    "serial_ptt_first": {\n        "title": "Transmitted through serial-PTT for the first time",\n        "description": "Even I can't do that... how did you manage to do that? please tell me😭",\n    },\n    "utc_tts": {\n        "title": "Got a UTC announcement via the TTS decoder",\n        "description": "Honestly amazing. That thing can barely hear the Text of Ulysses read at 0.5x speed!",\n    },\n    "chocolate_complete": {\n        "title": "Watched the whole Chocolate Broadcast",\n        "description": "Torture.",\n    },\n    "rx_contact": {\n        "title": "Received an RX contact for the first time",\n        "description": "Less chance of being lonely!",\n    },\n    "cw_contact": {\n        "title": "Made a first contact with CW/Morse Code",\n        "description": ".. / -... . - / -.-- --- ..- / -.-. .- -. .----. - / . ...- . -. / .-. . .- -.. / - .... .. ... .-.-.- .-.-.- .-.-.-",\n    },\n    "ai_freakout": {\n        "title": "Forced RR AI to freak out",\n        "description": "Ah yes, the art of messing with a 4b params model.",\n    },\n}\n\n\ndef ensure_store(cfg):\n    store = cfg.setdefault("achievements", {})\n    if not isinstance(store, dict):\n        store = {}\n        cfg["achievements"] = store\n    return store\n\n\ndef unlock(cfg, key):\n    if key not in ACHIEVEMENTS:\n        return None\n    store = ensure_store(cfg)\n    if key in store:\n        return None\n    store[key] = datetime.now(timezone.utc).isoformat(timespec="seconds")\n    item = dict(ACHIEVEMENTS[key])\n    item["key"] = key\n    item["unlocked_at"] = store[key]\n    return item\n\n\ndef is_unlocked(cfg, key):\n    return key in ensure_store(cfg)\n\n\ndef count_unlocked(cfg):\n    store = ensure_store(cfg)\n    return sum(1 for key in ACHIEVEMENTS if key in store)\n'''
ach_path.write_text(ACHIEVEMENTS_PY, encoding="utf-8")

print("Achievements semantic overlay complete")
