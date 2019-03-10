
[![built with Selenium](https://img.shields.io/badge/built%20with-Selenium-yellow.svg)](https://github.com/SeleniumHQ/selenium)
[![built with Scrapy](https://img.shields.io/badge/built%20with-Scrapy-green.svg)](https://scrapy.org/)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)
[![built with Chrome Web Driver](https://img.shields.io/badge/built%20with-Chrome%20Web%20Driver-blue.svg)](http://chromedriver.chromium.org/)
# Linkedin Crawler


## How ro run
- start selenium server
    ```bash
        make start-selenium
    ```
- run unit test
    ```bash
        make test
    ```
- crawl a company's employees  
    - run company spider
    ```bash
        make company-spider
    ```
    - run employee spider
    ```bash
        make employee-spider
    ```
