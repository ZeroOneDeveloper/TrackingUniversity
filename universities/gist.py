from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "https://ratio.uwayapply.com/Sl5KbzBlbyZlbyVlb3JlSl4lJjomSiNmVGY="

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")
    current = soup.select_one("#table > table:nth-child(4) > tbody:nth-child(3)")
    updatedAt = soup.select_one("#ID_DateStr > label").text.strip()

    GIST = CompetitionRate(
        universityName="GIST",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(119, 34, 46),
    )

    for tr in current.select("tr"):
        tds = tr.select("td")
        GIST.addParagon(
            paragon=tds[0].text,
            totalMember=tds[1].text,
            member=tds[2].text,
            competitionRate=tds[3].text,
        )

    return GIST
