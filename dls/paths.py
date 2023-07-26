from pathlib import Path
from typing import Callable, List, Union

from dls.extract import *


def filter_extensions(
    path: Path, extensions: List[str] = None
) -> List[Path]:
    if not extensions:
        extensions = ['.xlsx']
    if not path:
        return list()
    if path.is_file():
        path = path.parent
    paths = [p for p in path.glob('**/*') if p.suffix.lower() in extensions]
    return paths


def generate_preffix(extractor_fn: Callable) -> str:
    labels = {extract_size_by_intensity: "[size_by_intensity] ", 
              extract_correlation_fn: "[correlation_funcion] ",
              extract_size_results: "[size_results] ",
              extract_zeta_distribution: "[zeta_distribution] ",
              extract_phase_plot: "[phase_plot] ",
              extract_zeta_results: "[zeta_results] "}
    return labels.get(extractor_fn)
    

def validate_path(input: str):
    if not input:
        return None
    return Path(input)


def ensure(path: Path) -> Path:
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def generate_path(data_file: Path, replicate_index: Union[int, str], extractor_fn: Callable) -> Path:
    dirs = {extract_size_by_intensity: "size_by_intensity", 
            extract_correlation_fn: "correlation_function",
            extract_size_results: "size_results",
            extract_zeta_distribution: "zeta_distribution",
            extract_phase_plot: "phase_plot",
            extract_zeta_results: "zeta_results"}
    new_dir = Path(dirs.get(extractor_fn))
    new_path = ensure(data_file.parent/new_dir)
    new_file_name = generate_preffix(extractor_fn) + data_file.stem + f"_{replicate_index}{data_file.suffix}"
    return new_path/new_file_name


def handle_input(placeholder) -> List[Path]:
    data_input = input(placeholder)
    files_to_process = filter_extensions(validate_path(data_input))
    return files_to_process
