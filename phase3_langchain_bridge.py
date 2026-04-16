import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv('.env')

class Phase3Bridge:
    def __init__(self):
        api_key = os.getenv('OPENROUTER_API_KEY')
        model = os.getenv('OPENROUTER_MODEL', 'google/gemini-2.0-flash-lite-preview-02-05:free')
        
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.1
        )
        
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )

    def generate_blueprint(self, prompt, mode, audio):
        # SENIOR FIX: Use {{ }} for the C code so LangChain doesn't think they are variables
        rag_rules = """
        YOU ARE A PVSNESLIB EXPERT. 
        RULES:
        1. ALWAYS use #include <snes.h>
        2. NEVER use snes_dev.h.
        3. Logic: consoleInit() starts the SNES. RGB5(r,g,b) for colors (0-31).
        4. Loop: while(1) {{ WaitVBL(); }} must be present.
        """

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", rag_rules),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Mode: {mode}, Audio: {audio}. Request: {prompt}"),
            ("system", "Output ONLY the raw C code. No markdown code blocks, no backticks, no talking.")
        ])

        chain = prompt_template | self.llm
        
        # Get memory history
        mem_vars = self.memory.load_memory_variables({})
        history = mem_vars.get("chat_history", [])
        
        result = chain.invoke({
            "chat_history": history,
            "prompt": prompt,
            "mode": mode,
            "audio": audio
        })

        clean_code = re.sub(r'```[a-zA-Z]*\n?|```', '', result.content).strip()
        self.memory.save_context({"input": prompt}, {"output": "Code Generated"})
        
        return clean_code

    def write_to_engine(self, c_code):
        if "#include <snes.h>" not in c_code:
            c_code = "#include <snes.h>\n" + c_code
            
        with open("mega_engine.c", "w") as f:
            f.write(c_code)