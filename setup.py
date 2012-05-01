try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import glob

setup(
    name='network-pinger',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Tornado",
        "SQLAlchemy>=0.6",
        "Webhelpers",
        "beaker",
        "ping_wrapper",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'networkpinger': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'networkpinger': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    #paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [console_scripts]
    network-pinger-server   = networkpinger.app:main
    """,
    scripts=glob.glob("scripts/*"),
)
