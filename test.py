import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://addon.jinhakapply.com/RatioV1/RatioH/Ratio10080231.html"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")
    current = soup.select_one("#table > table:nth-child(5) > tbody:nth-child(3)")
    updatedAt = soup.select_one("#ID_DateStr > label").text.strip()

    KAIST = CompetitionRate(
        universityName="건국대학교(서울)",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(0, 65, 145),
    )

    for tr in current.select("tr"):
        tds = tr.select("td")
        KAIST.addParagon(
            paragon=tds[0].text,
            totalMember=tds[1].text,
            member=tds[2].text,
            competitionRate=tds[3].text,
        )

    return KAIST

print(asyncio.run(main()).toList())