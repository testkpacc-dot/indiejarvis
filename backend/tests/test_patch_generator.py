from backend.patch_generator.generator import generate_patches

def test_generate_patches_basic():
    old = "SYSTEM: original prompt"
    patches = generate_patches(old, representative_samples=[])
    assert isinstance(patches, list)
    assert any("patched_prompt" in p for p in patches)
    assert all(old in p["patched_prompt"] for p in patches)
