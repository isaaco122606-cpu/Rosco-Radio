"""Exercise the overlay against the actual, verified base supplied by CI."""
import ast
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace

overlay_path = Path(__file__).resolve().parents[1] / "build/apply_factory_overlay.py"
spec = importlib.util.spec_from_file_location("factory_overlay", overlay_path)
overlay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(overlay)


class Label:
    def setText(self, value):
        self.text = value


def test(source):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "nexusupdater").mkdir()
        for filename in ("main.py", "run.bat", "nexusupdater/widget.py"):
            shutil.copyfile(source / filename, root / filename)
        overlay.apply(root)
        main = ast.parse((root / "main.py").read_text())
        widget = ast.parse((root / "nexusupdater/widget.py").read_text())
        assert any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "APP_VERSION" for t in n.targets)
                   and ast.literal_eval(n.value) == "0.0.0" for n in main.body)
        methods = [n for n in ast.walk(main) if isinstance(n, ast.FunctionDef)
                   and n.name in ("_factory_version_checked", "_factory_version_failed", "_factory_open_updates")]
        namespace = {}
        exec(compile(ast.Module(body=methods, type_ignores=[]), "factory-methods", "exec"), namespace)
        label = Label()
        owner = SimpleNamespace(factory_announcement=label)
        owner._factory_version_failed = lambda msg: namespace["_factory_version_failed"](owner, msg)
        for version in ("0.1.6", "12.34.56", "v3.0.1"):
            namespace["_factory_version_checked"](owner, SimpleNamespace(latest_version=version))
            assert label.text == ("This is the factory Github install. Please update to " + version
                                  + " under the Updates tab to unlock the latest features.")
        owner._factory_version_failed("offline")
        assert "could not be reached" in label.text
        namespace["_factory_version_checked"](owner, SimpleNamespace(latest_version=""))
        assert "could not be reached" in label.text
        namespace["_factory_version_checked"](owner, SimpleNamespace(latest_version="0.1.7"))
        assert "0.1.7 under the Updates tab" in label.text  # Retry recovers.
        class Tabs:
            def count(self): return 3
            def tabText(self, index): return ["Home", "Radio", "Updates"][index]
            def setCurrentIndex(self, index): self.selected = index
        owner.tabs = Tabs()
        namespace["_factory_open_updates"](owner)
        assert owner.tabs.selected == 2
        checked = next(n for n in ast.walk(widget) if isinstance(n, ast.FunctionDef) and n.name == "_checked")
        assert "self.check_completed.emit(info)" in ast.unparse(checked)
        # The full package's helper and launch flow must remain untouched.
        original = (source / "main.py").read_text()
        original_tree = ast.parse(original)
        for name in ("_start_nexus_update", "_launch_nexus_helper"):
            get = lambda tree: next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == name)
            assert ast.dump(get(main)) == ast.dump(get(original_tree))
        try:
            overlay.apply(root)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Repeated overlay must fail instead of duplicating UI")
        # An incompatible base must fail without partially changing the package.
        (root / "main.py").write_text(original.replace("self.home_page = page", "self.home_page_changed = page"))
        before = (root / "main.py").read_bytes()
        try:
            overlay.apply(root)
        except RuntimeError:
            assert (root / "main.py").read_bytes() == before
        else:
            raise AssertionError("Missing anchor should fail")
    print("Factory overlay tests passed")


if __name__ == "__main__":
    test(Path(sys.argv[1]))
