"""ComfyUI AI 绘画/视频生成服务模块"""

from woliumcp.base import BaseMCPModule, ModuleMeta, ModuleHealth


class ComfyUIModule(BaseMCPModule):
    @property
    def meta(self) -> ModuleMeta:
        return ModuleMeta(
            id="comfyui",
            name="AI 绘画",
            description="ComfyUI 图像与视频生成（Z-Image-Turbo / NetaYume / WAN2.1）",
            icon="paint-brush",
            category="external",
        )

    def detect(self) -> bool:
        """检查 ComfyUI 目录是否存在"""
        return self._exists("side-projects/ComfyUI_windows_portable/ComfyUI/main.py")

    def get_mcp_command(self) -> dict | None:
        # ComfyUI 没有 MCP server，通过 HTTP API 直连
        return None

    def get_direct_tools(self) -> list[dict]:
        """ComfyUI 的 HTTP 桥接工具已内置在 agent.tools 中，此处仅声明"""
        return []

    async def health(self) -> ModuleHealth:
        h = ModuleHealth(installed=self.detect())
        if h.installed:
            h.port = 8188
            h.running = await self._check_port(8188)
            if not h.running:
                h.last_error = "ComfyUI 未运行"
        return h
