from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

def get_links(driver, domain, section_url):
    """
    Extract all internal links on a webpage within the specified section and return a set of URLs.
    """
    links = set()
    try:
        anchor_tags = driver.find_elements(By.TAG_NAME, 'a')
        for tag in anchor_tags:
            href = tag.get_attribute('href')
            if href and domain in href and section_url in href:
                links.add(href)
    except Exception as e:
        print(f"Error extracting links: {e}")
    return links

def get_text_from_url(driver, url):
    """
    Extract text from div elements with class 'main' and their sub-elements,
    excluding divs with id 'cookies-modal', and join them as complete words.
    """
    try:
        driver.get(url)
        time.sleep(2)  # Adjust based on page load time
        
        main_divs = driver.find_elements(By.CLASS_NAME, 'col-md-8')
        texts = []

        for main_div in main_divs:
            if main_div.get_attribute('id') != 'cookies-modal':
               
                str = main_div.text.strip() 
                if str:
                    texts.append(str)
                else:
                     str = main_div.get_attribute("innerText")
                     texts.append(str)

        return ' '.join(texts)
    except Exception as e:
        print(f"Error extracting text from URL {url}: {e}")
        return ""

def crawl_and_store(start_url, domain, section_url, csv_filename):
    """
    Crawl a website starting from a URL within a specific section and store the content in a CSV file.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Running in headless mode
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        with webdriver.Chrome(options=options) as driver, open(csv_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            visited = set()
            queue = set([start_url])

            while queue:
                current_url = queue.pop()
                visited.add(current_url)
                text_content = get_text_from_url(driver, current_url)
                
                # Write each row as a list of two elements: URL and text content
                if text_content!="":
                    writer.writerow([current_url, text_content])

                links = get_links(driver, domain, section_url)
                queue = queue.union(links - visited)
    except Exception as e:
        print(f"Error during crawling and storing: {e}")

# Starting URL, domain, and section
start_url = 'https://www.limassol.org.cy/'
domain = 'limassol.org.cy'
section_url = '/el/'

# File path for CSV output
csv_file_path_selenium = 'C:\\Users\\GeorgeChalkiadakis\\OneDrive - k2d properties LTD\\Documents\\Projects\\crwalmayor\\limassol_website_content_selenium.csv'

# Run the crawler with Selenium
crawl_and_store(start_url, domain, section_url, csv_file_path_selenium)
