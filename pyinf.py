#! python3
"""Show basic python information.

Based on examples from:
https://www.python.org/dev/peps/pep-0514/
https://docs.microsoft.com/en-us/visualstudio/python/installing-python-interpreters?view=vs-2017
"""

import sys
import winreg

def enum_keys(key):
    """iterates through child notes of key"""
    i = 0
    while True:
        try:
            yield winreg.EnumKey(key, i)
        except OSError:
            break
        i += 1

def get_value(key, value_name):
    """get registy value for key"""
    try:
        return winreg.QueryValue(key, value_name)
    except FileNotFoundError:
        return None

def search(key, sub_key):
    """try to open key and enumerate all python versions"""
    with winreg.OpenKey(key, sub_key) as company_key:
        for tag in enum_keys(company_key):
            with winreg.OpenKey(company_key, tag) as tag_key:
                print('PythonCore\\' + tag)
                print('DisplayName:', get_value(tag_key, 'DisplayName') or ('Python ' + tag))
                print('Version:', get_value(tag_key, 'Version') or tag[:3])
                print('SysArchitecture:', get_value(tag_key, 'SysArchitecture') or '(unknown)')

            try:
                ip_key = winreg.OpenKey(company_key, tag + '\\InstallPath')
            except FileNotFoundError:
                pass
            else:
                with ip_key:
                    print('InstallPath:', get_value(ip_key, None))
            print()

def current():
    """shows current version and executable"""
    print("Python")
    print("Version: " + sys.version)
    print("ExecutablePath: " + sys.executable)
    print()

def registered():
    """shows registered version and executable"""
    search(winreg.HKEY_LOCAL_MACHINE, r"Software\Python\PythonCore")
    search(winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Python\PythonCore")
    print()

if __name__ == "__main__":
    current()
    registered()
