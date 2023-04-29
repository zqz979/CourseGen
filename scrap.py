import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape
base_url = "https://bulletins.psu.edu"
undergrad_url = base_url + "/university-course-descriptions/undergraduate/"
grad_url = base_url + "/university-course-descriptions/graduate/"

# scrape undergrad courses
response = requests.get(undergrad_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all the sub-URLs
sub_urls = []
nav_list = soup.find("ul", {"class": "nav leveltwo", "id": "/university-course-descriptions/undergraduate/"})
for li in nav_list.find_all("li"):
    sub_url = li.find("a").get("href")
    sub_urls.append(sub_url)
    
courses = []

# Scrape the course information from each sub-URL
for sub_url in sub_urls:
    response = requests.get(base_url + sub_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all the course title and description pairs
    course_blocks = soup.find_all("div", {"class": "courseblock"})
    
    for block in course_blocks:
        title = block.find("div", {"class": "course_codetitle"}).text.strip()
        description_tag = block.find("div", {"class": "courseblockdesc"})
        
        
        if description_tag is not None:
            # Remove links from the description
            for link in description_tag.find_all('a'):
                link.decompose()
        
            # Get the text of the description without links
            description = description_tag.text.strip()
        
            course = {"title": title, "description": description}
            courses.append(course)


# scrape grad courses
response = requests.get(grad_url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all the sub-URLs
sub_urls = []
nav_list = soup.find("ul", {"class": "nav leveltwo", "id": "/university-course-descriptions/graduate/"})
for li in nav_list.find_all("li"):
    sub_url = li.find("a").get("href")
    sub_urls.append(sub_url)

# Scrape the course information from each sub-URL
for sub_url in sub_urls:
    response = requests.get(base_url + sub_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all the course title and description pairs
    course_blocks = soup.find_all("div", {"class": "courseblock"})
    
    for block in course_blocks:
        title = block.find("div", {"class": "course_codetitle"}).text.strip()
        description_tag = block.find("div", {"class": "courseblockdesc"})
        
        
        if description_tag is not None:
            # Remove links from the description
            for link in description_tag.find_all('a'):
                link.decompose()
        
            # Get the text of the description without links
            description = description_tag.text.strip()
        
            course = {"title": title, "description": description}
            courses.append(course)

file_path = "./data/courses.csv"

with open(file_path, mode="w", encoding="utf-8", newline="") as csv_file:
    fieldnames = ["title", "description"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for course in courses:
        writer.writerow(course)

