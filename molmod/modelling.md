---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling of the mouse MDM2 protein"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modelling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---
## General Overview
This tutorial is divided in 5 sections, each representing (roughly) a step of the homology modelling
procedure:  

- [A bite of theory](#a-bite-of-theory)  
- [Using Uniprot to retrieve sequence information](#using-uniprot-to-retrieve-sequence-information)  
- [Finding homologues of known structure using HMMER](#finding-homologues-of-known-structure-using-hmmer)  
- [Choosing a template from the list of homologues](#choosing-a-template-from-the-list-of-homologues)

## A bite of theory
The last decades of scientific advances in the fields of protein biology revealed the extent of both
the protein sequence and structure universes. Protein sequences databases currently hold tens of
millions of entries ([source](http://www.uniprot.org/statistics/)) and are foreseen to continue
growing exponentially, driven by high-throughput sequencing efforts. On the other hand, the number
of experimental protein structures is two orders of magnitude smaller ([source](http://www.rcsb.org/pdb/static.do?p=general_information/pdb_statistics/index.html)), and
that of unique folds has remained virtually unchanged since 2008. This apparent stagnation of the
protein structure universe is a boon for structure prediction enthusiasts, as finding a sequence
without a structurally characterized close homologue is, nowadays, quite rare.

<figure>
    <br>
    <a href="/images/molmod/rcsb-statistics.png">
        <img src="/images/molmod/rcsb-statistics.png">
    </a>
    <br>
    <figcaption>
        Growth of the protein structure database since its inception in 1974.
    </figcaption>
    <br>
</figure>

There are many methods for predicting the three-dimensional structure of proteins from their sequence,
most of which fall in one of three broad categories. Of this triumvirate, homology modelling is the
most reliable class of methods, with an estimated accuracy close to a low-resolution experimental
structure ([source](http://salilab.org/modeller/downloads/marc-bozi.pdf)). The two others, molecular
threading and _ab initio_ modelling, are usually of interest only if homology modelling is not an option.

Homology modelling is then a structure prediction method \- worth noting, not exclusively for proteins
\- that exploits the robustness of protein structure to changes in primary sequence. When protein
crystallography became routine in the 1980s, researchers started analysing and comparing
high-resolution structures. In doing so, they quickly realised that evolutionarily related proteins
shared common structural features and that the extent of this structural similarity directly
correlated with the sequence similarity ([source](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1166865/)).
To maintain structure and function, certain amino acids in the protein sequence suffer a stronger
selective pressure, evolving either slower than expected or within specific constraints, such as
chemical similarity. Combining these and other observations, early computational structural
biologists created the first homology modelling algorithms in the late 1980s/early 1990s.

## Using Uniprot to retrieve sequence information
Your goal is to create a model of the MDM2 mouse protein, in particular of its N-terminal region
that binds the p53 trans-activation domain. So, where do we start?

The Uniprot database is an online resource offering access to _all_ known protein sequences. Besides raw sequence data, Uniprot aggregates information from several other databases such as [RCSB PDB](http://www.rcsb.org) and its [European](http://www.ebi.ac.uk/pdbe) and [Japanese](http://www.pdbj.org) mirrors, NCBI [Pubmed](http://www.pubmed.org), [KEGG](http://www.genome.jp/kegg/), [Pfam](http://pfam.xfam.org/), and many others. This set of features makes Uniprot an obvious go-to resource when looking for information on any protein. There are two collections of sequences: Swiss-Prot, whose entries undergo manual annotation and revision, and TrEMBL, where the annotation is unsupervised. Consequently, if the entry for a particular protein of interest belongs to Swiss-Prot, it will be marked by a golden star/icon, and we can reliably (but not blindly!) trust its contents.

<a class="prompt prompt-info">
    Find the mouse MDM2 entry in Uniprot using the search box on the home page.
</a>

Take the time to browse through the Uniprot page of mouse MDM2. The header of the page lists the protein, gene, and organism names for this particular entry, as well as its unique Uniprot accession code. On the left, below the header, there is a sidebar listing the several sections of the page. We can use these to navigate directly to the 'Structure' section to verify if there are already published experimental structures for mouse MDM2. Fortunately, there aren't any; otherwise this tutorial would end here.

<a class="prompt prompt-question">
Given the lack of experimentally determined structures, how come there are plenty of structural annotations for mouse MDM2?
</a>

Besides reporting on experimental structures, Uniprot links to portals such as the [ProteinModelPortal](http://www.proteinmodelportal.org/), [SWISS-MODEL Repository](http://swissmodel.expasy.org/), and [ModBase](http://modbase.compbio.ucsf.edu/modbase-cgi/index.cgi), which regularly cross-reference sequence and structure databases in order to build homology models. These automated protocols are configured to create models only under certain conditions, such as sufficient sequence identity and coverage. Still, the template identification, target/template alignment, and modelling options are unsupervised, which may lead to severe errors in some cases. In general, these models offer a quick peek of what fold(s) a particular sequence can adapt and may as well serve as a starting point for further refinement and analyses. Nevertheless, if the model will be a central part of a larger study, it might be worth to invest time and effort in modelling a particular protein of interest with a set of dedicated protocols.

The following tab, "Family & Domains", lists structural and domain information derived either from experiments or by similarity to other entries. For the mouse MDM2 protein, it shows that it contains a SWIB domain and two zinc fingers and that it interacts with proteins such as USP2, PYHIN1, RFFL, RNF34, among others. Additional information displayed in the text offers additional insights on binding partners and interfaces.

<a class="prompt prompt-question">
Which region(s) of MDM2 bind p53 and which of those bind to the trans-activation domain?
</a>

From the introduction, we know that our region of interest in MDM2 interacts with the trans-activation region of p53 and does _not_ ubiquitinate it. The small print under the "Domain" header gives clues regarding possible p53 interfaces: "Region I is sufficient for binding p53"; "the RING finger domain [...] is also essential for [MDM2] ubiquitin ligase E3 activity toward p53". It seems, therefore, that _Region I_ is our modelling target, but besides this annotation, it is not listed anywhere on the Uniprot page. While this mystery has plenty of possible solutions, the easiest of which would be to search for a publication on the MDM2 domain organization, keep to the Uniprot page to find an answer.

Browsing further down the page, we find the "Sequences" tab and its listing of the several isoforms of this particular protein as they have been observed. One of these is classified as "canonical" while others are products of splicing events or mutations. The notes on isoform MDM2-p76 reveal that it lacks the first 47 amino acids and that it does _not_ bind p53. The interaction occurs then through the N-terminal of MDM2. Linking this information with that of the domain organization hints that the first region (positions 1-110) is very likely our modelling target. We can further refine this selection by choosing only the region comprising the SWIB domain (positions 27-107). Choose either the first region (positions 1-110), the SWIB domain, or whatever seems best in your opinion.

<a class="prompt prompt-question">
Why can the first ~20 amino acids of MDM2 be neglected for the modelling?
</a>

Clicking on the "position(s)" column of a particular region/domain opens a new window showing the corresponding sequence as well as the region in the context of the full sequence. Although this window provides a shortcut to launch a BLAST similarity search against the UniprotKB (or another) database, we will use other more sensitive methods for this purpose. For now, pay attention to the sequence and its format. Named FASTA after the software program it was first implemented in, it is perhaps the most widely used file format in bioinformatics, owing surely to its readability for both humans and machines.

{% highlight bash %}
>sp|P23804|1-110
MCNTNMSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQY
IMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAV
{% endhighlight %}

For each sequence in the file, it contains a header line starting with `>` followed by an identifier. In the Uniprot page, the identifier contains the entry's collection (sp - Swiss-Prot), accession code, and region of the sequence. The information on this header is used by several programs in many different ways, so it makes sense to keep it simple and readable.

<a class="prompt prompt-info">
Change the identifier to something more meaningful and human (e.g. MDM2_MOUSE).
</a>

The next line(s) contains the sequence in the standard one-letter code. Any character other than an upper case letter will cause some (not all) programs to throw an error about the format of the sequence. Although there is not a strictly enforced character limit, it is customary to split the sequence into multiple lines of 80 characters each. This limit, as many others based on character length, is a legacy from the old days when screen resolutions were small or terminals the only way of interfacing with the computer. Nevertheless, some programs will complain, or even worse, truncate, sequences longer than these 80 characters, so it is wise to respect this limit!

<a class="prompt prompt-info">
Copy the FASTA-formatted sequence to a text file and save it under an appropriate name (e.g. MDM2_MOUSE.fasta).
</a>
<a class="prompt prompt-attention">
Save the file in the home directory, Downloads/ folder, or any other easily accessible location.
</a>

Now that we have a sequence, the following step is to find a suitable homolog to use in the modelling protocol. The several homology modelling methods available online, such as the [HHpred web server](http://toolkit.tuebingen.mpg.de/hhpred), need only this sequence to start the entire procedure. After a few minutes or hours, depending on the protocol, these servers produce models and a set of quality criteria to help the user make a choice. The downside of using a web server is that, usually, the modelling protocol is a 'black box'. It is impossible to control settings beyond which templates and alignment to use. It is important, however, to understand what is happening behind the scenes, to make conscious choices and grasp the limitations of each method and model. Therefore, this tutorial uses a set of locally installed programs to search for templates, build the models, and evaluate their quality.

## Finding homologues of known structure using HMMER
The _template_ is the structurally-resolved homolog that serves as a basis for the modelling. The _query_, on the other hand, is the sequence being modelled.  This standard nomenclature is used by several web servers, software programs, and literature in the field of structure modelling. The first step in any modeling protocol is, therefore, to find a suitable template for the query.

As mentioned before, there are computational methods that perform similarity searches against databases of known sequences. [BLAST](http://blast.ncbi.nlm.nih.gov/Blast.cgi) is the most popular of such methods, and probably the most popular bioinformatics algorithm, with two of its versions in the top 20 of the most cited papers in history ([source](http://www.nature.com/news/the-top-100-papers-1.16224)). It works by finding fragments of the query that are similar to fragments of sequences in a database and then merging them into full alignments ([source](http://www.ncbi.nlm.nih.gov/pubmed/23749753)). Another class of similarity search methods uses the query sequence to seed a general _profile sequence_ that summarises significant features in those sequences, such as the most conserved amino acids. This profile sequence is then used to search the database for homologues. This approach used in PSI-BLAST, an iterative version of BLAST, and also in [HMMER](http://hmmer.janelia.org), which employs an entirely different statistical framework.

<a class="prompt prompt-question">
What is the advantage of searching sequence databases with a "profile" sequence?
</a>

Whichever the sequence search algorithm, the chances are that, after running through the database, it returns a (hopefully) long list of results. Each entry in this list refers to a particular sequence, the hit, which was deemed similar to the query. It will contain the sequence alignment itself and also some quantitative statistics, namely the sequence similarity, the bit score of the alignment, and its expectation (E) value. Sequence similarity is a quantitative measure of how evolutionarily related two sequences are. It is essentially a comparison of every amino acid to its aligned equivalent. There are three possible outcomes out of this comparison: the amino acids are exactly the same, i.e. identical; they are different but share common physicochemical characteristics, i.e. similar; they are neither. It is also possible that the alignment algorithm introduced _gaps_ in either of the sequences, meaning that there was possibly an insertion or a deletion event during evolution. While identity is straightforward, similarity depends on specific criteria that group amino acids together, e.g. D/E, K/R/H, F/Y/W. The bit score is the likelihood that the query sequence is _truly_ a homologue of the hit, as opposed to a random match. The E-value represents the number of sequences that are expected to have a bit score higher than that of this particular alignment just by chance, given the database size. In essence, a very high bit score and a very small E-value is an assurance that the alignment is indeed significant and that this hit is likely a true homologue of the query sequence.

Our goal is to search for homologues in a sequence database containing exclusively proteins of known structure, such as [RCSB PDB](http://www.rcsb.org). This database is available in text format at the RCSB website and as a selection in most of the homology search web servers. Given the rather small size of these databases (~100k sequences), for reasonably sized sequences, searches take only a few seconds on a laptop.

Start by creating a folder to store all the information related to the modelling process. To keep the files easily accessible, create the folder in the home directory, for example.

<a class="prompt prompt-cmd">
    cd $HOME  
    mkdir mdm2_modelling  
    cd mdm2_modelling  
</a>

Assuming the Uniprot sequence file is in the Downloads folder, copy it to the newly created folder and launch a `phmmer` search against the RCSB PDB sequence database. `phmmer` is part of the HMMER suite and searches a query protein sequence against a database. Behind the scenes, it builds a profile HMM from the query sequence and uses this profile to search the database for homologs ([source](ftp://selab.janelia.org/pub/software/hmmer3/3.1b2/Userguide.pdf)).

<a class="prompt prompt-cmd">
    cp $HOME/Downloads/MDM2_MOUSE.fasta .  
    phmmer \-\-notextw -o psa.out -A psa.sto MDM2_MOUSE.fasta /opt/database/pdb_seqres.txt
</a>
<a class="prompt prompt-attention">
  Adapt the file names accordingly!
</a>

Take a moment to inspect that command. (Most) GNU/Linux commands start with the command or program name, after which follow arguments and options. Arguments are usually positional, meaning that there is a specific order that must be respected. A dash (`-`) symbol indicates an option. Some options do not take any values and act as a simple switch while others require a value. Usually, a well-written program supports a `-h` or `--help` option that will print useful information containing the program description and usage instructions. In this particular example, `phmmer` is the program being executed, `--notextw`, `-o psa.out`, and `-A psa.sto` are options, and the remaining are arguments. The output of `phmmer -h` shows that `-notextw` and `-o` are both output-related, referring to the maximum line width and output file name respectively. The remaining option, `-A`, forces HMMER to write the full alignments to a separate file. As for the arguments, it shows that the first must be the sequence file and the second the sequence database. Additionally, there are certain instructions that are not necessarily part of the command or explained in its documentation. These are part of the GNU/Linux system and deal mostly with the execution of the command and its input/output. This tutorial will use the ampersand (`&`) and the redirection (`>`) symbol repeatedly. The first runs a program in the background and prevents the terminal session from being blocked while the second to redirect the output of the command to a file. For more information, refer to a generic tutorial on command-line usage ([example](http://www.ee.surrey.ac.uk/Teaching/Unix/)).

Back to the homology modelling, depending on which MDM2 sequence HMMER used to seed the search, the results will vary.

<a class="prompt prompt-info">
    Open and inspect the phmmer output file.
</a>
<a class="prompt prompt-cmd">
    leafpad psa.out &
</a>

The output file, `psa.out`, contains detailed information on each hit of the database considered homologous to the query. The first lines, starting with a `#` character, show information on the search parameters and the version of HMMER used to carry it out. This information is always useful; it allows a user to trace back the specifics of a particular step of the modelling, therefore allowing some degree of reproducibility.
The interesting bit comes next, after a line stating the name and length of the query sequence, as read from the input FASTA file.

{% highlight Text only %}
Query:       MDM2_MOUSE  [L=110]
Scores for complete sequences (score includes all domains):
   --- full sequence ---   --- best 1 domain ---    -#dom-
    E-value  score  bias    E-value  score  bias    exp  N  Sequence Description
    ------- ------ -----    ------- ------ -----   ---- --  -------- -----------
      1e-64  218.8   0.1    1.2e-64  218.6   0.1    1.0  1  1z1m_A    mol:protein length:119  Ubiquitin-protein ligase E3 Mdm2
    1.2e-64  218.5   0.1    1.4e-64  218.3   0.1    1.0  1  2lzg_A    mol:protein length:125  E3 ubiquitin-protein ligase Mdm2
    2.2e-62  211.3   0.1    2.4e-62  211.2   0.1    1.0  1  2mps_A    mol:protein length:107  E3 ubiquitin-protein ligase Mdm2
{% endhighlight %}

For each hit, HMMER outputs a line with several statistics and ending with the name and description of the hit. The first value, the sequence E-value, is the most important as it shows the significance of the hit to the query sequence. The lower this value, the better. The second value is the bit score, a database size-independent metric related to the E-value. The higher, the better. In this section, HMMER shows only one entry per hit, but a hit can have multiple domains matching the query sequence. The statistics in the middle columns refer to the best scoring domain and the number of domains in each hit.

{% highlight Text only %}
Domain annotation for each sequence (and alignments):
>> 1z1m_A  mol:protein length:119  Ubiquitin-protein ligase E3 Mdm2
   #    score  bias  c-Evalue  i-Evalue hmmfrom  hmm to    alifrom  ali to    envfrom  env to     acc
 ---   ------ ----- --------- --------- ------- -------    ------- -------    ------- -------    ----
   1 !  218.6   0.1   6.1e-68   1.2e-64       1     110 []       1     110 [.       1     110 [. 0.99

  Alignments for each domain:
  == domain 1  score: 218.6 bits;  conditional E-value: 6.1e-68
  MDM2_MOUSE   1 mcntnmsvstegaastsqipaseqetlvrpkplllkllksvgaqndtytmkeiifyigqyimtkrlydekqqhivycsndllgdvfgvpsfsvkehrkiyamiyrnlvav 110
                 mcntnmsv t+ga +tsqipaseqetlvrpkplllkllksvgaq dtytmke++fy+gqyimtkrlydekqqhivycsndllgd+fgvpsfsvkehrkiy miyrnlv v
      1z1m_A   1 MCNTNMSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQYIMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV 110
                 8**********************************************************************************************************976 PP
{% endhighlight %}

The details of each hit and all its domains come next. The hit identifier and description are repeated, preceded by `>>`, and the domains are sorted by order of appearance in the sequence, not significance. The `c-Evalue` and `i-Evalue` values are conditional and independent E-values. The first represents the significance of this domain  _after establishing the hit is a homologue_, while the second measures the significance of the domain if it was the only one being identified. In general, this latter is the important metric. The next values are the boundaries of the local alignment, and the last is the expected accuracy per residues of the alignment. The actual domain alignments make up the remainder of the hit information and include the query sequence (or the matching fragment), a consensus sequence, and the hit sequence. The last line shows the posterior probabilities, i.e. the expected accuracy, of each position of the alignment, and can be used to gauge the less conserved regions of the sequence in the alignment. The last lines of the file show some statistics on the search itself and on the HMM model building
process.

<a class="prompt prompt-question">
How many sequences does the RCSB PDB database contain and how many of these matched our query?
</a>

Unlike BLAST or the HMMER web server, the local version of HMMER does not provide any sequence identity or similarity scores. Since these are crucial statistics for deciding on a template for the modelling, we provide a Python script based on the [Biopython](http://biopython.org) library to parse the sequences and calculate identities. Additionally, the script calculates how much of the query sequence the hit is matching, also known as coverage. Run the script on the `psa.out` file and save the results in a separate `psa.info` file using the `-o` option.

<a class="prompt prompt-cmd">
python /opt/bin/aln_stats.py psa.out -o psa.info
</a>

<a class="prompt prompt-info">
Open and inspect the contents of the alignment information file.
</a>

This newly created file aggregates, for each hit, information copied from the HMMER output file and newly calculated values of pairwise sequence identity and coverage. Its simple tabular format is very suitable to identify plausible templates.

{% highlight Text Only %}
#PDBID     E-value      Bit Score       Seq. Id.        Seq. Cov.       Hit Description
1z1m_A     1.0E-64         218.80           0.90            1.00        Ubiquitin-protein ligase E3 Mdm2
2lzg_A     1.2E-64         218.50           0.90            1.00        E3 ubiquitin-protein ligase Mdm2
2mps_A     2.2E-62         211.30           0.91            0.96        E3 ubiquitin-protein ligase Mdm2
4ode_A     1.8E-60         205.20           0.90            0.95        E3 ubiquitin-protein ligase Mdm2
4odf_A     1.8E-60         205.20           0.90            0.95        E3 ubiquitin-protein ligase Mdm2
{% endhighlight %}

Apparently, there are plenty of homologues with known structure for mouse MDM2. A quick survey of the `psa.info` file shows that more than half of the hits has a sequence identity of at least 90% to the query sequence, which is the best possible for modelling. Nevertheless, protein structures are surprisingly robust to changes in sequence. Major structural characteristics are conserved even at _low_ sequence identities (~30%). As a rule of thumb, any sequence above 30-35% sequence _similarity_ can be used to build a somewhat
reliable model ([source](http://peds.oxfordjournals.org/content/12/2/85.long)). It is still possible to model a sequence on a template with 20-30% sequence similarity, the so-called twilight zone, but there must be extreme care in choosing a proper template. Below 20%, in the danger zone, there is no guarantee that there is any sequence-structure correlation. Note, though, that all these are relative percentages to the sequence size.

<figure>
    <a href="/images/molmod/rcsb-statistics.png"><img src="/images/molmod/similarity-structures.png"></a>
    <figcaption>Structures of sequence homologues of the Ribosomal protein L5 (in red).</figcaption>
</figure>

Choosing a template is, however, more complex than just choosing the most identical homologue. Modelling might be a computational method, based on chemical principles, but its fundamental principle is biological. The tertiary structure of a protein defines its function, and as such, folds should be conserved across functionally similar proteins. Consequently, it _always_ pays off to consider the biological function of both the query and the templates and make sure that there is, if possible, a match. Otherwise, nature might have a trick left up in her sleeve ([example](http://www.pnas.org/content/104/29/11963.full)). In the case of mouse MDM2, most of the hits belong to the E3 ubiquitin ligase family,  and several of them are MDM2 proteins of other organisms. It seems then that it is very much possible and straightforward to model mouse MDM2. Finally, the coverage metric also shows that there are very few gaps in the alignment, but it is important to know where these are. If a particular hit has 90% coverage, there could have been an insertion event during evolution. Another possibility, more common, are gaps at one or both termini of the sequences. Either way, gaps are always a point of concern, and there must always be a good justification for building a model from such an alignment.

<a class="prompt prompt-question">
Why is it worrying to have several gaps in the middle of the sequence, opposite to having them at the termini?
</a>

The second file produced by HMMER (`psa.sto`) contains the full sequence alignments for each query/hit pair, which is useful to check where the gaps are in a particular sequence. The Stockholm format is not as easy to read as FASTA though. Fortunately, HMMER includes a library called `easel` whose utilities are very helpful in doing these conversions and manipulations of sequence (alignment) files.

<a class="prompt prompt-cmd">
esl-reformat afa psa.sto -o psa.fasta
</a>

<a class="prompt prompt-info">
Open and inspect the contents of the alignment FASTA file.
</a>

The `psa.fasta` file contains the same information as the Stockholm file, except for the forward probabilities, just in a different format. The two top scoring hits do not have any gap (coverage is 1.0). The next few hits have roughly 5% of gaps (coverage 0.95-0.96), which corresponds to ~5 positions in the alignment. Fortunately, these are distributed between the N and C termini of the protein sequence, or concentrated at the N-terminus. Indeed, even the worst scoring hits have a consistent region of gaps and a homologous core domain.

{% highlight Text Only %}
>1z1m_A/1-110 [subseq from] mol:protein length:119  Ubiquitin-protein ligase E3 Mdm2
MCNTNMSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQY
IMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV
>2lzg_A/1-110 [subseq from] mol:protein length:125  E3 ubiquitin-protein ligase Mdm2
MCNTNMSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQY
IMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV
>2mps_A/1-106 [subseq from] mol:protein length:107  E3 ubiquitin-protein ligase Mdm2
--NTNMSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQY
IMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLV--
>4ode_A/1-105 [subseq from] mol:protein length:105  E3 ubiquitin-protein ligase Mdm2
-----MSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQY
IMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV
>4odf_A/1-105 [subseq from] mol:protein length:105  E3 ubiquitin-protein ligase Mdm2
-----MSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQY
IMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVV
{% endhighlight %}

## Choosing a template from the list of homologues
The two closest homologues, as identified by HMMER, have both 90% sequence identity and 100% coverage. The question is thus, which of them should be used to model mouse MDM2? Most homology modelling methods, including MODELLER, can use either one or multiple templates to build the models. Using several different templates is only really advantageous, however, in the case where they provide a better coverage of the query sequence ([source](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2386743/)). If one template matches the first half of the sequence and another the second half, then both can and should be used to build the full model. Otherwise, a single template with large enough coverage is sufficient to build a high-quality model. Since the N-terminal region of MDM2 that interacts with p53 seems to be a single domain, judging by the consistency of the HMMER results, the best course of action is the use a single template.

As previously mentioned, the main criteria to choose a template are its sequence identity to the query, the coverage, and the biological function. Beyond sequence features and function, it is also important to judge the structural quality of the templates. For example, structures determined by X-ray crystallography differ in the accuracy of the atomic positions in the final structure. On the other hand, NMR structures are built from a collection of experimental (distance, but not only) restraints that can rarely be satisfied by one single conformation. This ambiguity makes NMR structures relatively poor templates, as there is no _best_ model of an ensemble, only one with fewer restraints violations. Additionally, it is not straightforward to discern why a region is _floppy_ in the NMR ensemble: different restraints or a lack of thereof? Unlike NMR structures, X-ray structures have well-defined quality criteria, namely resolution and R-free. The resolution is a measure of the level of detail in the diffraction pattern, which translates to the unambiguity with which atoms fit into the electron density map. Ultra-high resolution structures have values below 1Å. The R-free value reflects the agreement of the final structure with a part of the diffraction data left aside for validation, i.e. a cross-validation measure. An average structure has an R-free value of 0.26, and the lower, the better ([source](http://www.rcsb.org/pdb/101/static101.do?p=education_discussion/Looking-at-Structures/resolution.html)). This preference is of course relative. Between two equally good structures, that determined by crystallography is likely best; however, if the NMR structure is far better in terms of sequence identity, for example, it becomes the obvious template. In this latter case, it might be productive to perform several _different_ single-template modelling runs, each using a different member of the NMR ensemble.

To gain some insight on the structural quality of the templates suggested after the HMMER search, use the [RCSB PDB](http://www.rcsb.org) database. The first column of the `psa.info` file contains the PDB ID and the PDB chain belonging to the hit sequence. The ID is a four-character alphanumerical code (e.g. `1z1m`) that is unique to each structure, much like the accession code is for an Uniprot entry.

<a class="prompt prompt-info">
Look for the entries of the best five homologues in the RCSB PDB database, using the search bar and the PDB IDs.
</a>

The three highest scoring templates identified by HMMER  (`1z1m_A`, `2lzg_A`, and `2mps_A`) are all NMR structures. The fourth, `4ode_A`, is a crystal structure that given its values of sequence identity (90%) and coverage (95%) is likely the best candidate. The RCSB PDB page for this entry confirms what HMMER reported: the structure belongs to the E3 ubiquitin-protein ligase Mdm2 of *Homo sapiens*. Further, the "Experimental Details" and "Structure Validation" sections detail the high quality of this structure: 1.80Å resolution and above-average R-free and stereochemistry parameters for structures of similar resolution.

Another factor to consider when choosing a template is its conformation in the crystal structure (or NMR ensemble) and experimental conditions under which the structure was obtained. The presence of co-factors, ligands, and other molecules might have a large impact on the conformation the protein adopts and, therefore, have a direct influence on the choice of using a structure as a template. A possible way of checking the conformational space, or at least its characterized fraction, is to analyze all the released structures related to this particular template. In the case of mouse MDM2, this means analyzing all the homologous MDM2 proteins HMMER found. Superimposing these structures and calculating overall and per-residue root mean square deviations (RMSD) of equivalent atomic coordinates gives a simple and clear answer to this problem.

There are several programs that allow a user to download, visualize, and (quantitatively) compare structures. This tutorial uses PyMOL, a free and open-source molecular visualization software that runs on Windows, MacOS X, and Linux. If necessary, download it [here](http://pymol.org/dsc/). For any help with the commands, visit first the
[community-maintained Wiki](www.pymolwiki.org) and then use Google; the chances are that someone else already posted that same problem in the PyMOL mailing-list.

<a class="prompt prompt-info">
Using PyMOL, download the structures of the top 10 templates and superimpose their structures.
</a>

<a class="prompt prompt-pymol">
fetch 1z1m 2lzg 2mps, async=0  
fetch 4ode 4odf 4ogn 4ogt 4wt2 4hbm 4hbm, async=0, type=pdb1  
split_states 1z1m  
split_states 2lzg  
split_states 2mps  
delete 1z1m or 2lzg or 2mps  
select scaffold, 4ode and chain A and name ca  
alignto scaffold  
</a>
