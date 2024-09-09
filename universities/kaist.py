from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://ratio.uwayapply.com/Sl5KMCYlODlKXiUmOiZKI2ZUZg=="

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")
    current = soup.select_one("#table > table:nth-child(4) > tbody:nth-child(3)")
    updatedAt = soup.select_one("#ID_DateStr > label").text.strip()

    KAIST = CompetitionRate(
        universityName="KAIST",
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
