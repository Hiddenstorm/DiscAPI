from distutils.core import setup

setup(
  name = 'DiscAPI',         # How you named your package folder (MyLib)
  packages = ['DiscAPI'],   # Chose the same as "name"
  version = '0.1.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple to use Python Library to make all kinds of discord bot.',   # Give a short description about your library
  author = 'HiddenStorm',                   # Type in your name
  author_email = 'schuck2345@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Hiddenstorm/DiscAPI',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Python', 'Discord', 'Simple'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'asyncio',
          'websocket-client'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9',
  ],
)