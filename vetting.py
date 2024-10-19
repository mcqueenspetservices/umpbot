import sqlite3

from interactions import Extension, Embed, OptionType, slash_option, Member
from interactions.ext.hybrid_commands import hybrid_slash_command, HybridContext

#region Database
def init_database():
    conn = sqlite3.connect('completed_vetting_tickets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vetting_progress
                 (channel_id INTEGER PRIMARY KEY, question_type TEXT, current_question INTEGER)''')
    conn.commit()
    conn.close()

def update_vetting_progress(channel_id, question_number):
    conn = sqlite3.connect('completed_vetting_tickets.db')
    c = conn.cursor()
    c.execute("UPDATE vetting_progress SET current_question = ? WHERE channel_id = ?", (question_number, channel_id))
    conn.commit()
    conn.close()

init_database()
#endregion

class Vetting(Extension):
    def __init__(self, bot):
        self.bot = bot

    async def start_vetting(self, channel_id, type):
        # Add Ticket To Database
        conn = sqlite3.connect('completed_vetting_tickets.db')
        c = conn.cursor()
        c.execute("INSERT INTO vetting_progress (channel_id, question_type, current_question) VALUES (?, ?, ?)",
                  (channel_id, type, 1))
        conn.commit()
        conn.close()

        # Send First Question
        if type == "learning":
            await self.send_vetting_question(channel_id)

        elif type == "educated":
            await self.send_vetting_question(channel_id)

    async def send_vetting_question(self, channel_id):
        # Set Channel
        channel = self.bot.get_channel(int(channel_id))
        
        # Fetch Progress From Database
        conn = sqlite3.connect('completed_vetting_tickets.db')
        c = conn.cursor()
        c.execute("SELECT question_type, current_question FROM vetting_progress WHERE channel_id = ?", (channel_id,))
        result = c.fetchone()
        conn.close()
        question_type, current_question = result

        if current_question == 0:
            return
        
        if question_type == "learning" and current_question == 10:
            role_mention = f'<@&{1243318458712592384}>'
            await channel.send(f"Thank You For Answering! {role_mention} Will Be With You Shortly.")
            conn = sqlite3.connect('completed_vetting_tickets.db')
            c = conn.cursor()
            c.execute("UPDATE vetting_progress SET current_question = 0 WHERE channel_id = ?", (channel_id,))
            conn.commit()
            conn.close()
            return

        if question_type == "educated" and current_question == 14:
            role_mention = f'<@&{1243318458712592384}>'
            await channel.send(f"Thank You For Answering! {role_mention} Will Be With You Shortly.")
            conn = sqlite3.connect('completed_vetting_tickets.db')
            c = conn.cursor()
            c.execute("UPDATE vetting_progress SET current_question = 0 WHERE channel_id = ?", (channel_id,))
            conn.commit()
            conn.close()
            return

        embed_obj = globals()[f"{question_type}_question_{current_question}"]
        await channel.send(embed=embed_obj)

        # Update Database
        conn = sqlite3.connect('completed_vetting_tickets.db')
        c = conn.cursor()
        c.execute("UPDATE vetting_progress SET current_question = current_question + 1 WHERE channel_id = ?", (channel_id,))
        conn.commit()
        conn.close()

#region Embeds
#region Learning
learning_question_1 = Embed(
    title="[1 / 9] Why Do You Want To Join The Server?",
    description="Make sure you have read our discussion ethics to understand the level of discussion, and type of space we are building in the United Marxist Pact.",
    color="#2986cc"
)
learning_question_2 = Embed(
    title="[2 / 9] What Are Your Views On Capitalism, And Why?",
    description="We do not require that you are a socialist/communist to join this server, for common myths or misunderstandings of socialism, please visit: <#1005887212614852618>.",
    color="#2986cc"
)
learning_question_3 = Embed(
    title="[3 / 9] What Would You Characterise Your Ideology As?",
    description="Include any thinkers or figures that have influenced your ideological views and what you have taken from them, mentioning key works that you have read may be helpful.",
    color="#2986cc"
)
learning_question_4 = Embed(
    title="[4 / 9] What Are Your Views On Lenin, Stalin and Mao? ",
    description="We do not require that you take a specific line or position on any of the figures mentioned, for common myths, misunderstandings, or discussion topics, please visit: <#1005887293065801768>.",
    color="#2986cc"
)
learning_question_5 = Embed(
    title="[5 / 9] What Are Your Views On AES States?",
    description="AES (actual existing socialism) states covers examples such as China, Cuba, the DPRK, the USSR. If you do not view them as socialist, please explain why.",
    color="#2986cc"
)
learning_question_6 = Embed(
    title="[6 / 9] What Are Your Views On National Liberation Movements?",
    description="This includes movements within existing nations, such as Black Liberation, Indigenous Land Back Movements, Palestine, Kurdistan, and Kosovo. if you do not support liberation movements, please explain why.",
    color="#2986cc"
)
learning_question_7 = Embed(
    title="[7 / 9] Do You Support LGBTQIA+ People And Movements For Their Liberation?",
    description="This includes specifically transgender people, intersex people, gay/lesbian people. if you are not supportive of these people / identities or movements, please explain why.",
    color="#2986cc"
)
learning_question_8 = Embed(
    title="[8 / 9] Do You Believe Communists Should Support Multipolarity?",
    description="Multipolarity takes the form of strengthening capitalist anti-US/West nations such as Russia, Iran, Belarus. Please explain why or why not. ",
    color="#2986cc"
)
learning_question_9 = Embed(
    title="[9 / 9] Did You Read The <#1005886992166420580>?",
    description="It is not required that you read the thread clarifications expanding on the rules. if you have read them, do you agree to follow them?",
    color="#2986cc"
)
#endregion

#region Educated
educated_question_1 = Embed(
    title="[1 / 13] Why Do You Want To Join The Server?",
    description="Make sure you have read our discussion ethics to understand the level of discussion, and type of space we are building in the United Marxist Pact.",
    color="#2986cc"
)
educated_question_2 = Embed(
    title="[2 / 13] What Are Your Views On National Liberation Movements?",
    description="This includes movements within existing nations, such as Black Liberation, Indigenous Land Back Movements, Palestine, Kurdistan, and Kosovo. if you do not support liberation movements, please explain why.",
    color="#2986cc"
)
educated_question_3 = Embed(
    title="[3 / 13] Do You Support LGBTQIA+ People And Movements For Their Liberation?",
    description="This includes specifically transgender people, intersex people, gay/lesbian people. if you are not supportive of these people / identities or movements, please explain why.",
    color="#2986cc"
)
educated_question_4 = Embed(
    title="[4 / 13] Do You Believe Communists Should Support Multipolarity?",
    description="Multipolarity takes the form of strengthening capitalist anti-US/West nations such as Russia, Iran, Belarus. Please explain why or why not. ",
    color="#2986cc"
)
educated_question_5 = Embed(
    title="[5 / 13] Did You Read The <#1005886992166420580>?",
    description="It is not required that you read the thread clarifications expanding on the rules. if you have read them, do you agree to follow them?",
    color="#2986cc"
)
educated_question_6 = Embed(
    title="[6 / 13] What Ideology Would You Say You Mostly Align With?",
    description="Include Any Thinkers Or Figures That Have Influenced Your Ideological Views And What You Have Taken From Them, Mentioning Key Works That You Have Read May Be Helpful.",
    color="#2986cc"
)
educated_question_7 = Embed(
    title="[7 / 13] What Social Relations Must Be Produced To Constitute A Capitalist Mode Of Production?",
    description="**[Key Words]:** Mode of Production; Production for Exchange; Wage Labor; Private Property; Bourgeoisie and Proletariat (Class); Capital; Valorization; Accumulation",
    color="#2986cc"
)
educated_question_8 = Embed(
    title="[8 / 13] What Are The Characteristics Of The Communist Mode Of Production, In Both The Lower Phase (AKA: Socialism) And The Higher Phase (AKA: Communism)?",
    description="**[Key Words]:** Transitional; Mode of Production; Higher and Lower Phase; Money; State; Commodity; Labor",
    color="#2986cc"
)
educated_question_9 = Embed(
    title="[9 / 13] Explain The Methodology Of Marx, Showing How Marx Reconciles The Inconsistencies Within Materialism And Idealism Via Dialectics.",
    description="**[Key Words]:** Contradiction; Materialism; Dialect; Transhistoricism; Hegel/Aristotle/Mao/Engels; Holistic; Dynamic; Social Relations; Dialectical Idealism; Production and Reproduction; Law of Dialect;",
    color="#2986cc"
)
educated_question_10 = Embed(
    title="[10 / 13] What Differentiates Scientific Socialism From Utopian Socialism? Please Give An Example Of Both.",
    description="**[Key Words]:** Moral/Normative Arguments; Class Character; Dialectical Materialism; Interchangeable with Communism; Robert Owen; Anarchism",
    color="#2986cc"
)
educated_question_11 = Embed(
    title="[11 / 13] Explain At Least Three Theoretically Derived Innovations Lenin Made To Marxism.",
    description="**[Key Words]:** Imperialism; Vanguard; Democratic Centralism; War Communism; Revolutionary Defeatism; Particulars of Legal and Illegal Struggle; Dual Power; Theory of Socialist Industrialization",
    color="#2986cc"
)
educated_question_12 = Embed(
    title="[12 / 13] What Is The Materialist Conception Of The History Of The State In Terms Of Its: Genesis, Development, Withering Away",
    description="**[Key Words]:** Dictatorship of the Proletariat/Bourgeoisie/Ruling Class; Withering; Capturing the State; Smashing Bourgeois State; Class Conflict; Social Relations; Means of Production; Distinct Interests",
    color="#2986cc"
)
educated_question_13 = Embed(
    title="[13 / 13] How Should The Working Class Organize To Take Class Power?",
    description="[Key Words]: Party; Oppressed Groups; Democratic Centralism; Tactics; Go to the Masses; Praxis",
    color="#2986cc"
)
#endregion
#endregion