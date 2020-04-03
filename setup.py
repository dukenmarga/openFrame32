from distutils.core import setup
setup(
  name = 'openSAP32',
  packages = ['openSAP32'],
  version = 0.2,
  license='New BSD',
  description = 'openSAP32 is open source software for modeling and perform structural analysis.',
  author = 'Duken Marga',
  author_email = 'dukenmarga@gmail.com',
  url = 'https://github.com/dukenmarga/openSAP32',
  download_url = 'https://github.com/dukenmarga/openSAP32/archive/v0.1.tar.gz',
  keywords = ['structural', 'analysis', 'civil','engineering','frame'],
  install_requires=[
          'numpy>=1.16',
          'math',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
