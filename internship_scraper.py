
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/internships')
def internships():
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

    return jsonify(internships)

if __name__ == "__main__":
    app.run(debug=True)
