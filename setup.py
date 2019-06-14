import setuptools

setuptools.setup(
  name='cah-clone',
  version='0.0.1',
  author='Ryan Bernstein',
  author_email='rmbern@yahoo.com',
  description='LAN based Cards Against Humanity Clone',
  long_description='TODO',
  long_description_content_type='text/markdown',
  url='https://github.com/rmbern/cah-clone',
  packages=setuptools.find_packages(),
  include_package_data=True,
  license='GNU GPL v3.0',
  install_requires=['flask', 'uwsgi'],
  setup_requires=['wheel'],
)
