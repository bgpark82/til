import os

# README.md 헤더
README_HEADER = """# 📂 프로젝트 문서 구조

이 리포지토리의 마크다운 파일 목록입니다.

"""

def get_markdown_files(root_dir="."):
    """리포지토리 내 모든 .md 파일을 찾아 디렉토리별로 정리"""
    md_files = []
    for root, _, files in os.walk(root_dir):
        if ".git" in root:  # .git 폴더는 무시
            continue
        for file in files:
            if file.endswith(".md") and file != "README.md":
                rel_path = os.path.relpath(os.path.join(root, file), root_dir)
                md_files.append(rel_path)
    return sorted(md_files)

def generate_tree_structure(md_files):
    """트리 형태의 마크다운 목록을 생성"""
    tree = {}
    for path in md_files:
        parts = path.split(os.sep)
        current = tree
        for part in parts[:-1]:  # 마지막 요소(파일명)는 포함하지 않음
            current = current.setdefault(part, {})
        current[parts[-1]] = None  # 파일은 None 값
    
    return tree

def format_tree(tree, prefix=""):
    """트리 구조를 마크다운 리스트로 변환"""
    lines = []
    for key, value in sorted(tree.items()):
        lines.append(f"{prefix}- [{key}]({os.path.join(prefix, key)})")
        if isinstance(value, dict):
            lines.extend(format_tree(value, prefix + "  "))  # 들여쓰기 추가
    return lines

def update_readme():
    """README.md 파일을 생성 및 업데이트"""
    md_files = get_markdown_files()
    tree = generate_tree_structure(md_files)
    tree_structure = "\n".join(format_tree(tree))

    new_readme = README_HEADER + "\n" + tree_structure

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    update_readme()
    print("✅ README.md 업데이트 완료!")
