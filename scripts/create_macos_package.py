import platform
import shutil
import subprocess
import sys


def build_app():
    pyinstaller = shutil.which("pyinstaller")
    if not pyinstaller:
        print("ERROR: This script requires pyinstaller.")
        sys.exit(1)

    pyinst_cmd = [
        pyinstaller,
        "activity-browser.spec",
        "--clean",
        "-y"
    ]
    subprocess.check_call(pyinst_cmd)


def build_macos_package(application_path='dist/Activity Browser.app', package_path='./Activity Browser-{}.pkg',
                        sign_identity: str=None):
    macos_architecture = 'intel' if platform.processor() == 'i386' else 'arm'
    build_cmd = [
        'pkgbuild',
        '--component',
        application_path,
        "--install-location",
        '/Applications',
        package_path.format(macos_architecture)
    ]
    if sign_identity:
        build_cmd = build_cmd[0] + ['--sign', sign_identity] + build_cmd[1:]
    subprocess.check_call(build_cmd)


if __name__ == "__main__":
    import argparse

    if not shutil.which("pyinstaller"):
        subprocess.check_call(["pip", "install", "--upgrade", "pyinstaller"])

    parser = argparse.ArgumentParser()
    parser.add_argument("--sign-identity", help="signing identity")
    options = parser.parse_args()
    build_app()
    build_macos_package(sign_identity=options.sign_identity)