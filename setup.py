from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='kmmessage',
      version='0.02.00',
      description='Cheap Personal Messaging Library',
      author='Keith Murray',
      author_email='kmurrayis@gmail.com',
      license='MIT',
      packages=['kmmessage'],
      install_requires=[
	  'email'
      ],
      include_package_data=True,
      zip_safe=False)
