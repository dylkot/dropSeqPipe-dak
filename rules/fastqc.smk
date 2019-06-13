"""Get fastqc reports"""

#Which rules will be run on the host computer and not sent to nodes
localrules:
    multiqc_fastqc_reads,
    multiqc_fastqc_barcodes
    make_adapter_txt



rule make_adapter_txt:
    input:
        adapter_fa
    output:
        adapter_txt
    script:
        '../scripts/make_fastqc_adapter_file.py'



rule fastqc_barcodes:
    """Create fastqc report"""
    input: 
        get_R1_files, adapter_txt
    output:
        html='{results_dir}/logs/fastqc/{sample}_R1_fastqc.html',
        zip='{results_dir}/logs/fastqc/{sample}_R1_fastqc.zip'
    params: '--extract --adapters {afn}'.format(afn=adapter_txt)
    wrapper:
        '0.31.1/bio/fastqc'

rule fastqc_reads:
    """Create fastqc report"""
    input: 
        get_R2_files, adapter_txt
    output:
        html='{results_dir}/logs/fastqc/{sample}_R2_fastqc.html',
        zip='{results_dir}/logs/fastqc/{sample}_R2_fastqc.zip'
    params: '--extract --adapters {afn}'.format(afn=adapter_txt)
    wrapper:
        '0.31.1/bio/fastqc'

rule multiqc_fastqc_barcodes:
    input:
        expand('{results_dir}/logs/fastqc/{sample}_R1_fastqc.html', sample=samples.index, results_dir=results_dir)
    output:
        html='{results_dir}/reports/fastqc_barcodes.html'
    params: '-m fastqc --ignore *_R2*'
    wrapper:
        '0.27.1/bio/multiqc'

rule multiqc_fastqc_reads:
    input: 
        expand('{results_dir}/logs/fastqc/{sample}_R2_fastqc.html', sample=samples.index, results_dir=results_dir)
    output:
        html='{results_dir}/reports/fastqc_reads.html'
    params: '-m fastqc --ignore *_R1*'
    wrapper:
        '0.27.1/bio/multiqc'
