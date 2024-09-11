from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10920311.html"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")

    current = soup.select_one("#Ratio1092031 > div:nth-child(2) > table")
    updatedAt = soup.select_one("#RatioTime").text.strip()

    Sungkyunkwan = CompetitionRate(
        universityName="성균관대학교",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(141, 198, 63),
    )

    for tr in current.select("tr")[1:]:
        tds = tr.select("td")
        Sungkyunkwan.addParagon(
            paragon=tds[0].text,
            totalMember=tds[1].text,
            member=tds[2].text,
            competitionRate=tds[3].text,
        )

    return Sungkyunkwan
