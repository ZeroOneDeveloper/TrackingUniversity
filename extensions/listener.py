from discord.ext import commands, tasks
from discord import Embed, TextChannel, Color

import os
import json

from main import ControlSystem
from dataStructure import CompetitionRate


class Listener(commands.Cog):
    def __init__(self, bot: ControlSystem):
        self.bot = bot
        self.collectCompetitionRate.start()

    @tasks.loop(minutes=1)
    async def collectCompetitionRate(self):
        with open(file="./universitiesData.json", mode="r", encoding="utf-8") as f:
            universitiesData = json.load(f)
        LOG_CHANNEL: TextChannel = self.bot.get_channel(int(os.getenv("LOG_CHANNEL")))
        if LOG_CHANNEL is None:
            return
        for university in os.listdir("./universities"):
            if university.endswith(".py"):
                try:
                    main: callable = __import__(
                        f"universities.{university[:-3]}", fromlist=[""]
                    ).main
                except AttributeError:
                    continue
                else:
                    competitionRate: CompetitionRate = await main()
                    if (
                        universitiesData.get(competitionRate.name) is None
                        or competitionRate.updatedAt
                        != universitiesData[competitionRate.name]["updatedAt"]
                    ):
                        embed = Embed(
                            title=f"[{competitionRate.name}] 대학교 입시 경쟁률",
                            description=f"자세한 정보는 [여기]({competitionRate.siteUri})에서 확인하세요.",
                            color=Color.from_rgb(*competitionRate.universityColor),
                        )
                        for paragon in competitionRate.toList():
                            embed.add_field(
                                name=paragon[0],
                                value=f"모집인원: {paragon[1]}\n지원인원: {paragon[2]}\n경쟁률: {paragon[3]}",
                                inline=True,
                            )
                        embed.set_footer(
                            text="마지막 업데이트: " + competitionRate.updatedAt
                        )
                        await LOG_CHANNEL.send(
                            content=", ".join(
                                list(
                                    map(
                                        lambda userId: f"<@{userId}>",
                                        universitiesData[competitionRate.name][
                                            "trackedMembers"
                                        ],
                                    )
                                )
                                if universitiesData.get(competitionRate.name)
                                else []
                            ),
                            embed=embed,
                        )
                        universitiesData[competitionRate.name] = {
                            "updatedAt": competitionRate.updatedAt,
                            "siteUri": competitionRate.siteUri,
                            "paragons": competitionRate.toList(),
                            "trackedMembers": (
                                universitiesData[competitionRate.name]["trackedMembers"]
                                if universitiesData.get(competitionRate.name)
                                is not None
                                else []
                            ),
                        }
            with open(file="./universitiesData.json", mode="w", encoding="utf-8") as f:
                json.dump(universitiesData, f, ensure_ascii=False, indent=4)


async def setup(bot: ControlSystem):
    await bot.add_cog(Listener(bot))
