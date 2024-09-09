import requests
from bs4 import BeautifulSoup

from dataStructure import CompetitionRate


url = "https://ratio.uwayapply.com/Sl5KVyVNOWFhOUpmJSY6JkojZlRm"

response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")


current = soup.select_one("#table > table > tbody:nth-child(3)")


University = CompetitionRate(
    universityName="가천대학교",
    siteUri=url,
    universityColor=(0, 65, 145),
)

for tr in current.select("tr"):
    tds = tr.select("td")

    if tds[3].text.strip() == "-":
        continue

    University.addParagon(
        paragon=tds[0].text,
        totalMember=tds[1].text,
        member=tds[2].text,
        competitionRate=tds[3].text,
    )


print(University.toList())
