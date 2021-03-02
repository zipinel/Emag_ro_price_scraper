# Emag_ro_price_scraper
Price scraper that saves history on a local file and sends an email if certain price drop is set. May work on most websites but is created mainly for emag.ro

02.03.2021 - Feature added: Besides the fact that the scraper saves the history on a text file, it now saves the history in a database made with PostgreSQL

Planned features to be added:

1. Use of a proxy or multiple proxies to avoid getting banned by the website
2. Use of google API for the email notification part
3. Better format of email contents
4. Implementation of SQL in the process (done)
5. Refactoring the scraper() 
