from discord.ui import Button, View
from typing import List, Dict
from discord import User


class Poll_sys_view(View):
    def __init__(self):
        super().__init__(timeout = None)
        self.choices:List[Dict[User, str]] = []