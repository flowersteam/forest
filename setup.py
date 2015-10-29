from setuptools import setup

import versioneer

setup(name         = 'forest',
      version      = '1.0',
      cmdclass     = versioneer.get_cmdclass(),
      author       = 'Fabien Benureau',
      author_email = 'fabien.benureau+forest@gmail.com',
      url          = 'github.com/humm/forest.git',
      maintainer   = 'Fabien C. Y. Benureau',
      license      = 'LGPLv3',
      packages     = ['forest'],
      description  ='A python hierarchical configuration structure for scientific experiments',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
      ]
     )
