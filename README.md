# WoLiu-MCP

WoLiu-AI-Agent 的 MCP 服务模块插件系统。

**插件化 · 自动发现 · 任意 MCP 客户端即插即用**

## 是什么

一套可插拔的 MCP 服务模块框架。每个模块（ComfyUI、PPT 生成、TTS、Spine2D 等）放入目录即可被自动发现，无需手动注册。

面向 **WoLiu-AI-Agent** 项目，但任何支持 MCP 协议的智能体客户端均可直接使用。

## 接入我流展示
<img width="2549" height="1403" alt="image" src="https://github.com/user-attachments/assets/0a3dee5c-c352-4975-8e27-245eb635f3e4" />

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

## 集成到 WoLiu-AI-Agent

WoLiu-MCP 是 WoLiu-AI-Agent 的服务管理核心。当你克隆主项目后：

### 1. 安装

```bash
cd WoLiu-AI-Agent
pip install woliumcp
```

### 2. 工作原理

主项目 `server/app.py` 启动时会自动调用 WoLiu-MCP：

```
server/app.py
    ├── 扫描 agent/mcp_modules/ 下的所有模块
    ├── 每个模块的 module.py 由 WoLiu-MCP 框架自动发现
    ├── 注册各模块提供的工具 Schema（供 LLM 调用）
    ├── 前端设置面板 → 显示模块开关/启停按钮
    ├── WebSocket handler → 接收前端点"开启"消息
    └── 子进程/HTTP 调用 → 启动各服务（ComfyUI、Presenton 等）
```

- **内置模块**（personality 等）直接 `import` 进 Agent 进程
- **外部服务模块**（ComfyUI、Presenton、JadeAI 等）通过子进程启动服务，Agent 通过 HTTP API 或 MCP 协议与它们通信

### 3. 添加新模块

在 `agent/mcp_modules/` 下创建目录，写入 `module.py`，参考上面的「自定义模块」示例。放到目录中即被自动发现，主项目无需任何额外配置。

### 4. MCP Server 集成

部分模块（spine2d、agent-browser）对外暴露标准 MCP Server：

```json
{
    "mcpServers": {
        "spine2d": {
            "command": "python",
            "args": ["-m", "spine2d_mcp.server"],
            "cwd": "./side-projects/spine2d-animation-mcp-main"
        },
        "agent-browser": {
            "command": "npx",
            "args": ["@playwright/mcp", "--headless"],
            "cwd": "."
        }
    }
}
```

主项目的 Agent 内核通过 `agent/mcp_client/` 连接这些 MCP Server，获取工具列表并调用。

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
## 集成项目
语音合成：
ChatTTS：
https://github.com/2noise/ChatTTS
Confucius4-TTS：
https://github.com/netease-youdao/Confucius4-TTS/blob/main/README.zh.md

简历制作：
JadeAI-0.4.1：
https://github.com/LingyiChen-AI/JadeAI

PPT制作：
https://github.com/presenton/presenton

Live2D动画：
https://github.com/ampersante/spine2d-animation-mcp

目标检测：
https://github.com/xzcGit/autolabel-dock

ComfyUI：
https://github.com/Comfy-Org/ComfyUI

## 许可证

MIT
