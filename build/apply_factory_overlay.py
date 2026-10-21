"""Turn a verified RR source package into the GitHub factory distribution."""
from pathlib import Path
import ast
import re
import sys


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError(f"Expected exactly one factory patch anchor: {old!r}")
    return text.replace(old, new, 1)


def apply(root):
    root = Path(root)
    main_path = root / "main.py"
    widget_path = root / "nexusupdater/widget.py"
    main = main_path.read_text(encoding="utf-8")
    widget = widget_path.read_text(encoding="utf-8")
    if "# RR_GITHUB_FACTORY" in main:
        raise RuntimeError("This source already has the factory overlay")
    main, count = re.subn(r'^APP_VERSION = "[^"]+"$',
                         'APP_VERSION = "0.0.0"  # RR_GITHUB_FACTORY', main, flags=re.M)
    if count != 1:
        raise RuntimeError("APP_VERSION anchor missing or ambiguous")
    main = replace_once(main, '        self.home_page = page\n        layout = QVBoxLayout(page)\n',
        '''        self.home_page = page
        layout = QVBoxLayout(page)
        self.factory_announcement = QLabel(
            "This is the factory Github install. Checking NexusUpdater for the latest version…"
        )
        self.factory_announcement.setTextFormat(Qt.PlainText)
        self.factory_announcement.setWordWrap(True)
        self.factory_announcement.setObjectName("cardTitle")
        layout.addWidget(self.factory_announcement)
        self.factory_updates_button = QPushButton("Open Updates")
        self.factory_updates_button.clicked.connect(self._factory_open_updates)
        layout.addWidget(self.factory_updates_button)
''')
    main = replace_once(main, '    def _build_updates_tab(self):\n', '''    def _factory_open_updates(self):
        for index in range(self.tabs.count()):
            if self.tabs.tabText(index) == "Updates":
                self.tabs.setCurrentIndex(index)
                break

    def _factory_version_checked(self, info):
        version = str(info.latest_version).strip()
        if not version:
            self._factory_version_failed("Missing version")
            return
        self.factory_announcement.setText(
            "This is the factory Github install. Please update to "
            f"{version} under the Updates tab to unlock the latest features."
        )

    def _factory_version_failed(self, _message):
        self.factory_announcement.setText(
            "This is the factory Github install. NexusUpdater could not be reached. "
            "Please check for updates under the Updates tab to unlock the latest features."
        )

    def _build_updates_tab(self):
''')
    # Use the same manifest request for the landing message and Install button.
    # Do not persist a factory flag in user settings: the full replacement has
    # no factory code, so the notice disappears after a successful update.
    main = replace_once(main,
        '        self.nexus_update_widget.update_requested.connect(self._start_nexus_update)\n',
        '''        self.nexus_update_widget.update_requested.connect(self._start_nexus_update)
        self.nexus_update_widget.check_completed.connect(self._factory_version_checked)
        self.nexus_update_widget.check_failed.connect(self._factory_version_failed)
''')
    main = replace_once(main,
        '        if bool(self.cfg.get("auto_update_check", True)) and self.nexus_update_widget.server_url.startswith("https://"):\n            QTimer.singleShot(5000, self.nexus_update_widget.check_updates)\n',
        '        QTimer.singleShot(0, self.nexus_update_widget.check_updates)\n')
    widget = replace_once(widget, '    update_requested = Signal(object)\n',
        '    update_requested = Signal(object)\n    check_completed = Signal(object)\n    check_failed = Signal(str)\n')
    widget = replace_once(widget, '    def check_updates(self):\n',
        '    def check_updates(self):\n        if self.worker is not None and self.worker.isRunning():\n            return\n')
    widget = replace_once(widget, '    def _checked(self, info):\n',
        '    def _checked(self, info):\n        self.check_completed.emit(info)\n')
    widget = replace_once(widget, '    def _failed(self, msg):\n',
        '    def _failed(self, msg):\n        self.check_failed.emit(msg)\n')
    # Validate all patches before writing anything.
    ast.parse(main)
    ast.parse(widget)
    main_path.write_text(main, encoding="utf-8")
    widget_path.write_text(widget, encoding="utf-8")
    run = root / "run.bat"
    run.write_text(run.read_text(encoding="utf-8").replace(
        "title Rosco Radio v0.1.5 AI", "title Rosco Radio - Github Factory"), encoding="utf-8")


if __name__ == "__main__":
    apply(sys.argv[1])
    print("GitHub factory overlay applied; updates are supplied by NexusUpdater.")
