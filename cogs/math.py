import discord
from discord.ext import commands
import math
import time
from datetime import date
from discord.ext.commands import Context
from bin.Chemistry import *


from config.bot_info import *


Pi = math.pi


class math_handeling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self, ctx:Context, a:float, b:float):
        if a > 100000000 or b > 100000000 or a < -100000000 or b < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            c = a+b
            if (c % 1 == 0):
                c = int(c)
            else:
                round(c, 5)
            await ctx.send(c)

    @commands.command()
    async def subtract(self, ctx:Context, a:float , b:float):
        if a > 100000000 or b > 100000000 or a < -100000000 or b < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            c = a-b
            if (c % 1 == 0):
                c = int(c)
            else:
                round(c, 5)
            await ctx.send(c)

    @commands.command()
    async def mult(self, ctx:Context, a:float ,b:float):
        if a > 100000000 or b > 100000000 or a < -100000000 or b < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            c = a*b
            if (c % 1 == 0):
                c = int(c)
            else:
                round(c, 5)
            await ctx.send(c)

    @commands.command()
    async def abso(self, ctx:Context, a:float):
        if a > 100000000 or a < -100000000 :
            await ctx.send('數字太大了我算不了QQ')
        else:
            b = abs(a)
            if (b % 1 == 0):
                b = int(b)
            else:
                round(b, 5)
            await ctx.send(b)

    @commands.command(name = 'log')
    async def _log(self, ctx:Context, a:int, b:int = 10):
        if a > 100000000 or b > 100000000 or a < -100000000 or b < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            c = math.log(a, b)
            if c % 1 == 0:
                c = int(c)
            else:
                round(c,10)
            await ctx.send(c)

    @commands.command(name = 'sin')
    async def _sin(self, ctx:Context, a:int):
        if a > 100000000 or a < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            a = a/180*Pi
            b = math.sin(a)
            if b % 1 == 0:
                b = int(b)
            elif b == 0:
                b = int(b)
            else:
                b = round(b,10)
            await ctx.send(b)

    @commands.command(name = 'cos')
    async def _cos(self, ctx:Context, a:int):
        if a > 100000000 or a < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            a = a/180*Pi
            b = math.cos(a)
            if b % 1 == 0:
                b = int(b)
            elif b == 0:
                b = int(b)
            else:
                b = round(b,10)
            await ctx.send(b)

    @commands.command(name = 'tan')
    async def _tan(self, ctx:Context, a:int):
        if a > 100000000 or a < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            a = a/180*Pi
            b = math.tan(a)
            if b % 1 == 0:
                b = int(b)
            elif b == 0:
                b = int(b)
            else:
                b = round(b,10)
            await ctx.send(b)

    @commands.command(name = 'cot')
    async def _cot(self, ctx:Context, a:int):
        if a > 100000000 or a < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            a = a/180*Pi
            b = math.cos(a) / math.sin(a)
            if b % 1 == 0:
                b = int(b)
            elif b == 0:
                b = int(b)
            else:
                b = round(b,10)
            await ctx.send(b)

    @commands.command(name = 'sec')
    async def _sec(self, ctx:Context, a:int):
        if a > 100000000 or a < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            a = a/180*Pi
            b = 1/math.cos(a)
            if b % 1 == 0:
                b = int(b)
            elif b == 0:
                b = int(b)
            else:
                b = round(b,10)
            await ctx.send(b)

    @commands.command(name = 'csc')
    async def _csc(self, ctx:Context, a:int):
        if a > 100000000 or a < -100000000:
            await ctx.send('數字太大了我算不了QQ')
        else:
            a = a/180*Pi
            b = 1/math.sin(a)
            if b % 1 == 0:
                b = int(b)
            elif b == 0:
                b = int(b)
            else:
                b = round(b,10)
            await ctx.send(b)

    @commands.command(name ='Pi')
    async def PI(self, ctx):
        await ctx.send(round(Pi,30))

    @commands.command(name = 'average')
    async def average(self, ctx:Context,* , data = []):
        if len(data) == 0:
            await ctx.send(f'Appropriate usage : {pre}average <data1> <data2> ...')
        sum = 0
        data = [i for i in data if i!=' ']
        for i in data:
            sum = sum + int(i)
        n = len(data)
        output = sum / n
        await ctx.send(output)
    
    @commands.command(name = 'stdev')
    async def stdev(self, ctx:Context, *, data:str):
        if len(data) == 0:
            await ctx.send(f'Appropriate usage : {pre}stdev <data1> <data2> ...')
        sum = 0
        sum2 = 0
        tmp = data
        tmp = [i for i in data.split()]
        data = tmp
        n = len(data)
        for i in data:
            sum = sum + int(i)
            sum2 = sum2 + int(i)*int(i)
        stdev = math.pow(sum2 / n - (sum*sum) / (n*n), 0.5)
        await ctx.send(stdev)
    
    @commands.command(name = 'stronghold')
    async def stronghold(self, ctx:Context, x1, z1, Angle1, x2, z2, Angle2):
        x1 ,x2 = -eval(x1) ,-eval(x2)
        #x座標互換
        Angle1 , Angle2 = -eval(Angle1) + 90 , -eval(Angle2) + 90
        #角度轉換
        tanAngle1 , tanAngle2 = math.tan(Angle1/180*Pi) , math.tan(Angle2/180*Pi)
        #轉換斜率

        a1 ,a2 = tanAngle1 , tanAngle2
        b1 = b2 = -1
        c1 , c2 = (a1*x1) - eval(z1) , (a2*x2) - eval(z2)
        xFin = -((c2*b1)-(c1*b2))/((a2*b1)-(a1*b2))
        zFin = ((a1*c2)-(a2*c1))/((b2*a1)-(a2*b1))
        await ctx.send(f'/tp @p {xFin} ~ {zFin}')

    @commands.command(name = 'Cross product', aliases = ['cross'])
    async def Cross_product(self, ctx:Context, *, data):
        v = data.split()
        if len(v) < 4:
            embed = discord.Embed(
                title = 'Error!',
                description = 'Given too less data',
                color = discord.Color.blue()
            )
            embed.add_field(name = 'Value given:', value = f'{v}', inline = True)
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)

            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction('❌')
        elif (len(v) >= 4) and (len(v) % 2 == 0):
            v1 = []
            v2 = []
            for x in range(0 , int(len(v)/2)):
                v1.append(eval(v[x]))
            for x in range(int(len(v)/2), len(v)):
                v2.append(eval(v[x]))
            cross_product = []
            if len(v1) == 2:
                v1.append(0)
                v2.append(0)
                x = v1[1]*v2[2]-v2[1]*v1[2]
                y = -(v1[0]*v2[2]-v2[0]*v1[2])
                z = v1[0]*v2[1]-v2[0]*v1[1]
                cross_product.append(x)
                cross_product.append(y)
                cross_product.append(z)
            elif len(v1) == 3:
                x = v1[1]*v2[2]-v2[1]*v1[2]
                y = -(v1[0]*v2[2]-v2[0]*v1[2])
                z = v1[0]*v2[1]-v2[0]*v1[1]
                cross_product.append(x)
                cross_product.append(y)
                cross_product.append(z)
            
            cross_product_len = f'`{round(pow(pow(x, 2)+pow(y, 2)+pow(z, 2), 0.5), 3)}`'
            embed = discord.Embed(
                title = 'Cross Product:',
                description = 'The result',
                color = discord.Color.blue()
            )
            for index in range(len(v)):
                v[index] = int(v[index])
            embed.add_field(name = 'Value given:', value = f'{v}', inline = False)
            embed.add_field(name = 'Vector 1:', value = f'{v1}', inline = True)
            embed.add_field(name = 'Vector 2:', value = f'{v2}', inline = True)
            embed.add_field(name = 'v₁×v₂', value = cross_product, inline = False)
            embed.add_field(name = 'Approximate value of |v₁×v₂|', value = cross_product_len, inline = False)
            embed.add_field(name = 'Absolute form of |v₁×v₂|', value = f'`√({pow(x, 2)}+{pow(y, 2)}+{pow(z, 2)})`')
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)

            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction('✅')
            

        else:
            embed = discord.Embed(
                title = 'Error!',
                description = 'Unable to calculate the cross product',
                color = discord.Color.blue()
            )

            embed.add_field(name = 'Value given:', value = f'{v}', inline = True)
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)

            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction('❌')

    @commands.command(name = 'Inner product', aliases = ['dot'])
    async def Inner_product(self, ctx:Context, *, data):
        v = data.split()
        if len(v) < 2:
            embed = discord.Embed(
                title = 'Error!',
                description = 'Given too less data',
                color = discord.Color.blue()
            )
            embed.add_field(name = 'Value given:', value = f'{v}', inline = True)
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)

            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction('❌')
        elif (len(v) >= 2) and (len(v) % 2 == 0):
            v1 = []
            v2 = []
            for x in range(0 , int(len(v)/2)):
                v1.append(eval(v[x]))
            for x in range(int(len(v)/2), len(v)):
                v2.append(eval(v[x]))
            print(v1)
            print(v2)
            inner_product = 0
            v1_len = 0
            v2_len = 0

            for x in range(0 ,len(v1)):
                v1_len = v1_len + pow(v1[x], 2)
                v2_len = v2_len + pow(v2[x], 2)
                inner_product = v1[x]*v2[x] + inner_product
            
            cos_theta = (inner_product)/(v1_len*v2_len)

            embed = discord.Embed(
                title = 'Inner Product:',
                description = 'The result',
                color = discord.Color.blue()
            )

            embed.add_field(name = 'Value given:', value = f'{v}', inline = False)
            embed.add_field(name = 'Vector 1:', value = f'{v1}', inline = True)
            embed.add_field(name = 'Vector 2:', value = f'{v2}', inline = True)
            embed.add_field(name = 'v₁·v₂', value = inner_product, inline = False)
            embed.add_field(name = 'cosθ', value = cos_theta, inline = True)
            #embed.add_field(name = 'θ(rad)', value = math.acos(cos_theta), inline = True)
            
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)

            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction('✅')
            

        else:
            embed = discord.Embed(
                title = 'Error!',
                description = 'Unable to calculate the Inner product',
                color = discord.Color.blue()
            )

            embed.add_field(name = 'Value given:', value = f'{v}', inline = True)
            t = time.localtime()
            today = date.today()
            today_date = today.strftime("%Y/%m/%d")
            current_time = time.strftime("%H:%M:%S", t)

            embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
            message = await ctx.send(embed = embed)
            await message.add_reaction('❌')
            
    @commands.command()
    async def bmi(self, ctx:Context, weight, height):
        bmirate = eval(weight) / (eval(height)*eval(height))
        embed = discord.Embed(
            title = "BMI",
            description = "Body mass index",
            color = discord.Color.blue()
        )
        embed.add_field(name = "Your BMI", value = bmirate, inline=False)
        embed.add_field(name = "Reference", value = 'https://www.hpa.gov.tw/Pages/Detail.aspx?nodeid=542&pid=9737', inline = False)
        embed.set_image(url = 'https://i.imgur.com/P89sh78.png')
        t = time.localtime()
        today = date.today()
        today_date = today.strftime("%Y/%m/%d")
        current_time = time.strftime("%H:%M:%S", t)
        embed.set_footer(text = f"{default_footer} \n Sent at {today_date} , {current_time}", icon_url = self.client.get_user(My_user_id).avatar.url)
        return await ctx.send(embed = embed)

    @commands.command(name = 'concentration', aliases = ['concen', 'chemicals'])
    async def concentration(self, ctx:Context):
        msg:Message = await ctx.send('ouo')
        return await msg.edit(view = Concentration_choice(attached_msg = msg))

    @stronghold.error
    async def strong_hold_error(self, ctx:Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await  ctx.send(f'Appropriate usage: \n {pre}stronghold <x1> <z1> <angle1> <x2> <z2> <angle2>')


async def setup(client):
    await client.add_cog(math_handeling(client))