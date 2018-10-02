from setuptools import setup
import codecs


# Copied from (and hacked):
# https://github.com/pypa/virtualenv/blob/develop/setup.py#L42
def get_version(filename):
    import os
    import re

    here = os.path.dirname(os.path.abspath(__file__))
    f = codecs.open(os.path.join(here, filename), encoding='utf-8')
    version_file = f.read()
    f.close()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='timeflies',
    description=(
        'Quick profiling'
    ),
    long_description=codecs.open("README.md", encoding='utf-8').read(),
    version=get_version('timeflies.py'),
    license='BSD',
    author='Teemu Kokkonen',
    author_email='teemu.kokkonen@planbrothers.io',
    py_modules=['timeflies'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['crayons'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
