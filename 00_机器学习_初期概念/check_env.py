# 依据 environment.yml 里实际声明的依赖

"""
check_env.py — 环境检测脚本
运行: python check_env.py
"""

import sys

# 依据 environment.yml 里实际声明的依赖
REQUIRED_PACKAGES = {
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "scipy": "scipy",
    "sklearn": "scikit-learn",
    "xgboost": "xgboost",
}

DOC_PACKAGES = {
    "mkdocs": "mkdocs",
    "mkdocs_jupyter": "mkdocs-jupyter",
}


def check_package(import_name, display_name):
    try:
        mod = __import__(import_name)
        version = getattr(mod, "__version__", "unknown")
        print(f"  ✅ {display_name:<22} v{version}")
        return True
    except ImportError:
        print(f"  ❌ {display_name:<22} 未安装 → pip install {display_name}")
        return False


def main():
    print("=" * 50)
    print("  机器学习环境 — 环境检测")
    print("=" * 50)
    print(f"\nPython 版本: {sys.version}")

    if sys.version_info < (3, 9):
        print("⚠️  建议使用 Python 3.9 及以上版本\n")

    print("\n📦 核心依赖：")
    required_ok = all(
        check_package(imp, disp) for imp, disp in REQUIRED_PACKAGES.items()
    )

    print("\n📦 文档工具（可选）：")
    for imp, disp in DOC_PACKAGES.items():
        check_package(imp, disp)

    print("\n" + "=" * 50)
    if required_ok:
        print("🎉 所有核心依赖已安装，可以开始学习！")
    else:
        print("⚠️  请安装缺少的依赖后重新运行此脚本")
        print("   提示: conda env create -f environment.yml")
    print("=" * 50)


if __name__ == "__main__":
    main()

import sys

