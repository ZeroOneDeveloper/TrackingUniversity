from discord import User, Forbidden
from discord.ext import commands
from discord.ext.commands.context import Context

import os
import json

from main import ControlSystem


class Command(commands.Cog):
    def __init__(self, bot: ControlSystem):
        self.bot = bot

    @commands.group(name="대학교")
    async def university(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return

    @university.command(name="신청")
    @commands.cooldown(1, 60 * 10, commands.BucketType.user)
    async def request(self, ctx: Context, name: str):
        await ctx.send(f"신청 완료: `{name}` 대학\n관리자가 확인 후 등록합니다.")
        owner: User = self.bot.get_user(int(os.getenv("OWNER_ID")))
        await owner.send(f"{ctx.author}님이 `{name}` 대학교를 신청하셨습니다.")

    @university.command(name="목록")
    async def list(self, ctx: Context):
        if ctx.guild is not None:
            await ctx.reply(content="대학교 목록을 불러옵니다.\nDM을 확인해주세요!")
        try:
            with open(file="./universitiesData.json", mode="r", encoding="utf-8") as f:
                universitiesData = json.load(f)
            await ctx.author.send(
                content="\n".join(
                    list(
                        map(
                            lambda university: f"{university} ({universitiesData[university]['updatedAt']})",
                            universitiesData.keys(),
                        )
                    )
                )
            )
        except FileNotFoundError:
            return
        except Forbidden:
            return

    @university.command(name="추적")
    async def track(self, ctx: Context, name: str):
        with open(file="./universitiesData.json", mode="r", encoding="utf-8") as f:
            universitiesData = json.load(f)
        if universitiesData.get(name) is None:
            await ctx.send(f"존재하지 않는 대학교: `{name}`")
            return
        if universitiesData[name]["trackedMembers"].count(str(ctx.author.id)) > 0:
            await ctx.send(f"이미 추적 중인 대학교: `{name}`")
            return
        universitiesData[name]["trackedMembers"].append(str(ctx.author.id))
        await ctx.send(
            f"추적 완료: `{name}` 대학\n해당 대학교의 입시 경쟁률을 추적합니다."
        )
        with open(file="./universitiesData.json", mode="w", encoding="utf-8") as f:
            json.dump(universitiesData, f, ensure_ascii=False, indent=4)


    @university.command(name="추적해제")
    async def untrack(self, ctx: Context, name: str):
        with open(file="./universitiesData.json", mode="r", encoding="utf-8") as f:
            universitiesData = json.load(f)
        if universitiesData.get(name) is None:
            await ctx.send(f"존재하지 않는 대학교: `{name}`")
            return
        if universitiesData[name]["trackedMembers"].count(str(ctx.author.id)) == 0:
            await ctx.send(f"추적 중이지 않은 대학교: `{name}`")
            return
        universitiesData[name]["trackedMembers"].remove(str(ctx.author.id))
        await ctx.send(
            f"추적 해제: `{name}` 대학\n해당 대학교의 입시 경쟁률 추적을 중단합니다."
        )
        with open(file="./universitiesData.json", mode="w", encoding="utf-8") as f:
            json.dump(universitiesData, f, ensure_ascii=False, indent=4)


async def setup(bot: ControlSystem):
    await bot.add_cog(Command(bot))
