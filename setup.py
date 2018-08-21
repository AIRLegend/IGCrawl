from setuptools import setup

setup(
    name='IGCrawl',
    version='1.0.0',
    description='Instagram scrapper focused on social media analytics.',
    url='https://github.com/AIRLegend/IGCrawl',
    author='Alvaro Ibrain',
    author_email='alvaroibrain@hotmail.com',
    license='GNU',
    packages=['IGCrawl'],
    zip_safe=False,
    install_requires=[
        "requests==2.11.1",
        "InstagramAPI==1.0.2"
    ])
