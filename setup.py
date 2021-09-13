from distutils.core import setup

setup(
  name = 'DiscAPI',         
  packages = ['DiscAPI'],   
  version = '0.1.2',      
  license='MIT',        
  description = 'A simple to use Python Library to make all kinds of discord bot.',   
  author = 'HiddenStorm',                   
  author_email = 'schuck2345@gmail.com',     
  url = 'https://github.com/Hiddenstorm/DiscAPI',  
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',   
  keywords = ['Python', 'Discord', 'Simple'],   
  install_requires=[           
          'websocket-client',
          'json'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # "3 - Alpha", "4 - Beta", "5 - Production/Stable" 
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.9',
  ],
)