# scripts/fol_patch_ttl.py
"""Patch firstOrderLogicAxiom/Definition annotations in copi-core.ttl."""
import re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from fol_gen import fix_fol_annotation, fix_dl_in_fol


def patch_ttl_annotations(ttl_src_path: str) -> str:
    """Return patched content of copi-core.ttl with ∀v wrappers added."""
    content = pathlib.Path(ttl_src_path).read_text(encoding='utf-8')

    patched = re.sub(
        r'iof-av:firstOrderLogic(Axiom|Definition)\s+"([^"]+)"',
        lambda m: (
            f'iof-av:firstOrderLogic{m.group(1)} '
            f'"{fix_dl_in_fol(fix_fol_annotation(m.group(2)))}"'
        ),
        content
    )
    return patched


if __name__ == '__main__':
    repo_root = pathlib.Path(__file__).parent.parent
    src_path = repo_root / 'src' / 'ontology' / 'components' / 'copi-core.ttl'

    original = src_path.read_text(encoding='utf-8')
    patched = patch_ttl_annotations(str(src_path))

    if patched != original:
        src_path.write_text(patched, encoding='utf-8')
        print(f'Patched {src_path.name}')
        orig_lines = set(original.splitlines())
        new_lines = set(patched.splitlines())
        changed = len(new_lines - orig_lines)
        print(f'  ~{changed} lines changed')
    else:
        print('No changes needed')
