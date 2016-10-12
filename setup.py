from setuptools import setup, Distribution


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


setup(
    name='Coliform',
    version='0.6.7',
    description='Coliform UPRM Project Library, Written for Raspberry Pi',
    packages=['Coliform'],
    author='Osvaldo E Duran',
    author_email='osvaldo.duran@upr.edu',
    url='https://github.com/Regendor/coliform-project',
    classifiers=['Programming Language :: Python :: 3', 'Intended Audience :: Education',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
    install_requires=['RPi.GPIO', 'pyserial', 'picamera', 'matplotlib'],
    distclass=BinaryDistribution
)
