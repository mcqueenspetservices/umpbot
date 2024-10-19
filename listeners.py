import asyncio
import string

from interactions import Extension, listen, Embed
from interactions.api.events import ChannelCreate, Component, MemberAdd, MemberRemove, MessageCreate, MessageUpdate

class Listeners(Extension):
    def __init__(self, bot):
        self.bot = bot

    #region ChannelCreate
    @listen(ChannelCreate)
    async def channel_create_def(self, event: ChannelCreate):
        #region Vetting
        # Check The Channel Was Created In Vetting Tickets Category
        if event.channel.parent_id == 1273989310051389470:
            await asyncio.sleep(1)
            channel_name_parts = event.channel.name.split('-')

            if channel_name_parts[0] == "learning" or channel_name_parts[0] == "educated":
                vetting_instance = self.bot.get_extensions("vetting")[0]
                await vetting_instance.start_vetting(event.channel.id, channel_name_parts[0])
        #endregion
    #endregion

    #region MessageCreate
    @listen(MessageCreate)
    async def message_create_def(self, event: MessageCreate):
        # Ignore Bot Messages
        if event.message.author.bot:
            return
        
        #region Vetting
        if event.message.channel.parent_id == 1273989310051389470:
            channel_name_parts = event.message.channel.name.split('-')
            op_username = ''.join(ch for ch in channel_name_parts[2] if ch not in string.punctuation and ch != '_')
            author_username = ''.join(ch for ch in event.message.author.username if ch not in string.punctuation and ch != '_')

            if op_username != author_username:
                return
            
            vetting_instance = self.bot.get_extensions("vetting")[0]
            await vetting_instance.send_vetting_question(event.message.channel.id)
        #endregion
    #endregion

    #region Components (Buttons and Webhooks)
    @listen(Component)
    async def component_interaction_def(self, event: Component):
        ctx = event.ctx

        #region Rules and Discussion Ethics Buttons
        if ctx.custom_id == "rule_6_criticism":
            embed = Embed(
                title="Principled and Unprincipled Criticism",
                description="Alongside these clarifications, it is important to remember that one can be educated, but have been lied to, thus have principled critiques but with incorrect information guiding those critiques. We will take 100 principled but misled people over 1 unprincipled but properly informed person.",
                color="#36393F"
            )
            embed.add_field(
                name="Principled Criticism",
                value="1. Holistic analysis of individuals and movements in terms of history, material conditions, social conditions.\n a. Holistic analysis takes into account the full context of something as an interconnected whole that can’t be separated from that greater whole- it rejects Positivist forms of separating disciplines and includes history, culture, individuals, groups, everything.\n2.Engages in <#972529765137395752>\n3. Verifies that their reading of a question is correct when unsure- “This is my understanding of this question- could you please let me know if this is correct?”\n4. Open about a lack of understanding of a topic, or otherwise preface their strengths/weaknesses. Seeks education and struggles for greater understanding, rather than shutting down discourse.\n5. Willingness to engage in rebuttals to their points\n",
                inline=True
            )
            embed.add_field(
                name="Unprincipled Criticism",
                value="1. Repeating sensationalized propaganda\n2. Devoid of content: A load of fluff, lacking substance, without conclusions, a whole lot of talk with nothing actually stated\n a. Devoid of context: ignores historical realities (what they were struggling with at the time, what their mindset was attempting it, etc)- questions of willful neglect v incorrect train of thought born of opportunism, revisionism, etc. Not taking note of mitigating circumstances\n3. Slandering Revolutionaries and attacking them on grounds of their personal character, character assassinations, etc to destroy support for individuals and cultivate the need for the 'perfect person' as a revolutionary leader\n4. Focuses on 'what-if''s and brings things into conspiratorial nonsense\n5. Lack of criticism is uncritical",
                inline=True
            )

            await ctx.send (embeds=[embed], ephemeral=True)

        if ctx.custom_id == "rule_9_genocides":
            genocides_embed = Embed(
                title="Genocides",
                description="This is not an entire exhaustive list that will violate Rule 9, with Rule 1984 remaining in place to determine appropriate action surrounding that which is not specifically listed within this clarification.",
                color="#36393F"
            )
            genocides_embed.add_field(
                name="** **",
                value="The Holocaust (includes all those unjustifiably killed by Nazi, Ustaše, Horthy, Iron Guard, Bulgarian Tsarist or Mannerheim forces outside of direct combat in relation to the Second World War)\nThe Japanese Occupation of China & the Rape of Nanjing (1931-45)\nThe Armenian Genocide (1915-22)\nThe Massacres of Hutus (1996-97)\nThe Cambodian Genocide (1975-79)\nThe Rubber Terror (1885-1908)\nThe Circassian Genocide (1864-67)\nThe Rwandan Genocide (1994)\nThe Greek Genocide (1914-22)\nThe Bengal Famine (1942-43)\nThe Assyrian Genocide (1915-23)\nThe Pacification of Libya (1923-33)\nThe Irish 'Potato' Famine (1845-50)\n\nThe NATO Bombing of Yugoslavia (1999)\nThe NATO Bombing of Libya (2011)\nThe Iraq War (2003-11)",
                inline = True
            )
            genocides_embed.add_field(
                name="** **",
                value="The Anfal Campaign (1986-89)\nThe Palestinian Genocide & an-Nakbah (1948-present)\nThe Bangladesh Genocide (1971)\nThe Donbas War (2014-22)\nOperation Condor (1968-89)\nThe Rhodesian Bush War (1964-79)\nThe Transatlantic Slave-Trade & American Slavery (1526-1865)\nThe Colonisation of Sápmi (1607-present)\nThe Colonisation of the Americas (1492-present)\nThe Japanese Occupation of Korea (1910-45)\nThe Colonisation of Hawai'i (1900-present)\nThe Saudi-led Intervention in Yemen (2014-present)\nThe Bosnian Genocide (1992-95)\nSegregation in the United States (1865-1964)\nThe Darfur Genocide (2003-present)\nThe Yazidi Genocide (2014-15)\nThe Indonesian Genocide (1965-66)",
                inline = True
            )

            await ctx.send (embeds=[genocides_embed], ephemeral=True)
        
        if ctx.custom_id == "rule_9_imperialisms":
            imperialism_embed = Embed(
                title="Imperialism",
                description="This is not an entire exhaustive list that will violate Rule 9, with Rule 1984 remaining in place to determine appropriate action surrounding that which is not specifically listed within this clarification.",
                color="#36393F"
            )
            imperialism_embed.add_field(
                name="** **",
                value="American Imperialism\nJapanese Imperialism\nRussian Imperialism\nBritish Imperialism\nFrench Imperialism\nSpanish Imperialism\nPortuguese Imperialism\nItalian Imperialism\nOttoman Imperialism\nChinese Imperialism\nAustrian Imperialism\nSwedish Imperialism\nDanish Imperialism\nDutch Imperialism\nBelgian Imperialism",
                inline=True
            )
            imperialism_embed.add_field(
                name="** **",
                value="Canadian Imperialism\nGerman Imperialism\nSoviet Imperialism\nYugoslav Imperialism\nNorwegian Imperialism\nBrazilian Imperialism\nIranian Imperialism\nAustralian Imperialism\nNew Zealandic Imperialism\nSaudi Imperialism\nQatari Imperialism\nBahraini Imperialism\nEmirati Imperialism\nIsraeli Imperialism",
                inline=True
            )

            await ctx.send (embeds=[imperialism_embed], ephemeral=True)
        
        if ctx.custom_id == "rule_9_bigotries":
            bigotries_embed = Embed(
                title="Bigotries",
                description="This is not an entire exhaustive list that will violate Rule 9, with Rule 1984 remaining in place to determine appropriate action surrounding that which is not specifically listed within this clarification.",
                color="#36393F"
            )
            bigotries_embed.add_field(
                name="** **",
                value="Anti-Semitism\nAntiziganism\nHomophobia\nTransphobia\nBiphobia\nMisogyny\nQueerphobia\nAbleism",
                inline=True
            )
            bigotries_embed.add_field(
                name="** **",
                value="Pol-Potism\nEugenicism\nWhite Supremacism (White Identitarianism/Race Realism/Racialism/Racism)",
                inline=True
            )

            await ctx.send (embeds=[bigotries_embed], ephemeral=True)
        
        if ctx.custom_id == "rule_9_ideologies":
            ideologies_embed = Embed(
                title="Ideologies",
                description="This is not an entire exhaustive list that will violate Rule 9, with Rule 1984 remaining in place to determine appropriate action surrounding that which is not specifically listed within this clarification.",
                color="#36393F"
            )
            ideologies_embed.add_field(
                name="** **",
                value="Fascism (Third Position/Third Way)\nNazism (National-Socialism/Hitlerism)\nItalian Fascism (Mussolinism)\nSpanish Fascism (Falangism/Francoism)\nNational Syndicalism\nDuginism (Fourth Way/National-Bolshevism)",
                inline=True
            )
            ideologies_embed.add_field(
                name="** **",
                value="Chilean Fascism (Pinochetism)\nSocial-Darwinism (Nordicism/Han Nationalism/Aryanism)\nHindutva\nMosleyism\nUltra-nationalism\nIrredentism\nConservatism\nLegionarism\nMonarchism\nStrasserism",
                inline=True
            )

            await ctx.send (embeds=[ideologies_embed], ephemeral=True)

        if ctx.custom_id == "rule_9_states":
            states_embed = Embed(
                title="States",
                description="This is not an entire exhaustive list that will violate Rule 9, with Rule 1984 remaining in place to determine appropriate action surrounding that which is not specifically listed within this clarification.",
                color="#36393F"
            )
            states_embed.add_field(
                name="** **",
                value="The German Reich (1933-45)\nThe Kingdom of Italy (1922-43)\nThe Italian Social Republic (1943-45)\nThe Kingdom of Hungary (1920-46)\nThe Empire of Japan (1868-1947)\nThe Slovak Republic (1939-45)\nThe Tsardom of Bulgaria (1941-46)\nThe Kingdom of Thailand (1941-45)\nThe Russian Empire (1904-17)\nThe German Empire (1881-1918)\nThe Republic of Cuba (1952-1959)\nThe Republic of Chile (1974-90)\nThe Kingdom of Romania (1941-44)\nThe French State (1940-44)\nThe United States of America (1776-present)\nThe Confederate States of America (1861-1865)\nThe Republic of Korea (1948-60, 1963-87)\nThe Kingdom of England (1607-1707)",
                inline=True
            )
            states_embed.add_field(
                name="** **",
                value="The Republic of Vietnam (1955-75)\nThe United Kingdom of Great Britain and Northern Ireland (1707-present)\nDemocratic Kampuchea (1975-79)\nThe State of Israel (1948-present)\nCanada (1982-present)\nThe Russian Federation (1991-present)\nThe United Arab Emirates (1971-present)\nThe Kingdom of Saudi Arabia (1932-present)\nThe State of Qatar (1971-present)\nThe Kingdom of Bahrain (1971-present)\nThe Kingdom/Republic of France (1524-present)\nThe Kingdom/Republic/State of Spain (1492-present)\nThe Kingdom/Republic of Portugal (1415-1975)\nThe Islamic State (of Iraq and the Levant/Syria) (1999-2019)",
                inline=True
            )

            await ctx.send (embeds=[states_embed], ephemeral=True)
        #endregion
    #endregion