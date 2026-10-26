set -eu
cd /work
python /evidence/verify_source.py > /evidence/source-final-commit.json
mkdir -p /evidence/artifacts/final
python -m build --outdir /evidence/artifacts/final
python -m pip install --disable-pip-version-check twine
python -m twine check /evidence/artifacts/final/*
python -m venv /runtime-candidate-final
/runtime-candidate-final/bin/pip install /evidence/artifacts/final/*.whl
cd /tmp
/runtime-candidate-final/bin/python /evidence/file_roundtrip.py candidate final
python /evidence/verify_source.py > /evidence/source-after-final-build.json
git -C /work status --porcelain
git -C /work rev-parse HEAD
git -C /work rev-parse HEAD^{tree}
