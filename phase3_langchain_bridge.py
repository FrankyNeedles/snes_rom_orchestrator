from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory # type: ignore
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv('.env')

class Phase3Bridge:
    def __init__(self):
        api_key = os.getenv('OPENROUTER_API_KEY')
        model = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3.5-sonnet')
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.1
        )
        import re
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="output"
        )
        self.rag_context = """
pvsneslib APIs: oamSetPosition(x,y,obj,priority,siz), oamSetVisible(obj,visible), oamSetGfxTileIndex(obj,tile,siz),
spcPlayMusic(song), sfxPlaySample(sample), REG_BRIGHTNESS for fade (0-15), frame_counter++ in VBlank.
OAM DMA: s_dma(3, OAM, 0x0400, 64, DMA_SPRITEREF).
Timeline: array of events triggered by frame_counter.
Examples from SNES-IDE/docs/examples.
        """
    
    def generate_blueprint(self, prompt, mode, audio):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are SNES ROM architect. Use {rag_context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Mode: {mode}, Audio: {audio}\nPrompt: {prompt}\nRespond with ONLY valid JSON blueprint."),
            ("system", "JSON: {\"mode\": \"{mode}\", \"audio\": \"{audio}\", \"actors\": [], \"timeline\": [{{ \"frame\": 60, \"action\": \"move\", \"actor\": 0, \"x\": 50, \"y\": 30 }}], \"custom_c\": \"// Dynamic C\"}")
        ])
        chain = prompt_template | self.llm
        result = chain.invoke({
            "rag_context": self.rag_context,
            "mode": mode,
            "audio": audio,
            "prompt": prompt
        })
        blueprint_str = result.content.strip()
        # Simple JSON extract
        json_match = re.search(r'\{.*\}', blueprint_str, re.DOTALL)
        blueprint = json.loads(json_match.group())
        self.memory.save_context({"input": prompt}, {"output": blueprint_str})
        return blueprint
