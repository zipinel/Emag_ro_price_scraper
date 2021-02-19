###### A web scrapper that will get the price from EMAG.ro website and save all the history within a text file locally
###### You can monitor the price fluctuation history to see if deals are really good deals
###### You can set up a certain price drop point to send an email to you as notification. You get the price in the email
###### The program will work without the email notification part if you comment out line 68, 69 and 70


###### python libraries to import. bs4 needs to be installed with pip, as it is not standard library
import requests, bs4, re, time
import smtplib


########## We want to save locally all the scraping on to a text file, together with timestamp
def fileCreator(filename, content):
    with open("{}_stored_item.txt".format(str(filename)), "a") as fileWriter:
        timeis = timeStamp()
        fileWriter.write(timeis + ' - ' + str(content) + ' RON\n')


########## a local (your country) timestamp creator
def timeStamp():
    seconds = time.time()
    local_time = time.ctime(seconds)
    timeis = 'Time of check '+local_time
    return timeis


########## A function that will be used in case the price drops under certain price, it will send an email
########## The functions accepts an arguement msg. It must always be a string
########## Program will not work without the credentials entered below
def emailNote(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("youremail@gmail.com", "password")
    server.sendmail("mailFrom", "mailTo", msg)
    server.quit()



########## The actual scrapper where you send as arguements the page to check and the selector of element to store
########## Requests module gets the page, bs4 parse the info and uses selector to reach your element
########## Then re.compile wants ONLY number of 4 digits(ex 2.099) and returns it
########## If you are looking at different values then format accordingly at re.compile (ex: for 233 you put re.compile(r'\d\d\d'))
def scraper(url,selector):
    rawRequest = requests.get(url)
    rawRequest.raise_for_status()
    soup = bs4.BeautifulSoup(rawRequest.text, 'html.parser')
    element = soup.select(selector)
    formatOfPrice = re.compile(r'\d.\d\d\d')
    match = formatOfPrice.findall(element[0].text)
    return match

########### For the purpose to test the code yourself, you can use the web page and selector below
########### If you want to use it for yourself, change web to where you look at and selector
########### (check bs4 docs for more options than COPY CSS SELECTOR option chosen here)
webToScrape = ('https://www.emag.ro/televizor-lg-139-cm-smart-4k-ultra-hd-led-clasa-a-55un73003la/pd/D4GCJMMBM/')
selector = ('#page-skin > div.container > div > div:nth-child(2) > div.col-sm-5.col-md-7.col-lg-7 > div > div > div.col-sm-12.col-md-6.col-lg-5 > form > div.product-highlight.product-page-pricing > div:nth-child(1) > div > div.w-50.mrg-rgt-xs > p.product-new-price')



########## A for loop that will run the program for a certain amount of times plus time module used to sleep to prolong the process
########## If you put for example range(0,30) and time.sleep(1440) then 1440 is a day in seconds and it will check for a month(daily)
########## Or you can split the 1440 in half and double the 30 from range and you get 2 times per day for one month
for i in range(0,2):
    data = scraper(webToScrape,selector)
    fileContent = data[0]
    withoutDot = fileContent.replace(".","")
    integerToCompare = int(withoutDot)
    if integerToCompare > 1900:              ##### here we set a desired price to trigger a function
        stringIt = str(integerToCompare)
        emailNote(stringIt)                  ##### a function that will send us a notification email about price drop
    fileCreator('Emag',integerToCompare)
    time.sleep(3)

########## Of course don't forget that you must have a computer running and/or the program live
########## You can remove the email notification function if you just comment out line 68,69 and 70