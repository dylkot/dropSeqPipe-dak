'''
Creates a bam file containing only reads with a cellbarcode that wasn't assigned as a core barcode, or as an error of a core barcode. This bam file can later be used to extract a soup profile.

It sets all cellbarcodes to AAAAAAAAAAAA so that they will all be merged together by DigitaGeneExpression.

It sets the UMI to the original cell barcode + the UMI. This will allow UMI error detection taking into account mismatches in either the cellbarcode or the UMI.
'''

import pickle
import pysam

def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)

infile_bam = pysam.AlignmentFile(snakemake.input.bam, "rb")
outfile = pysam.AlignmentFile(snakemake.output.bam, "wb", template=infile_bam)
barcode_ref = load_obj(snakemake.input.barcode_mapping_counts)

unused_barcodes = set(barcode_ref['unknown'].keys()) ## barcodes that aren't added to whitelist
generic_cellbarcode = 'AAAAAAAAAAAA'
open(snakemake.output.genericbarcode, 'w').write(generic_cellbarcode)
print('%d unused barcodes found' % len(unused_barcodes))

for bam_read in infile_bam:
    barcode = bam_read.get_tag('XC')
    if barcode in unused_barcodes:
        bam_read.set_tag('XC',generic_cellbarcode,value_type='Z',replace=True)
        UMI = bam_read.get_tag('XM')
        bam_read.set_tag('XM',barcode+UMI,value_type='Z',replace=True)
        outfile.write(bam_read)