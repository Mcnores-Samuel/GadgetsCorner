__version__ = '2.0.0'
VENSION = __version__
from . import _version
__version__ = _version.get_versions()['version']
