import os
import tempfile
import git

def clone_and_parse_repo(repo_url):
    tmp_dir = tempfile.mkdtemp()
    repo = git.Repo.clone_from(repo_url, tmp_dir)

    # Read README.md (fallback if missing)
    readme_path = os.path.join(tmp_dir, "README.md")
    readme = open(readme_path, "r").read() if os.path.exists(readme_path) else "No README found."

    files_info = []
    for root, _, files in os.walk(tmp_dir):
        for file in files:
            if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', errors='ignore') as f:
                        snippet = f.read(500)
                        files_info.append({'filename': file, 'snippet': snippet})
                except Exception as e:
                    continue

    return {
        "readme": readme,
        "files": files_info,
        "tech_stack": detect_stack(tmp_dir)
    }

def detect_stack(path):
    tech = []
    if os.path.exists(os.path.join(path, 'package.json')):
        tech.append("JavaScript/Node")
    if os.path.exists(os.path.join(path, 'requirements.txt')):
        tech.append("Python")
    if os.path.exists(os.path.join(path, 'tailwind.config.js')):
        tech.append("TailwindCSS")
    if os.path.exists(os.path.join(path, 'pom.xml')):
        tech.append("Java")
    if os.path.exists(os.path.join(path, 'CMakeLists.txt')):
        tech.append("C++")
    return tech
