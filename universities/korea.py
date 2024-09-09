from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "https://ratio.uwayapply.com/Sl5KOGB9YTlKZiUmOiZKI2ZUZg=="

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")
    current = soup.select_one("#table > table:nth-child(5) > tbody:nth-child(3)")
    updatedAt = soup.select_one("#ID_DateStr > label").text.strip()

    KOREA = CompetitionRate(
        universityName="고려대학교",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(134, 38, 51),
    )

    for tr in current.select("tr"):
        tds = tr.select("td")
        KOREA.addParagon(
            paragon=tds[0].text,
            totalMember=tds[1].text,
            member=tds[2].text,
            competitionRate=tds[3].text,
        )

    return KOREA
