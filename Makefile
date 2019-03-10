directory-spider:
	scrapy crawl directory-spider -a selenium_hostname=localhost



employee-spider:
	scrapy crawl employee-spider -a selenium_hostname=localhost


company-spider:
	scrapy crawl company-spider -a selenium_hostname=localhost


start-selenium:
	cd linkedin ; bash -c "java -Dwebdriver.chrome.driver="etc/chromedriver" -jar etc/selenium-server-standalone-3.141.59.jar"


test:
	cd linkedin ; pytest