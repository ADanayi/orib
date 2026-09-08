# gen/code_generator.py
import os
import shutil
from pathlib import Path


class CodeGenerator:
    def __init__(self, belt_dir: str):
        self.belt_dir = Path(belt_dir)

    def generate(self, output_dir: str, parameters: dict, ntb_source: str = None):
        """
        Copy BELT components and generate detector.py / sample.py.
        parameters: dictionary containing values for placeholders.
        ntb_source: path to a user-selected Python file containing create_ntb().
                    If provided, it will be copied to BELT/user_ntb.py and used.
                    If None, the default BELT/ntb.py will be used.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Copy the BELT package (excluding placeholder files)
        belt_out = output_dir / "BELT"
        if belt_out.exists():
            shutil.rmtree(belt_out)
        shutil.copytree(
            self.belt_dir,
            belt_out,
            ignore=shutil.ignore_patterns("__*.placeholder")
        )

        # 2. If user NTB file is provided, copy it into the BELT folder
        if ntb_source and Path(ntb_source).exists():
            shutil.copy2(ntb_source, belt_out / "user_ntb.py")
            ntb_file_value = 'os.path.join(os.path.dirname(__file__), "BELT", "user_ntb.py")'
        else:
            ntb_file_value = 'None'

        parameters["ntb_file_path"] = ntb_file_value

        # 3. Read placeholders, replace, write to output root
        det_placeholder = self.belt_dir / "__detector.py.placeholder"
        sample_placeholder = self.belt_dir / "__sample.py.placeholder"

        det_content = det_placeholder.read_text(encoding="utf-8")
        det_content = self._fill_template(det_content, parameters)
        (output_dir / "detector.py").write_text(det_content, encoding="utf-8")

        sample_content = sample_placeholder.read_text(encoding="utf-8")
        # sample.py may not contain placeholders, but we run anyway
        sample_content = self._fill_template(sample_content, parameters)
        (output_dir / "sample.py").write_text(sample_content, encoding="utf-8")

    @staticmethod
    def _fill_template(content: str, params: dict) -> str:
        for key, value in params.items():
            content = content.replace("{{" + key + "}}", str(value))
        return content