# -*- coding: utf-8 -*-
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, cooldown, command, helper, usage
from bobotinho.utils.rand import random_choice, random_line_from_txt, random_number


class Rand(Cog):
    """Randômicos

    Comandos resultantes da aleatoriedade que podem ser usados para decidir algo
    """

    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot

    @helper("receba uma probabilidade de 0 a 100")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["%"])
    async def chance(self, ctx: Context) -> None:
        percentage = random_number(max=1000, div=10)
        return await ctx.reply(f"{percentage}%")

    @helper('dê opções separadas por "ou" (ou vírgulas, ou espaço) e uma delas será escolhida')
    @usage("para usar: %choice <list_de_opcoes>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["choose", "pick"])
    async def choice(self, ctx: Context, *, content: str) -> None:
        content = content.rstrip("?")
        sep = " ou " if " ou " in content else ", " if ", " in content else " " if " " in content else ""
        option = random_choice(content, sep=sep)
        return await ctx.reply(f"eu escolhi: {option}")

    @helper("jogue uma moeda e veja se deu cara ou coroa")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["coinflip", "cf"])
    async def coin(self, ctx: Context) -> None:
        percentage = random_number(max=6000)  # Murray & Teare (1993)
        if percentage > 3000:
            return await ctx.reply("você jogou uma moeda e ela caiu em cara")
        if percentage < 3000:
            return await ctx.reply("você jogou uma moeda e ela caiu em coroa")
        return await ctx.reply("você jogou uma moeda e ela caiu no meio, em pé! PogChamp PogChamp")

    @helper("receba uma piada ou trocadilho")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["joke", "4head", "hahaa"])
    async def randomjoke(self, ctx: Context) -> None:
        joke = random_line_from_txt("bobotinho//data//jokes.txt")
        return await ctx.reply(f"{joke} 4Head")

    @helper("tente vencer no pedra, papel e tesoura")
    @usage("para usar: %jokenpo <pedra|papel|tesoura>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["jokempo"])
    async def jokenpo(self, ctx: Context, choice: str) -> None:
        choice = (
            choice
            .replace("✊", "pedra")
            .replace("✋", "papel")
            .replace("✌️", "tesoura")
            .replace("✌", "tesoura")
        )
        i = random_number(min=0, max=2)
        options = ["papel", "pedra", "tesoura", "papel"]
        option = options[i]
        if choice == option:
            return await ctx.reply(f"eu também escolhi {option}, nós empatamos...")
        elif (choice, option) in [options[0:2], options[1:3], options[2:4]]:
            return await ctx.reply(f"eu escolhi {option}, você deu sorte dessa vez")
        elif (option, choice) in [options[::-1][0:2], options[::-1][1:3], options[::-1][2:4]]:
            return await ctx.reply(f"eu escolhi {option} e consegui te vencer facilmente")

    @helper("tenha sua pergunta respondida por uma previsão")
    @usage("para usar: %8ball <pergunta>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["8ball"])
    async def magicball(self, ctx: Context) -> None:
        predictions = [
            "ao meu ver, sim",
            "com certeza",
            "com certeza não",
            "concentre-se e pergunte novamente",
            "decididamente sim",
            "definitivamente sim",
            "dificilmente",
            "é complicado...",
            "é melhor você não saber",
            "fontes dizem que não",
            "impossível isso acontecer",
            "impossível prever isso",
            "jamais",
            "muito duvidoso",
            "nunca",
            "não",
            "não conte com isso",
            "não é possível prever isso",
            "pergunta nebulosa, tente novamente",
            "pergunte novamente mais tarde...",
            "pode apostar que sim",
            "possivelmente",
            "provavelmente...",
            "sem dúvidas",
            "sim",
            "sinais apontam que sim",
            "talvez",
            "você ainda tem dúvidas?",
            "você não acreditaria...",
        ]
        prediction = random_choice(predictions)
        return await ctx.reply(f"{prediction} 🎱")

    @helper("gere uma cor hexadecimal aleatória")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["rcg"])
    async def randomcolor(self, ctx: Context) -> None:
        color = random_number(max=0xFFFFFF)
        return await ctx.reply(f"aqui está uma cor aleatória: #{color:06X}")

    @helper("gere um número aleatório dentre o intervalo fornecido")
    @usage("para usar: %rng <valor_minimo> <valor_maximo>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["rng"])
    async def randomnumber(self, ctx: Context, min: int = 1, max: int = 100) -> None:
        if min > max:
            min, max = max, min
        number = random_number(min=min, max=max)
        return await ctx.reply(f"aqui está um número entre {min} e {max}: {number}")

    @helper("receba uma foto aleatória de um gatinho triste")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["sadcat", "sc"])
    async def randomsadcat(self, ctx: Context) -> None:
        sadcat = random_line_from_txt("bobotinho//data//sadcats.txt")
        return await ctx.reply(f"https://i.imgur.com/{sadcat} 😿")

    @helper("role um dado e veja o resultado")
    @usage("para usar: %roll <quantidade_de_dados>d<quantidade_de_lados>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["dice"])
    async def roll(self, ctx: Context, content: str = "1d20") -> None:
        dices = content.lower().split("d")
        amount = int(dices[0]) if dices[0] else None
        sides = int(dices[1]) if dices[1] else None
        if not amount:
            return await ctx.reply("especifique a quantidade de dados, <quantidade>d<lados> (ex: 1d20)")
        if not sides:
            return await ctx.reply("especifique a quantidade de lados do dado, <quantidade>d<lados> (ex: 1d20)")
        if amount > 12:
            return await ctx.reply("eu não tenho tantos dados")
        if amount == 0:
            return await ctx.reply("eu não consigo rolar sem dados")
        if amount < 0:
            return await ctx.reply("não tente tirar meus dados de mim")
        if sides > 9999:
            return await ctx.reply("meus dados não tem tantos lados")
        if sides == 1:
            return await ctx.reply(f"um dado de {sides} lado? Esse é um exercício topológico interessante...")
        if sides <= 0:
            return await ctx.reply(f"um dado de {sides} lados? Esse é um exercício topológico interessante...")
        rolls = [random_number(min=1, max=round(sides)) for i in range(round(amount))]
        each = ", ".join([str(roll) for roll in rolls])
        total = sum(rolls)
        if len(rolls) > 1:
            return await ctx.reply(f"você rolou {each} totalizando {total} 🎲")
        return await ctx.reply(f"você rolou {total} 🎲")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Rand(bot))
