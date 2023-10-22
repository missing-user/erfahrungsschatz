import streamlit as st
import datetime
import pandas as pd
import streamlit_bd_cytoscapejs
import openai 


from openai.embeddings_utils import get_embedding
openai.api_key = "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"

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191



st.set_page_config(layout="wide")

# Sample data
users = ["You","You", "Theo", "Theo", "Theo", "Felix", "Felix", "Felix"]
journal_entries = [
    """First day of journaling with Erfahrungsschatz! REally excited; I am mostly working on the fabrication of the photonic chip in the lab.
    We are working on it for a quantum networks group. In quantum networks there are two type of networks: those which need node entanglement and those who do not. The method this experimental group is 
    working on is doping erbium atoms into silicon and building a quantum memory platform from this. 
    This could be extremely useful, because erbium atoms have energy spectrums (that would be used as TLS 
    for the qubit for the quantum menmory) that emit in the telecom-c length. with that entanglement over fiber 
    could be made way more efficient maybe. current methods of entangling distant nodes via optical fibres require the 
    modulation of the frequency of the light for sending it over larger distances without loss and then back modulation. 
    The modulation creates huge losses and thus node entanglement is very difficult currently.
    The SU8 and fiber to chip coupling is one subproblem, which is the interface between the optical fiber (long distance link to next node) 
    and the Chip where the silicon and erbium is on.""",
    """
    Trying to coat a chip with SU8 but not succeeding. The SU8 is not sticking to the chip.
    """,
    """Trying new fabrication method, namely to try new high-resolution mask for fabrication of photonic chip. 
    First attempt of using SU8 as a high-resolution mask. Made one initial attempt for developing SU8 using the following parameters: 
    Spin-Coating SU8 Soft Bake (3 min. at 60 degrees)
    Photolithography Exposure (lambda = 450 nm, P = 15 muW, t = 2 min.)
    Development (3 min. in SU8 developer)
    Looking at Chip under the microscope;
    This attempt Failed; The development step dissolved all the SU8 for an unknown reason so far. Will have to investigate tomorrow.""",
    """As yesterday's attempt of using SU8 as a high-resolution mask. Made further attempts for developing SU8 
    using the same steps as yesterday with various different parameters, all failed. The development step still dissolved all the SU8 for an unknown reason""",
    """Third attempt of using SU8 as a high-resolution mask. Realized that I skipped a step (the post-exposure step) that was flagged as optional in the SU8 manual. Introducing the step turned out to make the process work. The steps I followed for my working version:
    1. Spin-Coating SU8
    Soft Bake (3 min. at 60 degrees)
    Photolithography Exposure (lambda = 450 nm, P = 15 muW, t = 2 min.)
    Post-Exposure Bake (4 min.)
    Development (3 min. in SU8 developer)
    Looking at the chip under the microscope. This time I saw the SU8 on the chip after the development! --> method worked""",
    """For testing and designing my on chip cavity, I need to couple from fiber to on-chip waveguide on the room temperature setup.""",
    """trying to couple to the chip. Coupling not possible for unknown reason. Data jumps around weirdly. Tried methods that did not lead to success:
    - checking laser frequency
    - changing chip we know couples
    - checking pigtail connections
    - checking that laser exites through fiber with visible laser
    - turning off ventilation system to reduce noise""",
    """At the beginning of the day I still had no clue why it was not working; After a lot of discussions with group members, I
    finally figured out what the problem was: The detection diode was not calibrated correctly. So next time keep that in mind!"""
]
dates = [datetime.date(2021, 2, 1),datetime.date(2023, 2, 1), datetime.date(2021, 2, 1), datetime.date(2022, 2, 1), 
         datetime.date(2023, 2, 1), datetime.date(2021, 2, 1), datetime.date(2022, 2, 1),
         datetime.date(2023, 2, 1)]


# Create DataFrame
df = pd.DataFrame({'user': users, 'journal_entry': journal_entries, 'date': dates})

print(df)

#ontological siminlarity

dates = df.date.unique()
users = df.user.unique()
dates = sorted(dates)

containers = []
#how to inlcude external css file: https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804/2
for date in dates:
    c = st.container()
    containers.append(c)
    columns = containers[-1].columns(len(users)+1)
    with columns[0]:
        columns[0].header("Date")
        #columns[0].markdown(f'<div style="border-radius: 15px; background-color: light-grey; padding: 20px; box-shadow: 5px 5px 10px #888888;">{date}</div>', unsafe_allow_html=True)
        columns[0].write(date)
    for index, column in enumerate(columns[1:]):
        with column:
            column.header(users[index])
            try:
                text = df[(df['user'] == users[index]) & (df['date'] == date)].iloc[0]['journal_entry']
            except:
                text = ""
            #column.markdown(f'<div style="border-radius: 15px; background-color: grey; padding: 20px; box-shadow: 5px 5px 10px #888888;">{text}</div>', unsafe_allow_html=True)
            column.write(text)


completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=formatted_messages
        )