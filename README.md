# WoLiu-MCP

WoLiu-AI-Agent 的 MCP 服务模块插件系统。

**插件化 · 自动发现 · 任意 MCP 客户端即插即用**

## 是什么

一套可插拔的 MCP 服务模块框架。每个模块（ComfyUI、PPT 生成、TTS、Spine2D 等）放入目录即可被自动发现，无需手动注册。

面向 **WoLiu-AI-Agent** 项目，但任何支持 MCP 协议的智能体客户端均可直接使用。

## 安装

```bash
pip install woliumcp
```

如需 MCP Server 支持：

```bash
pip install woliumcp[mcp]
```

## 快速开始

```python
from woliumcp import init, list_modules, get_module, get_all_mcp_configs

# 设置 WoLiu-AI-Agent 项目根目录
init(project_root="/path/to/WoLiu-AI-Agent")

# 列出所有已安装的服务模块
for m in list_modules():
    print(f"{m['id']}: {m['name']} (running={m['running']})")

# 获取单个模块的 MCP 配置
spine_mcp = get_module("spine2d").get_mcp_command()
print(spine_mcp)
# {'command': 'python', 'args': ['-m', 'spine2d_mcp.server'], 'cwd': '...'}

# 获取所有 MCP 配置，供 MCP 客户端连接
configs = get_all_mcp_configs()
```

或命令行：

```bash
python -m woliumcp /path/to/WoLiu-AI-Agent
```

## 内置模块

| 模块 | ID | 类型 | MCP |
|------|-----|------|-----|
| AI 绘画 (ComfyUI) | `comfyui` | external | - |
| PPT 生成 (Presenton) | `presenton` | external | - |
| 语音合成 (ChatTTS) | `tts` | external | - |
| Spine 动画 | `spine2d` | external | MCP |
| 简历生成 (JadeAI) | `jadeai` | external | - |
| YOLO 训练 (AutoLabel) | `autolabel` | external | - |
| 浏览器自动化 | `agent-browser` | external | MCP |
| 本地 LLM (Ollama) | `ollama` | external | - |
| 15维人格系统 | `personality` | builtin | - |

## 自定义模块

在 `woliumcp/modules/` 下创建新目录，放入 `module.py`：

```python
from woliumcp.base import BaseMCPModule, ModuleMeta, ModuleHealth

class MyModule(BaseMCPModule):
    @property
    def meta(self) -> ModuleMeta:
        return ModuleMeta(
            id="my-module",
            name="我的模块",
            description="这是一个自定义 MCP 服务模块",
            icon="star",
            category="external",
        )

    def detect(self) -> bool:
        return self._exists("side-projects/my-module/main.py")

    def get_mcp_command(self) -> dict | None:
        return {
            "command": "python",
            "args": ["-m", "my_module.server"],
            "cwd": self._path("side-projects/my-module"),
        }

    async def health(self) -> ModuleHealth:
        return ModuleHealth(installed=self.detect())
```

放进去就自动发现，无需改任何注册代码。

## 与其他 MCP 客户端集成

WoLiu-MCP 模块通过标准 MCP 协议暴露。任何支持 MCP 的客户端（Claude Desktop、Cursor、VS Code Copilot 等）都可通过 `get_mcp_command()` 返回的配置直接连接。

在 MCP 客户端配置文件中添加：

```json
{
    "mcpServers": {
        "spine2d": {
            "command": "python",
            "args": ["-m", "spine2d_mcp.server"],
            "cwd": "./side-projects/spine2d-animation-mcp-main"
        }
    }
}
```

## 许可证

MIT
