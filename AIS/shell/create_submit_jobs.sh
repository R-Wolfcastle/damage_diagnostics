
#!/bin/bash

source /nobackup/eetss/BISICLES/.bstart

version_number="5_pc_1e6_nomsh"
domain="ASE"

control_template_filepath="/resstore/b0133/eetss/BISICLES/damage_regularisation/data/inversion_sensitivity/inputs/ASE/inputs.ase_sentinel_noisy_mega.inv.template"
local_vel_input_dir="/nobackup/eetss/BISICLES/damage_regularisation_study/inversion_sensitivity/inputs/ASE/v_${version_number}/"
mkdir -p ${local_vel_input_dir}

vel_input_files=$(find /resstore/b0133/eetss/BISICLES/damage_regularisation/data/inversion_sensitivity/inputs/ASE/ -name "ase_init_noisy_*pc_mega_*.hdf5")
for file in "${vel_input_files[@]}"; do
	cp $file ${local_vel_input_dir} 
done
vel_input_files=$(find ${local_vel_input_dir} -name "ase_init_noisy_*pc_mega_*.hdf5")

make_inputs_file () {
    local vif_tag=$1
    local control_template_filepath=$2
    local dam_reg_param=$3
    local vel_inputs_fp=$4

    control_template_filename=$(echo ${control_template_filepath} | awk -F '/' '{print $NF}')
    fn_stub=${control_template_filename%".inv.template"}
    new_fn=${fn_stub}_${vif_tag}.inv

    cp ${control_template_filepath} ./${new_fn}

    #sed -i "238s/.*/control.oneMinusMuSqRegularization = ${dam_reg_param}/" $new_fn
    sed -i "s/ASSIGN_ALPHA_PHI/${dam_reg_param}/" ${new_fn}
    ####sed -i "215s/.*/control.xVel.fileFormat = ${vel_inputs_fp}/" $new_fn ##slashes seem to be a problem here...
    sed -i "s|ASSIGN_DIR|${vel_inputs_fp}|" ${new_fn}

    echo ${new_fn}
}

make_qsub_script () {
    local control_filepath=$1

cat >"qsub_script.sh"<<EOF

#!/bin/bash

#$ -cwd -V
#$ -l h_rt=08:00:00
#$ -pe smp 8
#$ -l h_vmem=4G

date
bash /resstore/b0133/eetss/BISICLES/damage_regularisation/scripts/inversion_sensitivity/shell/run_executable.sh ${control_filepath}
date

EOF
}

reg_params=("0.0" "1e+6")
for vif in ${vel_input_files[@]}; do
    echo $vif
    for reg_param in "${reg_params[@]}"; do
        vif_tag=$(echo $vif | awk -F '/' '{print $NF}' | awk -F '_' '{print $5_$6}' | awk -F '.' '{print $1}')
        target_dir=/nobackup/eetss/BISICLES/damage_regularisation_study/inversion_sensitivity/output/${domain}/v_${version_number}/${vif_tag}/${reg_param}
        mkdir -p $target_dir || exit -1
        cd $target_dir || exit -1


        inputs_file_name="$(make_inputs_file ${vif_tag} ${control_template_filepath} ${reg_param} ${vif})"
   
        make_qsub_script ${inputs_file_name}

        echo $vif_tag "--->" $target_dir
        
        qsub ${target_dir}/qsub_script.sh
    done
done


