import sys

from pip._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import Optional
# Shim to wrap setup.py invocation with setuptools
#
# We set sys.argv[0] to the path to the underlying setup.py file so
# setuptools / distutils don't take the path to the setup.py to be "-c" when
# invoking via the shim.  This avoids e.g. the following manifest_maker
# warning: "warning: manifest_maker: standard file '-c' not found".


def make_setuptools_shim_args(setup_py_path, unbuffered=False):
    # type: (str, Optional[bool]) -> list
    setuptools_shim = (
        "import sys, setuptools, tokenize;"
        "sys.argv[0] = {0!r}; __file__={0!r};"
        "f=getattr(tokenize, 'open', open)(__file__);"
        "code=f.read().replace('\\r\\n', '\\n');"
        "f.close();"
        "exec(compile(code, __file__, 'exec'))"
    )
    shim_args = [sys.executable, '-c', setuptools_shim.format(setup_py_path)]
    if unbuffered:
        shim_args.insert(1, '-u')
    return shim_args
