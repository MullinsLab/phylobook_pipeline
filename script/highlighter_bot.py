import re, os, sys, wget, glob, time, argparse
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
import shutil
from robobrowser import RoboBrowser

import highlighter
from Bio import AlignIO, Phylo
from Bio.Align.AlignInfo import Highlighter
from Bio.Graphics import HighlighterPlot

from utils import SequenceNameShortenizer, SortFasta

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--aminoacid", help="flag for amino acid sequence", action="store_true")
parser.add_argument("-d", "--dir", help="directory to hold input sequence fasta file", nargs="?", const=1, type=str, default=".")
parser.add_argument("-f", "--file", help="specific file to operate on", nargs="?", const=1, type=str, default=None)
parser.add_argument("-w", "--width", help="width of marks in the highlighter plot", nargs="?", const=1, type=int, default=3)

args = parser.parse_args()
aaflag = args.aminoacid
path = args.dir
specific_file = args.file
width: int = args.width

files = []
for file in glob.glob(os.path.join(path, '*.fasta')):
    if re.search("_highlighter.fasta", file) is None:
        if not specific_file or file == os.path.join(path, specific_file):
            files.append(file)

num_files = len(files)
filenum = 0
full_time = time.time()

for file in files:
    filenum += 1
    job_time = time.time()

    alignmentFilePath = file
    cur_seq_path = os.path.splitext(file)[0]
    cur_seq_name = os.path.basename(cur_seq_path)
    treeFilePath = cur_seq_path+'.phy_phyml_tree.txt_newick.tre'
    # tmpAlignmentFilePath = os.path.join(path, '0_tmp.fasta')
    # tmpTreeFilePath = os.path.join(path, '0_tmp_newick.tre')
    save_png = os.path.join(cur_seq_path + '_highlighter.png')
    save_svg = f"{cur_seq_path}_highlighter.{width}.svg"
    save_data = os.path.join(cur_seq_path + '_highlighter.txt')
    save_rearr_fasta = os.path.join(cur_seq_path + '_highlighter.fasta')

    print("cur_seq_path: " + cur_seq_path)
    print("cur_seq_name: " + cur_seq_name)
    print("alignmentFilePath: " + alignmentFilePath)
    print("treeFilePath: " + treeFilePath)
    print("save_png: " + save_png)
    print("save_svg: " + save_svg)
    print("save_data: " + save_data)
    print("save_rearr_fasta: " + save_rearr_fasta)
    
    if not os.path.isfile(alignmentFilePath):
        sys.exit("File not found: " + alignmentFilePath)

    if not os.path.isfile(treeFilePath):
        print("Tree file not found: " + treeFilePath + ", skipped processing.")
        continue

    if os.path.isfile(save_png):
        print('Skipping {}, PNG already exists'.format(cur_seq_name))
        continue

    if os.path.isfile(save_data):
        print('Odd, data file .txt exists but not PNG for {}. Proceeding anyway.'.format(cur_seq_name))

    alignment = AlignIO.read(alignmentFilePath, "fasta")
    tree = Phylo.read(treeFilePath, "newick")

    # Create a sorted fasta
    SortFasta(alignment, tree, save_rearr_fasta)
    
    # Shortenize the sequence names
    try:
        shortenizer = SequenceNameShortenizer(alignment)

        for sequence in alignment:
            sequence.id = shortenizer.shortenize(sequence.id)
            
        for terminal in tree.get_terminals():
            terminal.name = shortenizer.shortenize(terminal.name)
    except:
        pass

    seq_type: str = "AA" if aaflag else "NT"

    # Create image files
    highlighter_plot = HighlighterPlot(alignment, tree=tree, seq_type=seq_type, top_margin=12, seq_gap=-0.185*2, seq_name_font_size=16, ruler_font_size=12, plot_width=6*72, bottom_margin=45, left_margin=0, right_margin=0, plot_label_gap=3)
    highlighter_plot.draw_mismatches(save_png, output_format="png", apobec=True, g_to_a=True, glycosylation=True, sort="tree", scheme="LANL", mark_width=width)
    highlighter_plot.draw_mismatches(save_svg, output_format="svg", apobec=True, g_to_a=True, glycosylation=True, sort="tree", scheme="LANL", mark_width=width)

    # Create data file
    highlighter = Highlighter(alignment, seq_type=seq_type)
    highlighter.export_mismatches(save_data, apobec=True, g_to_a=True, glycosylation=True)

    ####################################################
    # Origional system to get files from LANL hightler retained for historical purposes
    ####################################################
    
    # if filenames are too long, use temporary shorter filenames
    # if len(cur_seq_name) > 50:
    #     shutil.copyfile(alignmentFilePath, tmpAlignmentFilePath)
    #     shutil.copyfile(treeFilePath, tmpTreeFilePath)
    #     alignmentFilePath = tmpAlignmentFilePath
    #     treeFilePath = tmpTreeFilePath
    
    # browser = RoboBrowser(history=True, parser='lxml')
    # url = "https://www.hiv.lanl.gov/content/sequence/HIGHLIGHT/highlighter_top.html?choice=mismatches"
    # download_url = "https://www.hiv.lanl.gov"
    # #download_referer = "https://www.hiv.lanl.gov/cgi-bin/HIGHLIGHT/highlighter.cgi"
    # browser.open(url)
    # form = browser.get_form(action=re.compile(r'highlighter.cgi'))

    # form["alignmentFile"].value = open(alignmentFilePath, 'r')
    # form["uploadTree"].value = open(treeFilePath, 'r')
    # form["choice"].value = "mismatches"
    # form["sort"].value = "tree"
    # form["treeType"].value = "upload"
    # form["tw_multiplier"].value = "7"
    # form["submit"].value = ""  ### There are 2 input type="submit", we need the second one
    # if aaflag is True:
    # 	form["base"].value = "aa"
    # 	form["glyco"].value = "no" # or "no" if glycosolation information is not desired
    # else:
    # 	form["apobec"].value = "yes"

    # browser.session.headers['Referer'] = url

    # print('Submitting file {}/{}, {}'.format(filenum,num_files,cur_seq_name))
    # browser.submit_form(form)

    # # save the PNG and TXT results
    # anchors = browser.find_all('a', {'href': True})

    # image = None
    # data = None
    # rearr_fasta = None

    # for anchor in anchors:
    #     if "highlighter.png" in anchor['href'] and "[View large]" in anchor.contents[0]:
    #         image = download_url + anchor['href']
    #         data = download_url + anchor['href'][0:anchor['href'].index("png")] + "txt"
    #     elif "inseqs_rearr.fasta" in anchor['href']:
    #         rearr_fasta = download_url + anchor['href']

    # if image == None:
    #     sys.exit("No image for: " + cur_seq_name)

    # wget.download(image, save_png)
    # wget.download(data, save_data)
    # wget.download(rearr_fasta, save_rearr_fasta)

    # # clean up temporary files
    # if os.path.isfile(tmpAlignmentFilePath):
    #     os.remove(tmpAlignmentFilePath)
    # if os.path.isfile(tmpTreeFilePath):
    #     os.remove(tmpTreeFilePath)

    # jt = int(time.time() - job_time)
    # print('\nTook {} seconds to downloaded PNG, TXT, and FASTA from Highlighter for file: {}'.format(jt, cur_seq_name))

    # # please be courteous to the server's resources and do not reduce the sleep time between jobs below 60 seconds
    # if filenum != num_files:
    #     time.sleep(10)

ft = int(time.time() - full_time)
print('All done! Completed in {} seconds. Exiting.'.format(ft))
