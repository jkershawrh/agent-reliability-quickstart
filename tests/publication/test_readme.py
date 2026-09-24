from pathlib import Path


def test_publication_structure():
    required = ["LICENSE", "README.md", "site.yml", "antora.yml", "modules/ROOT/nav.adoc", "config/reliability-profile.yaml"]
    assert [path for path in required if not Path(path).exists()] == []


def test_readme_declares_safety_and_attribution():
    content = Path("README.md").read_text()
    for phrase in ("human approval", "Failure injection is disabled", "Attribution", "MIT License"):
        assert phrase in content

