from distutils.core import setup
import re

version = ''
with open('DiscAPI/__init__.py') as f:
  version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
  name = 'DiscAPI',         
  packages = ['DiscAPI'],   
  version = version,      
  license='MIT',        
  description = 'A simple to use Python Library to make all kinds of discord bot.',   
  author = "HiddenStorm",                   
  author_email = 'schuck2345@gmail.com',     
  url = 'https://github.com/Hiddenstorm/DiscAPI',  
  download_url = 'https://github.com/Hiddenstorm/DiscAPI/archive/refs/tags/v{}.tar.gz'.format(version),   
  keywords = ['Python', 'Discord', 'Simple'],   
  install_requires=[           
          'websocket-client'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta", "5 - Production/Stable" 
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.9',
  ],
)