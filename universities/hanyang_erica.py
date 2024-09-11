from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio11650561.html"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")
    
    current = soup.select_one("#Ratio11650561 > div:nth-child(1) > table")
    updatedAt = soup.select_one("#RatioTime").text.strip()

    Hanyang = CompetitionRate(
        universityName="한양대학교(ERICA)",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(14,74,132),
    )

    for tr in current.select("tr")[1:]:
        tds = tr.select("td")
        Hanyang.addParagon(
                paragon=tds[0].text,
                totalMember=tds[1].text,
                member=tds[2].text,
                competitionRate=tds[3].text,
            )

    return Hanyang
