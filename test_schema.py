from tools.registry import registry
import tools.propose_hire_tool
schema = registry.get_tool_schema("propose_hire_worker")
print(schema)
