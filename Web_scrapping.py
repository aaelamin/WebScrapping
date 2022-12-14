# Import necessary Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time 
import pandas as pd

class WebScrapping:
    def __init__(self = object, job = str, place = str) -> None:
        """
        Parameters
        ----------
        job: str
             The job title; Specified by the user
             
        place: str
             The job location; Specified by the user
        """
        self.job = job
        self.place = place
        self.driver = webdriver.Chrome("/Users/elamin/Projects/Extras/chromedriver")
        self.driver.get("https://ca.indeed.com/")
    
      
    def search(self):
        """
        Searches for jobs using the tite and the location given by the user
        """
        # Fill in the 'What' section    
        what = self.driver.find_element(By.ID, "text-input-what")
        what.send_keys(Keys.COMMAND + "a")
        what.send_keys(Keys.DELETE)
        what.send_keys(self.job)
        
        # Fill in the 'where' section
        where = self.driver.find_element(By.ID, "text-input-where")
        where.send_keys(Keys.COMMAND + "a")
        where.send_keys(Keys.DELETE)
        where.send_keys(self.place)
        
        # Start Search
        self.driver.find_element(By.CSS_SELECTOR, '#jobsearch > button').click()
    
    
    def container(self):
        """
        Finds the containers that holds information about the job posting
        
        Return
        ------
        div: str
             The HTML elements that hold information about the jon
        """
        
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        div = soup.find_all('div', {'class': "slider_container css-g7s71f eu4oa1w0"})
        return div
    
    
    def next(self):
        """
        Moves to the next page 
        """
        self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']").click()
        
        
    def data(self):
        """
        Collects the information of individual job postings 
        """
        while True:
            try:
                cards = self.container()
                for card in cards: 
                    
                    # Find title
                    try:
                        title = card.find('a').text
                    except:
                        title = ' '
                    
                    # Find company
                    try:
                        company = card.find('span', {'class': "companyName"}).text
                    except:
                        company = ''
                        
                    # Find location 
                    try:
                        location = card.find('div', {'class': "companyLocation"}).text
                    except:
                        location = ''
                        
                    # Find salary
                    try:
                        salary = card.find('div', {'class': "metadata salary-snippet-container"}).text
                    except:
                        salary = ''
                        
                    # Find rating
                    try:
                        rating = card.find('span', {'class':"ratingsDisplay withRatingLink"}).text
                    except:
                        rating = ''
                    
                    # Find link
                    try:
                        href = card.find("a",{"class":"jcs-JobTitle css-jspxzf eu4oa1w0"})['href']
                        link = (f"https://ca.indeed.com{href}")
                    except:
                        link = ''
                    
                    job = {
                    'Title':title,
                    'Company':company,
                    'Location':location,
                    'Rating':rating,
                    'Salary':salary,
                    'Link':link
                    }
                    
                    jobs.append(job)
                
                self.next()
                time.sleep(5)
                    
            except:
                break
            
if __name__ == '__main__': 
    
    # Get user input
    job = input("Enter the name of the title:\n")
    place = input("Enter the location:\n")
    file = input("Export csv file as:\n")
    
    # Run the class
    jobs = []
    bot = WebScrapping(job, place)        
    bot.search()
    bot.container()
    bot.data()
    
    # Convert to csv file
    df = pd.DataFrame(jobs)
    df.to_csv(f'{file}.csv')
    
    print("Finished")
    
      