import discord
from discord.ext import commands

import mysql.connector



class memjoin(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        Kanatadb = mysql.connector.connect(
        host='localhost',
        database='kanata',
        password='ImSingleDog1',
        user='root'
        )
        cursor = Kanatadb.cursor()
        sql = 'SELECT * FROM welcome_channel'
        cursor.execute(sql)
        wel_channel_info = cursor.fetchall()
        send_wm = 0
        has_guild = False
        guild_id = 0
        index = 0
        for x,i in enumerate(wel_channel_info):
            if str(member.guild.id) == i[0]:
                has_guild = True
                index = x
                guild_id = int(i[0])
                break
        
        if has_guild:
            guild = self.client.get_guild(guild_id)
            channel = self.client.get_channel(int(wel_channel_info[index][1]))
            raw_msg = wel_channel_info[index][2]
            if raw_msg.startswith('{'):
                rm_front = raw_msg.split('{')
                all_element = []
                all_str = []
                for i in rm_front:
                    all_element.append(i.split('}')[0])
                    if len(i.split('}'))>1:
                        all_str.append(i.split('}')[1])

                
                output_str = ''
                if len(all_element) > len(all_str):
                    for i in range(len(all_element)):
                        if all_element[i] == 'member':
                            output_str += member.mention
                        elif all_element[i] == 'guild':
                            output_str += guild.name
                        elif all_element[i] == 'member_number':
                            output_str += str(len(member.guild.members))
                        
                        if i < len(all_str):
                            output_str += all_str[i]
                        
                elif len(all_element) < len(all_str):
                    for i in range(len(all_str)):
                        if i < len(all_element):
                            if all_element[i] == 'member':
                                output_str += member.mention
                            elif all_element[i] == 'guild':
                                output_str += guild.name
                            elif all_element[i] == 'member_number':
                                output_str += str(len(member.guild.members))
                        
                        output_str += all_str[i]

                elif len(all_element) == len(all_str):
                    for i in range(len(all_element)):
                        if all_element[i] == 'member':
                            output_str += member.mention
                        elif all_element[i] == 'guild':
                            output_str += guild.nam
                        elif all_element[i] == 'member_number':
                            output_str += str(len(member.guild.members))

                        output_str += all_str[i]


            else:
                rm_front = raw_msg.split('{')
                all_element = []
                all_str = []
                for i in rm_front:
                    all_element.append(i.split('}')[0])
                    if len(i.split('}'))>1:
                        all_str.append(i.split('}')[1])

                all_str.insert(0, all_element[0])
                all_element.pop(0)
                output_str = ""

                if len(all_element) > len(all_str):
                    for i in range(len(all_element)):
                        if i < len(all_str):
                            output_str += all_str[i]

                        if all_element[i] == 'member':
                            output_str+=member.mention
                        elif all_element[i] == 'guild':
                            output_str+=guild.name
                        elif all_element[i] == 'member_number':
                            output_str += str(len(member.guild.members))

                elif len(all_element) < len(all_str):
                    for i in range(len(all_str)):
                        output_str += all_str[i]
                        if i < len(all_element):
                            if all_element[i] == 'member':
                                output_str += member.mention
                            elif all_element[i] == 'guild':
                                output_str += guild.name
                            elif all_element[i] == 'member_number':
                                output_str += str(len(member.guild.members))                        

                elif len(all_element) == len(all_str):
                    for i in range(len(all_element)):
                        output_str += all_str[i]
                        
                        if all_element[i] == 'member':
                            output_str += member.mention
                        elif all_element[i] == 'guild':
                            output_str += guild.name
                        elif all_element[i] == 'member_number':
                            output_str += str(len(member.guild.members))
                        
            send_wm = await channel.send(output_str)
#-------------------------------------roles------------------------------------------------
        guild_id = member.guild.id
        cursor = Kanatadb.cursor()
        sql = 'SELECT * FROM default_role'
        cursor.execute(sql)
        role_info = cursor.fetchall()
        has_guild = False
        default_role = 0
        for guilds in role_info:
            if guilds[0] == str(guild_id):
                has_guild = True
                default_role = int(guilds[1])
                break

        if has_guild:
            for i in member.guild.roles:
                if i.id == default_role:
                    default_role = i
                    break
            await member.add_roles(default_role)
            if send_wm != 0:
                await channel.send(f'已將{member.mention}添加{default_role.name}身分組!')

async def setup(client):
    await client.add_cog(memjoin(client))