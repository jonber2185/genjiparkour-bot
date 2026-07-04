import discord
from discord import ui
from db.entities import CodeEntity


class PaginationView(ui.View):
    def __init__(self, data_list: list[CodeEntity], per_page: int = 10):
        super().__init__(timeout=60)
        self.data_list = data_list
        self.per_page = per_page
        self.current_page = 0
        self.total_pages = (len(data_list) - 1) // per_page + 1
        self.message: discord.Message = None
        self.update_buttons()

    def update_buttons(self):
        self.prev_btn.disabled = self.current_page == 0
        self.next_btn.disabled = self.current_page == self.total_pages - 1

    async def on_timeout(self) -> None:
        if not self.message:
            return
        for item in self.children:
            if isinstance(item, ui.Button):
                item.disabled = True
        self.next_btn.label = "⏱️ 조회 시간이 만료되었습니다."
        try:
            await self.message.edit(view=self)
        except discord.HTTPException:
            pass

    def make_embed(self) -> discord.Embed:
        start = self.current_page * self.per_page
        page_data = self.data_list[start:start + self.per_page]

        embed = discord.Embed(
            title="📂 코드 목록",
            description="현재 등록된 플레이 가능한 코드 리스트입니다.\n",
            color=discord.Color.green(),
        )

        current_map = ""
        for code in page_data:
            if code.map_name != current_map:
                embed.add_field(name=f"• {code.map_name}", value="", inline=False)
                current_map = code.map_name

            creator = code.creator
            if "(@" in creator:
                creator = creator[:creator.find("(@")]

            clear_time = f"*#{code.clear_time}초*" if code.clear_time else ""

            lines = [
                f"> 코드 : **`{code.code}` {clear_time}**",
                f"> 난이도: {code.difficulty.value}",
            ]
            if code.cp:          lines.append(f"> 체크포인트 : {code.cp}cp")
            if code.description: lines.append(f"> 설명 : {code.description}")
            lines.append(f"> 제작자 : {creator}")
            if code.guide:       lines.append(f"> [가이드]({code.guide})")

            embed.add_field(name="", value="\n".join(lines), inline=False)

        embed.set_footer(text=f"페이지 {self.current_page + 1} / {self.total_pages}")
        return embed

    @ui.button(label="이전", style=discord.ButtonStyle.grey)
    async def prev_btn(self, interaction: discord.Interaction, button: ui.Button):
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.make_embed(), view=self)

    @ui.button(label="다음", style=discord.ButtonStyle.grey)
    async def next_btn(self, interaction: discord.Interaction, button: ui.Button):
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.make_embed(), view=self)