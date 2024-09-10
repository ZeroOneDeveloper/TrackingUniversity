from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "http://ratio.uwayapply.com/Sl5KTjlKZiUmOiZKI2ZUZg=="

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")
    current = soup.select_one("#table > table > tbody:nth-child(3)")
    updatedAt = soup.select_one("#ID_DateStr > label").text.strip()

    Kwangwoon = CompetitionRate(
        universityName="광운대학교",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(119, 34, 46),
    )

    for tr in current.select("tr")[1:]:
        tds = tr.select("td")
        Kwangwoon.addParagon(
            paragon=tds[0].text,
            totalMember=tds[1].text,
            member=tds[2].text,
            competitionRate=tds[3].text,
        )

    return Kwangwoon
