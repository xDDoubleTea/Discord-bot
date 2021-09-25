import discord
from discord.ext import commands
import math

pre = 'a!'

Pi = math.pi


class math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def add(self, ctx, a:float, b:float):
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
    async def subtract(self, ctx, a:float , b:float):
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
    async def mult(self, ctx, a:float ,b:float):
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
    async def abso(self, ctx, a:float):
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
    async def _log(self, ctx, a:int, b:int = 10):
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
    async def _sin(self, ctx, a:int):
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
    async def _cos(self, ctx, a:int):
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
    async def _tan(self, ctx, a:int):
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
    async def _cot(self, ctx, a:int):
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
    async def _sec(self, ctx, a:int):
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
    async def _csc(self, ctx, a:int):
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
    async def average(self, ctx,* , data = []):
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
    async def stdev(self, ctx, *, data = []):
        if len(data) == 0:
            await ctx.send(f'Appropriate usage : {pre}average <data1> <data2> ...')
        sum = 0
        sum2 = 0
        data = [i for i in data if i!=' ']
        n = len(data)
        for i in data:
            sum = sum + int(i)
            sum2 = sum2 + int(i)*int(i)
        stdev = math.sqrt(sum2 / n - (sum*sum) / (n*n))
        await ctx.send(stdev)
    
    @commands.command(name = 'stronghold')
    async def stronghold(self, ctx, x1, z1, Angle1, x2, z2, Angle2):
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

    @stronghold.error
    async def strong_hold_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await  ctx.send(f'Appropriate usage: \n {pre}stronghold <x1> <z1> <angle1> <x2> <z2> <angle2>')


def setup(client):
    client.add_cog(math(client))