from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Phylo import BaseTree

class SequenceNameShortenizer(object):
    """ Class to shorten sequence names """

    def __init__(self, alignment: MultipleSeqAlignment):
        """ Set upt the shortenizer """

        self.alignment = alignment
        self.setup_tags()

    def setup_tags(self):
        """ Setup the tags """
        
        self.used_tags: list = []
        
        tags: dict[int: str] = {}
        tag_count: int = None

        for sequence in self.alignment:
            for index, tag in enumerate(sequence.id.split("_")):

                if tag_count is None:
                    tag_count = len(sequence.id.split("_"))
                elif tag_count != len(sequence.id.split("_")):
                    raise ValueError("All sequences must have the same number of tags")

                if index in self.used_tags:
                    continue

                if index not in tags:
                    tags[index] = tag
                
                elif tag != tags[index]:
                    self.used_tags.append(index)

    def shortenize(self, sequence_name: str) -> str:
        """ Shortenize a record """

        tags = sequence_name.split("_")
        new_tags = []

        for index in sorted(self.used_tags):
            new_tags.append(tags[index])

        return "_".join(new_tags)
    

class SortFasta(object):
    """ Class to sort a fasta file by tree order """

    def __init__(self, alignment: MultipleSeqAlignment, tree: BaseTree.Tree, file_name: str = None):
        """ Set up the sorter """

        self.old_alignment: MultipleSeqAlignment = alignment
        self.tree: BaseTree.Tree = tree
        self.new_alignment: MultipleSeqAlignment = MultipleSeqAlignment([])

        self.sort()

        if file_name is not None:
            self.file_name = file_name
            self.write()

    def sequence_by_name(self, sequence_name: str) -> str:
        """ Return the sequence from an alignment by name """

        for sequence in self.old_alignment:
            if sequence.id == sequence_name:
                return sequence

        raise ValueError(f"Sequence name {sequence_name} not found in alignment")
    
    def sort(self):
        """ Sort the alignment """

        for terminal in self.tree.get_terminals():
            self.new_alignment.append(self.sequence_by_name(terminal.name))

    def write(self):
        """ Write the new alignment out to a file """
            
        with open(self.file_name, "wt+") as file_handle:
            AlignIO.write(self.new_alignment, file_handle, "fasta")
