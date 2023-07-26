from collections import defaultdict
import logging

from dls.export import export
from dls.extract import *
from dls.paths import *

logging.basicConfig(level=logging.INFO)


def main():
    size_files_to_process = handle_input("Caminho da pasta com arquivos XLSX de tamanho hidrodinâmico: ")
    zeta_files_to_process = handle_input("Caminho da pasta com arquivos XLSX de potencial zeta: ")

    for size_file in size_files_to_process:
        size_replicates = read_replicates(size_file)
        size_replicates_to_concat = defaultdict(list)
        
        for repl_index, repl_data in size_replicates.items():
            size_by_intensity = extract_size_by_intensity(repl_data)
            size_replicates_to_concat["size_by_intensity"].append(size_by_intensity)
            size_by_intensity_path = generate_path(size_file, repl_index, extract_size_by_intensity)
            export(size_by_intensity, size_by_intensity_path)
            
            correlation_fn = extract_correlation_fn(repl_data)
            size_replicates_to_concat["correlation_fn"].append(correlation_fn)
            correlation_fn_path = generate_path(size_file, repl_index, extract_correlation_fn)
            export(correlation_fn, correlation_fn_path)
            
            size_results = extract_size_results(repl_data)
            size_replicates_to_concat["size_results"].append(size_results)
            size_results_path = generate_path(size_file, repl_index, extract_size_results)
            export(size_results, size_results_path)
            
        size_by_intensity_concat = pd.concat(size_replicates_to_concat["size_by_intensity"], axis=1)
        size_by_intensity_agg = size_by_intensity_concat.groupby(by=size_by_intensity_concat.columns, axis=1).mean()
        size_by_intensity_agg_path = generate_path(size_file, "mean", extract_size_by_intensity)
        export(size_by_intensity_agg, size_by_intensity_agg_path)
        
        correlation_fn_concat = pd.concat(size_replicates_to_concat["correlation_fn"], axis=1)
        correlation_fn_agg = correlation_fn_concat.groupby(by=correlation_fn_concat.columns, axis=1).mean()
        correlation_fn_agg_path = generate_path(size_file, "mean", extract_correlation_fn)
        export(correlation_fn_agg, correlation_fn_agg_path)
        
        size_results_concat = pd.concat(size_replicates_to_concat["size_results"], axis=1)
        size_results_concat_num = size_results_concat.iloc[:, 1::3]
        size_results_agg = size_results_concat_num.groupby(by=size_results_concat_num.columns, axis=1).mean()
        size_results_agg = pd.concat([size_results_concat.iloc[:, 0], size_results_agg], axis=1)
        size_results_agg_path = generate_path(size_file, "mean", extract_size_results)
        export(size_results_agg, size_results_agg_path)
        
        logging.info(f'[size] Processed {size_file}')
        
    for zeta_file in zeta_files_to_process:
        zeta_replicates = read_replicates(zeta_file)
        zeta_replicates_to_concat = defaultdict(list)
        
        for repl_index, repl_data in zeta_replicates.items():
            zeta_distribution = extract_zeta_distribution(repl_data)
            zeta_replicates_to_concat["zeta_distribution"].append(zeta_distribution)
            zeta_distribution_path = generate_path(zeta_file, repl_index, extract_zeta_distribution)
            export(zeta_distribution, zeta_distribution_path)
            
            phase_plot = extract_phase_plot(repl_data)
            zeta_replicates_to_concat["phase_plot"].append(phase_plot)
            phase_plot_path = generate_path(zeta_file, repl_index, extract_phase_plot)
            export(phase_plot, phase_plot_path)
            
            zeta_results = extract_zeta_results(repl_data)
            zeta_results_path = generate_path(zeta_file, repl_index, extract_zeta_results)
            export(zeta_results, zeta_results_path)
        
        zeta_distribution_concat = pd.concat(zeta_replicates_to_concat["zeta_distribution"], axis=1)
        zeta_distribution_agg = zeta_distribution_concat.groupby(by=zeta_distribution_concat.columns, axis=1).mean()
        zeta_distribution_agg_path = generate_path(size_file, "mean", extract_zeta_distribution)
        export(zeta_distribution_agg, zeta_distribution_agg_path)
        
        phase_plot_concat = pd.concat(zeta_replicates_to_concat["phase_plot"], axis=1)
        phase_plot_agg = phase_plot_concat.groupby(by=phase_plot_concat.columns, axis=1).mean()
        phase_plot_agg_path = generate_path(size_file, "mean", extract_phase_plot)
        export(phase_plot_agg, phase_plot_agg_path)
        
        zeta_results_concat = pd.concat(zeta_replicates_to_concat["zeta_results"], axis=1)
        zeta_results_concat_num = zeta_results_concat.iloc[:, 1::3]
        zeta_results_agg = zeta_results_concat_num.groupby(by=zeta_results_concat_num.columns, axis=1).mean()
        zeta_results_agg = pd.concat([zeta_results_concat.iloc[:, 0], zeta_results_agg], axis=1)
        zeta_results_agg_path = generate_path(size_file, "mean", extract_zeta_results)
        export(zeta_results_agg, zeta_results_agg_path)
        
        logging.info(f'[zeta] Processed {zeta_file}')
        
if __name__ == "__main__":
    main()
