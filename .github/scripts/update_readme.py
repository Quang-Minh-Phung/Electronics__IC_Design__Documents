import os
import re

ROOT = "."

IGNORE = [".git", ".github", "scripts"]

def get_folders():
    return [
        d for d in os.listdir(ROOT)
        if os.path.isdir(d) and d not in IGNORE
    ]

def generate_dashboard(folder):
    subfolders = [
        d for d in os.listdir(folder)
        if os.path.isdir(os.path.join(folder, d))
    ]

    data = []
    total = 0

    for sub in sorted(subfolders):
        sub_path = os.path.join(folder, sub)

        count = 0
        for _, _, files in os.walk(sub_path):
            for f in files:
                if f.lower().endswith(".pdf"):
                    count += 1

        total += count
        data.append((sub, count))

    # tạo table
    table = f"📊 **Tổng số PDF:** {total}\n\n"
    table += "| Subfolder | Số file PDF |\n"
    table += "|-----------|-------------|\n"

    for sub, count in data:
        table += f"| {sub} | {count} |\n"

    return table

def update_dashboard(folder):
    readme_path = os.path.join(folder, "README.md")

    if not os.path.exists(readme_path):
        return

    table = generate_dashboard(folder)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = "<!-- DASHBOARD_START -->"
    end = "<!-- DASHBOARD_END -->"

    new_section = f"{start}\n{table}{end}"

    import re
    updated = re.sub(
        f"{start}.*?{end}",
        new_section,
        content,
        flags=re.S
    )

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✅ Updated dashboard: {folder}")

def count_files(folder):
    count = 0
    for _, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".pdf"):
                count += 1
    return count

folders = sorted(get_folders())

table = "| Thư mục | Số file |\n"
table += "|----------|---------|\n"

total = 0

for f in folders:
    c = count_files(f)
    total += c
    table += f"| {f} | {c} |\n"

table += f"| **Tổng** | **{total}** |\n"

# đọc README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start = "<!-- FILE_COUNT_START -->"
end = "<!-- FILE_COUNT_END -->"

new_content = re.sub(
    f"{start}.*?{end}",
    f"{start}\n{table}{end}",
    content,
    flags=re.S
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

update_dashboard("Tai_Lieu_Tham_Khao")
print("✅ Updated README")
