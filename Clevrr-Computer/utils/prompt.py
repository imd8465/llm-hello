from langchain_core.prompts import PromptTemplate
from utils.contants import PREFIX, SUFFIX, EXAMPLES

_template = PREFIX + "\n\n" + EXAMPLES + "\n\n"  + SUFFIX
prompt = PromptTemplate(input_variables=['agent_scratchpad', 'tool_names', 'input', 'tools'], template=_template)