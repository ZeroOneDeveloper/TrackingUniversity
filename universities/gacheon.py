from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10190421.html"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text(encoding="utf-8")
    soup = BeautifulSoup(response, "html.parser")

    current = soup.select("#Ratio1019042 > div:nth-child(1) > table > tr")
    updatedAt = soup.select_one("#RatioTime").text.strip()

    Gacheon = CompetitionRate(
        universityName="가천대학교",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(250, 166, 53),
    )

    for tr in current[1:]:
        tds = tr.select("td")
        try:
            Gacheon.addParagon(
                paragon=tds[1].text,
                totalMember=tds[2].text,
                member=tds[3].text,
                competitionRate=tds[4].text,
            )
        except IndexError:
            Gacheon.addParagon(
                paragon=tds[0].text,
                totalMember=tds[1].text,
                member=tds[2].text,
                competitionRate=tds[3].text,
            )

    return Gacheon
