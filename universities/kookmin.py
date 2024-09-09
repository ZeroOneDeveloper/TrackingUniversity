from bs4 import BeautifulSoup
from aiohttp import ClientSession

from dataStructure import CompetitionRate


async def main() -> CompetitionRate:
    url = "https://ratio.uwayapply.com/Sl5KVyVNOWFhOUpmJSY6JkojZlRm"

    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.text()
    soup = BeautifulSoup(response, "html.parser")

    current = soup.select_one("#table > table > tbody:nth-child(3)")
    updatedAt = soup.select_one("#ID_DateStr > label").text.strip()

    Kookmin = CompetitionRate(
        universityName="국민대학교",
        siteUri=url,
        updatedAt=updatedAt,
        universityColor=(255, 206, 68),
    )

    for tr in current.select("tr"):
        tds = tr.select("td")

        if tds[3].text.strip() == "-":
            continue

        Kookmin.addParagon(
            paragon=tds[0].text,
            totalMember=tds[1].text,
            member=tds[2].text,
            competitionRate=tds[3].text,
        )

    return Kookmin
