"""WoLiu-MCP 命令行入口"""

import sys


def main():
    from woliumcp import init, list_modules, get_all_mcp_configs

    project_root = sys.argv[1] if len(sys.argv) > 1 else None
    if project_root:
        init(project_root=project_root)
    else:
        init(project_root=".")

    print("=" * 60)
    print("  WoLiu-MCP — 服务模块扫描结果")
    print("=" * 60)

    modules = list_modules()
    if not modules:
        print("\n  未发现任何已安装的模块。")
        print("  将服务放入项目 side-projects/ 目录后重试。")
        return

    print(f"\n  共发现 {len(modules)} 个模块:\n")
    for m in modules:
        mcp_mark = " [MCP]" if m["has_mcp"] else ""
        status_icon = "●" if m["running"] else "○"
        print(f"  {status_icon} {m['id']:20s} {m['name']:12s}  {m['status']:8s}{mcp_mark}")

    configs = get_all_mcp_configs()
    if configs:
        print(f"\n  支持 MCP 协议的模块 ({len(configs)}):")
        for mod_id in configs:
            print(f"    - {mod_id}")
    else:
        print("\n  提示: 暂无模块支持 MCP 协议")


if __name__ == "__main__":
    main()
