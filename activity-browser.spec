# -*- mode: python ; coding: utf-8 -*-
import argparse
import os
import platform

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true")
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--console", action="store_true")
options = parser.parse_args()

python_options = [
    ("W ignore", None, "OPTION"),
]
if options.verbose:
    python_options.append(("v", None, "OPTION"))

EXE_ICON = os.path.join("activity_browser", "static", "icons", "activity-browser.ico") if platform.system().lower() == 'windows' else None

a = Analysis(
    ["run-activity-browser.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=["activity_browser", "playhouse"],
    hookspath=['scripts/hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
a.datas += Tree("activity_browser/static", prefix="activity_browser/static")
pyz = PYZ(a.pure)

if options.debug:
    exe = EXE(
        pyz,
        a.scripts,
        python_options,
        exclude_binaries=True,
        name="activity-browser",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=options.console,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name="activity-browser",
        icon=EXE_ICON
    )
    target = coll
else:
    exe = EXE(
        pyz,
        a.scripts,
        python_options,
        a.binaries,
        a.datas,
        name="activity-browser",
        console=options.console,
        icon=EXE_ICON
    )
    target = exe

if platform.system() == "Darwin":
    app = BUNDLE(
        target,
        name="Activity Browser.app",
        icon="activity_browser/static/icons/activity-browser.icns",
        bundle_identifier="com.github.lca_activity_browser.activity_browser",
        version=os.environ.get("VERSION", "0.0.0"),
        info_plist={
            "NSPrincipalClass": "NSApplication",
            "NSAppleScriptEnabled": False,
            "CFBundleDocumentTypes": [
                {
                    "CFBundleTypeName": "Icon",
                    "CFBundleTypeIconFile": "activity_browser/static/icons/activity-browser.icns",
                    "LSItemContentTypes": [
                        "com.github.lca_activity_browser.activity_browser"
                    ],
                    "LSHandlerRank": "Owner",
                }
            ],
        },
    )
