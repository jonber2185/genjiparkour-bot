import discord
from discord import ui
from db.entities import ClearEntity


class PaginationView(ui.View):
    def __init__(self, data_list: list[ClearEntity], default_embed=discord.Embed, per_page: int = 10):
        super().__init__(timeout=60)
        self.default_embed = default_embed
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

        current_diff = ""
        for clear_info in page_data:
            clear_diff = clear_info.difficulty.value.replace("+", "").replace("-", "")
            if clear_diff != current_diff:
                self.default_embed.add_field(name=f"• {clear_diff}", value="", inline=False)
                current_diff = clear_diff
                
            self.default_embed.add_field(
                name="", 
                value=f"> 코드 : **`{clear_info.code}`**\n"
                    f"> 난이도 : {clear_info.difficulty.value}\n"
                    f"> 클리어타임 : ***{clear_info.clear_time:.2f}초***\n",
                inline=False
            )

        self.default_embed.set_footer(text=f"페이지 {self.current_page + 1} / {self.total_pages}")
        return self.default_embed

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