###### A web scrapper that will get the price from EMAG.ro website and save all the history within a text file locally
###### You can monitor the price fluctuation history to see if deals are really good deals
###### You can set up a certain price drop point to send an email to you as notification. You get the price in the email
###### The program will work without the email notification part. Notice that the email notification functionality is turned off by default. If you want to use it, just uncomment lines from FOR LOOP Part of the code


###### python libraries to import. bs4 needs to be installed with pip, as it is not standard library
import requests, bs4, re, time
import smtplib
import psycopg2 as pg2


########## We want to save locally all the scraping on to a text file, together with timestamp
def fileCreator(filename, content):
    with open("{}_stored_item.txt".format(str(filename)), "a") as fileWriter:
        timeis = timeStamp()
        fileWriter.write(timeis + ' - ' + str(content) + ' RON\n')


########## a local timestamp creator
def timeStamp():
    seconds = time.time()
    local_time = time.ctime(seconds)
    timeis = 'Time of check '+local_time
    return timeis


########## A function that will be used in case the price drops under certain price, it will send an email
def emailNote(msg):             ##### msg can only be a String
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("youremail@gmail.com", "password")
    server.sendmail("mailFrom", "mailTo", msg)
    server.quit()


########## The actual scrapper where you send as arguements the page to check and the selector of element to store. After ,just change with web and selector you need
def scraper(url,selector):
    rawRequest = requests.get(url)
    rawRequest.raise_for_status()
    soup = bs4.BeautifulSoup(rawRequest.text, 'html.parser')
    element = soup.select(selector)
    formatOfPrice = re.compile(r'\d.\d\d\d')            ########## re.compile wants ONLY number of 4 digits(ex 2.099). For own use format accordingly at re.compile (ex: for 233 you put re.compile(r'\d\d\d'))
    match = formatOfPrice.findall(element[0].text)
    return match


########### For the purpose to test the code yourself, you can use the web page and selector below
########### If you want to use it for yourself, change web to where you look at and selector
########### (check bs4 docs for more options for selector. Below is a COPY CSS SELECTOR example)
webToScrape = ('https://www.emag.ro/televizor-lg-139-cm-smart-4k-ultra-hd-led-clasa-a-55un73003la/pd/D4GCJMMBM/')
selector = ('#page-skin > div.container > div > div:nth-child(2) > div.col-sm-5.col-md-7.col-lg-7 > div > div > div.col-sm-12.col-md-6.col-lg-5 > form > div.product-highlight.product-page-pricing > div:nth-child(1) > div > div.w-50.mrg-rgt-xs > p.product-new-price')


########### add1data will write the price scraped INTO the database and showLastQuery is here just for debugging purpose so you can see the confirmation straight from the database that the update was performed
########### Notice that in this case you work with a database already created. In here database is named emagscrape, table is named allprices and it has 2 columns, first is price which is the value we scrape and second is exact_time which is a time stamp of the update into db action
def add1data(query):
    conn = pg2.connect(dbname='emagscrape',user='postgres',password='yourPasswordHere')      ###########  user for the PostgreSQL is set to default which is postgres. But do not forget to insert your password here
    cur = conn.cursor()
    priceToReturn = cur.execute("INSERT INTO allprices(price) VALUES({});".format(query))
    conn.commit()
    conn.close()

def showLastQuery():
    conn = pg2.connect(dbname='emagscrape',user='postgres',password='yourPasswordHere')
    cur = conn.cursor()
    cur.execute("SELECT price FROM allprices ORDER BY exact_time DESC LIMIT 1;")
    return cur.fetchall()
    conn.close()

    
########## A for loop that will run the program for a certain amount of times plus time module used to sleep to prolong the process
########## If you put for example range(0,30) and time.sleep(1440) then 1440 is a day in seconds and it will check for a month(daily)
########## Or you can split the 1440 in half and double the 30 from range and you get 2 times per day for one month
for i in range(0,2):
    data = scraper(webToScrape,selector)
    fileContent = data[0]
    print('Data scraped from the web: ' + fileContent)
    add1data(fileContent)
    lastQuery = showLastQuery()
    print('Database succesfully updated with value: '+lastQuery[0][0])
    withoutDot = fileContent.replace(".","")
    integerToCompare = int(withoutDot)
    # if integerToCompare > 1900:              ##### here we set a desired price to trigger a function
    # stringIt = str(integerToCompare)
    # emailNote(stringIt)                  ##### a function that will send us a notification email about price drop
    fileCreator('Emag',integerToCompare)
    time.sleep(3)

