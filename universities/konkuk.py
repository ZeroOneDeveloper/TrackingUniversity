from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10080231.html"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text(encoding="utf-8")
    soup = BeautifulSoup(response, "html.parser")

    current = soup.select("#Ratio10080231 > div:nth-child(1) > table > tr")
    updatedAt = soup.select_one("#RatioTime").text.strip()

    Konkuk = CompetitionRate(
        universityName="건국대학교(서울)",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(3, 107, 41),
    )

    for tr in current[1:]:
        tds = tr.select("td")
        try:
            Konkuk.addParagon(
                paragon=tds[1].text,
                totalMember=tds[2].text,
                member=tds[3].text,
                competitionRate=tds[4].text,
            )
        except IndexError:
            Konkuk.addParagon(
                paragon=tds[0].text,
                totalMember=tds[1].text,
                member=tds[2].text,
                competitionRate=tds[3].text,
            )

    return Konkuk
