#!/usr/bin/env python
import sys
import pandas as pd
from datetime import datetime
from mof_array.pmf.process_mass_data import (read_output_data,
                                            yaml_loader,
                                            write_output_data,
                                            import_experimental_results,
                                            import_simulated_data,
                                            calculate_pmf,
                                            create_bins,
                                            bin_compositions,
                                            array_pmf,
                                            plot_binned_pmf_array,
                                            save_array_pmf_data,
                                            save_raw_pmf_data,
                                            information_gain,
                                            choose_best_arrays)

# Import results as dictionary
sim_results_import = read_data_as_dict(sim_data)
exp_results_import = read_data_as_dict(exp_data)

filepath = 'settings/process_config.yaml'
data = yaml_loader(filepath)

mof_array = data['mof_array']
mof_densities_import = {}
mof_experimental_mass = {}

for mof in mof_array:
    mof_densities_import.copy()
    mof_densities_import.update({ mof : data['mofs'][mof]['density']})

num_mixtures = data['num_mixtures']
stdev = data['stdev']
mrange = data['mrange']
gases = data['gases']
number_mofs = data['number_mofs']
number_bins = data['number_bins']

calculate_pmf_results = calculate_pmf(experimental_mass_results, import_data_results, experimental_mofs, stdev, mrange)
array_pmf_results, list_of_arrays = array_pmf(gases, number_mofs, experimental_mofs, calculate_pmf_results, experimental_mass_mofs)
create_bins_results = create_bins(experimental_mofs, calculate_pmf_results, gases, number_bins)
bin_compositions_results = bin_compositions(gases, list_of_arrays, create_bins_results, array_pmf_results, experimental_mass_mofs)
kl_divergence = information_gain(gases, list_of_arrays, bin_compositions_results, create_bins_results)
ordered_by_kld_product, ordered_by_gas, all_arrays_ranked = choose_best_arrays(gases, number_mofs, kl_divergence)
(exp_results_full, exp_results_mass, exp_mof_list) = (
    import_experimental_data(exp_results_import, mof_list, mof_densities, gases) )
(sim_results_full) = (
    import_simulated_data(sim_results_import, mof_list, mof_densities, gases) )

pmf_results_df = pd.DataFrame(data=array_pmf_results)
save_raw_pmf_data(pmf_results_df, stdev, mrange, min(number_mofs))
plot_binned_pmf_array(gases, list_of_arrays, create_bins_results, bin_compositions_results)
save_array_pmf_data(gases, list_of_arrays, create_bins_results, bin_compositions_results)
write_output_data('saved_results/ordered_by_gas_%s.csv' % (datetime.now().strftime("%Y_%m_%d__%H_%M_%S")), ordered_by_gas)
write_output_data('saved_results/ordered_by_kld_product_%s.csv' % (datetime.now().strftime("%Y_%m_%d__%H_%M_%S")), ordered_by_kld_product)
write_output_data('saved_results/all_arrays_ranked_%s.csv' % (datetime.now().strftime("%Y_%m_%d__%H_%M_%S")), all_arrays_ranked)
