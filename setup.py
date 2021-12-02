import os
from setuptools import setup, find_packages
from setuptools import Extension
from distutils.command.build import build as build_orig

from setuptools import dist

__version__ = "0.1.0"

exts = [Extension(name='pynms.nms_ext',
                  sources=["pynms/_nms_ext.c", "pynms/nms_ext.pyx"],
                  include_dirs=["pynms"],
                  extra_compile_args=['-std=c99'])]

class build(build_orig):
    def finalize_options(self):
        super().finalize_options()
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        for extension in self.distribution.ext_modules:
            extension.include_dirs.append(numpy.get_include())
        from Cython.Build import cythonize
        self.distribution.ext_modules = cythonize(self.distribution.ext_modules,
                                                  language_level=3)

setup(name='pynms',
    version=__version__,
    description='Python Non-maximal supress',
    url='https://github.com/vlkit/pynms',
    author_email='kz@kaizhao.net',
    license='MIT',
    packages=find_packages(),
    ext_modules=exts,
    setup_requires=['numpy', 'cython'],
    install_requires=["numpy", 'cython'],
    zip_safe=False,
    package_data={"pynms": ["nms.h", "nms_ext.pyx"]},
    cmdclass={"build": build},
)
