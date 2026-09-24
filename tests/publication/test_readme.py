from pathlib import Path


def test_publication_structure():
    required = ["LICENSE", "README.md", "site.yml", "antora.yml", "modules/ROOT/nav.adoc", "config/reliability-profile.yaml"]
    assert [path for path in required if not Path(path).exists()] == []


def test_readme_declares_safety_and_attribution():
    content = Path("README.md").read_text()
    for phrase in ("human approval", "Failure injection is disabled", "Attribution", "MIT License"):
        assert phrase in content


def test_showroom_contains_the_complete_reliability_journey():
    pages = Path("modules/ROOT/pages")
    nav = Path("modules/ROOT/nav.adoc").read_text()
    journey = [
        "01-healthy-agent.adoc",
        "02-safety-architecture.adoc",
        "03-prompt-injection.adoc",
        "04-tool-authorization.adoc",
        "05-inference-disruption.adoc",
        "06-prove-recover.adoc",
    ]

    for name in journey:
        page = pages / name
        assert page.is_file()
        assert name in nav
        content = page.read_text()
        assert "== What you will learn" in content
        assert 'role="execute"' in content
        assert "Verify" in content
        assert "== Key takeaway" in content

    assert "conclusion.adoc" in nav
    assert (pages / "conclusion.adoc").is_file()
    assert sum(len(page.read_text().split()) for page in pages.glob("*.adoc")) >= 5500


def test_showroom_contains_original_learning_visuals():
    images = Path("modules/ROOT/assets/images")
    assert {path.name for path in images.glob("*.svg")} >= {
        "reliability-architecture.svg",
        "control-planes.svg",
        "failure-paths.svg",
        "qualification-loop.svg",
    }
