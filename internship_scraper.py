import os
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

# LinkedIn Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)
@app.route("/")
def home():
    return "Internship Scraper API is running. Visit /internships to get data."


# ---------- Internshala ----------
def scrape_internshala():
    url = "https://internshala.com/internships/keywords-computer-science"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    internships = []
    cards = soup.find_all("div", class_="individual_internship")
    for card in cards[:10]:
        try:
            title = card.find("div", class_="heading_4_5").get_text(strip=True)
            company = card.find("a", class_="link_display_like_text").get_text(strip=True)
            location = card.find("a", class_="location_link").get_text(strip=True)
            stipend = card.find("span", class_="stipend").get_text(strip=True)
            duration = card.find_all("div", class_="item_body")[1].get_text(strip=True)
            link = "https://internshala.com" + card.find("a")["href"]
            internships.append({
                "source": "Internshala",
                "title": title,
                "company": company,
                "location": location,
                "stipend": stipend,
                "duration": duration,
                "link": link,
                "deadline": "See on site"
            })
        except:
            continue
    return internships

# ---------- LetsIntern ----------
def scrape_letsintern():
    url = "https://www.letsintern.com/internships/computer-science-internships"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    internships = []
    cards = soup.find_all("div", class_="internship_detail")
    for card in cards[:5]:
        try:
            title = card.find("a", class_="profile").get_text(strip=True)
            company = card.find("a", class_="org_name").get_text(strip=True)
            location = card.find("span", class_="location").get_text(strip=True)
            link = "https://www.letsintern.com" + card.find("a", class_="profile")["href"]
            internships.append({
                "source": "LetsIntern",
                "title": title,
                "company": company,
                "location": location,
                "stipend": "Check site",
                "duration": "Varies",
                "link": link,
                "deadline": "Check on site"
            })
        except:
            continue
    return internships

# ---------- HelloIntern ----------
def scrape_hellointern():
    url = "https://www.hellointern.com/internships"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    internships = []
    cards = soup.find_all("div", class_="internship-item")
    for card in cards[:5]:
        try:
            title = card.find("h4").get_text(strip=True)
            company = card.find("h5").get_text(strip=True)
            location = card.find("li", class_="internship-location").get_text(strip=True)
            stipend = card.find("li", class_="internship-stipend").get_text(strip=True)
            duration = card.find("li", class_="internship-duration").get_text(strip=True)
            link = "https://www.hellointern.com" + card.find("a")["href"]
            internships.append({
                "source": "HelloIntern",
                "title": title,
                "company": company,
                "location": location,
                "stipend": stipend,
                "duration": duration,
                "link": link,
                "deadline": "Check on site"
            })
        except:
            continue
    return internships

# ---------- LinkedIn (Selenium) ----------
def scrape_linkedin_internships():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.linkedin.com/jobs/internships/?keywords=computer%20science")
    internships = []

    time.sleep(5)  # wait for JS content to load
    try:
        job_cards = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
        for card in job_cards[:5]:
            try:
                title = card.find_element(By.CSS_SELECTOR, "a.job-card-list__title").text
                company = card.find_element(By.CSS_SELECTOR, "a.job-card-container__company-name").text
                location = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
                link = card.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute("href")
                internships.append({
                    "source": "LinkedIn",
                    "title": title,
                    "company": company,
                    "location": location,
                    "stipend": "Not Listed",
                    "duration": "Not Listed",
                    "link": link,
                    "deadline": "Apply Soon"
                })
            except:
                continue
    except Exception as e:
        print(f"[LinkedIn Error] {e}")
    finally:
        driver.quit()
    return internships

# ---------- Flask Route ----------
@app.route('/internships')
def internships():
    combined = []
    combined.extend(scrape_internshala())
    combined.extend(scrape_letsintern())
    combined.extend(scrape_hellointern())
    combined.extend(scrape_linkedin_internships())
    return jsonify(combined)

# ---------- Main ----------
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

