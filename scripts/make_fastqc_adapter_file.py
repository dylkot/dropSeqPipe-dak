"""Snakemake wrapper for fastqc."""
def fa2tsv(fasta_in_fn, tsv_out_fn):
    'converts fasta file and outputs in tsv format'
    lines = open(fasta_in_fn).read().split('\n')[:-1]
    res = []
    for (i,l) in enumerate(lines):
        if (i % 2) == 0:
            newline = [l[1:]]
        else:
            newline.append(l)
            res.append(newline)

    
    with open(tsv_out_fn, 'w') as F:
        F.write('\n'.join(['\t'.join(x) for x in res]))

if __name__ == '__main__':
    fa2tsv(snakemake.input[0], snakemake.output[0])
