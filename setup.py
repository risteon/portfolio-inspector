from setuptools import setup

setup(
    name="portfolio_inspector",
    version="0.1.0dev",
    description="Analyse portfolio data.",
    url="http://github.com/risteon/portfolio-inspector",
    author="Christoph Rist",
    author_email="c.rist@posteo.de",
    license="MIT",
    packages=["portfolio_inspector"],
    zip_safe=False,
    install_requires=[],
    test_suite="nose.collector",
    tests_require=["nose", "pytest"],
    python_requires=">=3.7",
)
