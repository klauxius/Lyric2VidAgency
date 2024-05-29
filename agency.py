import os
import openai
from agency_swarm import Agency
from Lyricist import Lyricist
from CEO import CEO
from VideoProducer import VideoProducer
from agency_swarm import set_openai_key
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your OpenAI API key here
#set_openai_key(os.getenv("OPENAI_API_KEY"))


#Creates an instance of the CEO, Lyricist, and VideoProducer classes
ceo = CEO()
lyricist = Lyricist()
videoproducer = VideoProducer()

agency = Agency([ceo, [ceo, lyricist], #CEO at top level interacts with Lyricist
 [ceo, videoproducer], #CEO at top level interacts with VideoProducer
 [lyricist, videoproducer],[videoproducer, ceo]], #Lyricist interacts with VideoProducer
shared_instructions='./agency_manifesto.md')

if __name__ == '__main__':
    agency.demo_gradio()
