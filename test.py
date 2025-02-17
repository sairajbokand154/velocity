    

@register_tool(category="MyCategory")
class MyTool(BaseTool):
    async def execute(self, param: str) -> str:
        return f"Result: {param}"