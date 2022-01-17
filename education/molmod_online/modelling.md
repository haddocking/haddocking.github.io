---
layout: page
title: "Homology Modeling of the mouse MDM2 protein"
excerpt: "Homology Modeling of the mouse MDM2 protein"
tags: [MODELLER, GROMACS, HADDOCK, molecular dynamics, homology modeling, docking, p53, MDM2]
image:
  feature: pages/banner_education-thin.jpg
---
## General Overview
{:.no_toc}

This tutorial is divided into various sections, each representing (roughly) a step of the homology modeling
procedure.

* table of contents
{:toc}


<hr>
## A bite of theory
The last decades of scientific advances in the fields of protein biology revealed the extent of both
the protein sequence and structure universes. Protein sequences databases currently hold tens of
millions of entries ([source](https://www.uniprot.org/statistics/){:target="_blank"}) and are foreseen to continue
growing exponentially, driven by high-throughput sequencing efforts. On the other hand, the number
of experimental protein structures is two orders of magnitude smaller
([source](https://www.rcsb.org/stats/growth/growth-released-structures){:target="_blank"}), and
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

There are many methods for predicting the three-dimensional structure of proteins from their
sequence,
most of which fall in one of three broad categories. Of this triumvirate, homology modeling is the
most reliable class of methods, with an estimated accuracy close to a low-resolution experimental
structure ([source](https://salilab.org/modeller/downloads/marc-bozi.pdf){:target="_blank"}). The two others, molecular
threading and _ab initio_ modeling, are usually of interest only if homology modeling is not an
option.

Homology modeling is then a structure prediction method \- worth noting, not exclusively for
proteins
\- that exploits the robustness of protein structure to changes in primary sequence. When protein
crystallography became routine in the 1980s, researchers started analyzing and comparing
high-resolution structures. In doing so, they quickly realized that evolutionarily related proteins
shared common structural features and that the extent of this structural similarity directly
correlated with the sequence similarity
([source](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1166865/){:target="_blank"}).
To maintain structure and function, certain amino acids in the protein sequence suffer a stronger
selective pressure, evolving either slower than expected or within specific constraints, such as
chemical similarity. Combining these and other observations, early computational structural
biologists created the first homology modeling algorithms in the late 1980s/early 1990s.


<hr>
## Using Uniprot to retrieve sequence information
Your goal is to create a model of the MDM2 mouse protein, in particular of its N-terminal region
that binds the p53 trans-activation domain. So, where to start?

The [Uniprot](https://www.uniprot.org){:target="_blank"} database is an online resource offering access to _all_ known
protein sequences. Besides raw sequence data, Uniprot aggregates information from several other
databases such as the [Worldwide PDB](https://www.wwpdb.org){:target="_blank"} (wwPDB) that archives information
about the 3D structures of proteins, nucleic acids, and complex assemblies and ensures that the PDB
is freely and publicly available to the global community, NCBI [Pubmed](https://www.ncbi.nlm.nih.gov/pubmed/){:target="_blank"},
[KEGG](https://www.genome.jp/kegg/){:target="_blank"}, [Pfam](https://pfam.xfam.org/){:target="_blank"}, and many others.
The wwPDB itself consists of several sites that all provide access in their own way to the wwPDB core database together with various associated services: The Research Collaboratory for Structural Bioinformatics PDB ([RCSB](https://www.rcsb.org){:target="_blank"}), PDB Europe ([PDBe](https://www.pdbe.org){:target="_blank"}) and PDB Japan ([PDBj](https://www.pdbj.org){:target="_blank"}), together with the Biological Magnetic Resonance Data Bank ([BMRB](https://bmrb.io/){:target="_blank"}) that collects NMR data.
These features of Uniprot makes it an obvious go-to resource when looking for information on any protein. There
are two collections of sequences: Swiss-Prot, whose entries undergo manual annotation and revision,
and TrEMBL, where the annotation is unsupervised. Consequently, if the entry for a particular
protein of interest belongs to Swiss-Prot, it will be marked by a golden star/icon meaning its
contents are very likely (but not blindly!) reliable.

<a class="prompt prompt-info">
  Find the mouse MDM2 entry in Uniprot using the search box on the home page.
</a>

Take the time to browse through the Uniprot page of mouse MDM2. The header of the page lists the
protein, gene, and organism names for this particular entry, as well as its unique Uniprot
accession code. On the left, below the header, there is a sidebar listing the several sections of
the page. You can use these to navigate directly to the **Structure** section to verify if there are
already published experimental structures for mouse MDM2. Fortunately, there aren't any; otherwise
this tutorial would end here.


Similarly as man, no protein is an island, entire of itself, every protein is a piece of the cell, a part of the main. Thus if we imagine the cytoplasm as a thick molecular soup, proteins are constantly in contact, interacting and exchanging information. To predict the entire cell interactome is close to impossible, however UniProt offers us a possibility to see experimentally confirmed interaction partners of proteins. Under **Interaction** you can see the available information about the interaction partners of MDM2. The 'Binary Interaction' subsection shows which is taken and regularly updated from the [InAct Database](https://www.ebi.ac.uk/intact/){:target="_blank"}. These interactions represent only those binary interactions, which were proven by more than one experiment. The complete IntAct set can be accessed using the link in the *Cross-references* section.

<a class="prompt prompt-question">
  Which proteins does MDM2 interact with and which interaction was most frequently confirmed? Where does the interaction with p53 take place?
</a>


You can navigate directly to the **Structure** section to verify if there are
already published experimental structures for mouse MDM2. Fortunately, there aren't any; otherwise
this tutorial would end here.


<a class="prompt prompt-question">
  Given the lack of experimentally determined structures, how come there are plenty of structural
annotations for mouse MDM2?
</a>

Besides reporting on experimental structures, Uniprot links to portals such as the
[SWISS-MODEL Repository](https://swissmodel.expasy.org/){:target="_blank"}, and
[ModBase](https://modbase.compbio.ucsf.edu/modbase-cgi/index.cgi){:target="_blank"}, which regularly cross-reference
sequence and structure databases in order to build homology models. These automated protocols are
configured to create models only under certain conditions, such as sufficient sequence identity and
coverage. Still, the template identification, target/template alignment, and modeling options are
unsupervised, which may lead to severe errors in some cases. In general, these models offer a quick
peek of what fold(s) a particular sequence can adapt and may as well serve as a starting point for
further refinement and analyses. Nevertheless, if the model will be a central part of a larger
study, it might be worth to invest time and effort in modeling a particular protein of interest
with a set of dedicated protocols.

The following tab, **Family & Domains**, lists structural and domain information derived either from
experiments or by similarity to other entries. For the mouse MDM2 protein, it shows that it
contains a SWIB domain and two zinc fingers and that it interacts with proteins such as USP2,
PYHIN1, RFFL, RNF34, among others. Additional information displayed in the text offers additional
insights on binding partners and interfaces.

<a class="prompt prompt-question">
  Which region(s) of MDM2 bind p53 and which of those bind to the trans-activation domain?
</a>

From the introduction, you know that our region of interest in MDM2 interacts with the
trans-activation region of p53 and does _not_ ubiquitinate it. The small print under the "Domain"
header gives clues regarding possible p53 interfaces: "Region I is sufficient for binding p53";
"the RING finger domain [...] is also essential for [MDM2] ubiquitin ligase E3 activity toward
p53". It seems, therefore, that _Region I_ is our modeling target, but besides this annotation, it
is not listed anywhere on the Uniprot page. While this mystery has plenty of possible solutions,
the easiest of which would be to search for a publication on the MDM2 domain organisation, keep to
the Uniprot page to find an answer.


Browsing further down the page, the **Sequences** tab lists the several isoforms of this particular
protein as they have been observed. One of these is classified as "canonical" while others are
products of splicing events or mutations. The notes on isoform MDM2-p76 reveal that it lacks the
first 49 amino acids and that it does _not_ bind p53. The interaction occurs then through the
N-terminal of MDM2. Linking this information with that of the domain organization hints that the
first region (positions 1-110) is very likely our modeling target. This selection can be further
refined by choosing only the region comprising the SWIB domain (positions 26-109). Choose either
the first region (positions 1-110), the SWIB domain, or whatever seems best in your opinion.

<a class="prompt prompt-question">
  Why can the first ~20 amino acids of MDM2 be neglected for the modeling?
</a>

Clicking on the *position(s)* column of a particular region/domain (*Family and Domains* section) opens a new window showing the
corresponding sequence as well as the region in the context of the full sequence. Although this
window provides a shortcut to launch a BLAST similarity search against the UniprotKB (or another)
database, there are other more sensitive methods for this purpose. For now, pay attention to the
sequence and its format. Named FASTA after the software program it was first implemented in, it is
perhaps the most widely used file format in bioinformatics, owing surely to its readability for
both humans and machines.

<pre style="background-color:#DAE4E7;padding:15px;margin:0px">
>sp|P23804|1-110
MCNTNMSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQY
IMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAV
</pre>

For each sequence in the file, it contains a header line starting with `>` followed by an
identifier. In the Uniprot page, the identifier contains the entry's collection (sp = Swiss-Prot),
accession code, and region of the sequence. The information on this header is used by several
programs in many different ways, so it makes sense to keep it simple and readable.

<a class="prompt prompt-info">
  Change the identifier to something more meaningful and human readable (e.g. MDM2_MOUSE).
</a>

The next line(s) contains the sequence in the standard one-letter code. Any character other than an
upper case letter will cause some (not all) programs to throw an error about the format of the
sequence. Although there is not a strictly enforced character limit, it is customary to split the
sequence into multiple lines of 80 characters each. This limit, as many others based on character
length, is a legacy from the old days when screen resolutions were small or terminals the only way
of interfacing with the computer. Nevertheless, some programs will complain, or even worse,
truncate, lines longer than these 80 characters, so it is wise to respect this limit!

<a class="prompt prompt-info">
  Copy the FASTA-formatted sequence to a text file and save it under an appropriate name (e.g.
MDM2_MOUSE.fasta).
</a>
<a class="prompt prompt-attention">
  Save the file in the home directory, Downloads/ folder, or any other easily accessible location.
</a>

Now that you have a sequence, the following step is to find a suitable homolog to use in the
modeling protocol. The several homology modeling methods available online, such as the
[HHpred web server](https://toolkit.tuebingen.mpg.de/tools/hhpred){:target="_blank"}, need only this sequence to start the
entire procedure. After a few minutes or hours, depending on the protocol, these servers produce
models and a set of quality criteria to help the user make a choice. The downside of using a web
server is that, usually, the modeling protocol is a 'black box'. It is impossible to control
settings beyond which templates and alignment to use. It is important, however, to understand what
is happening behind the scenes, to make conscious choices and grasp the limitations of each method
and model. Therefore, this tutorial uses a set of locally installed programs to search for
templates, build the models, and evaluate their quality.


<hr>
## Finding homologues of known structure using SWISS-MODEL

In the previous version of this course, we used multiple tools to search for sequence homologues, compare them and build a homology model. This year, to make this course accessible from remote locations, we will be using an online tool [SWISS-MODEL](https://swissmodel.expasy.org/){:target="_blank"}, which can conveniently perform above mentioned tasks and visualize both templates and created models.

The _template_ is the structurally-resolved homolog that serves as a basis for the modeling. The
_query_, on the other hand, is the sequence being modelled. This standard nomenclature is used by
several web servers, software programs, and literature in the field of structure modeling. The
first step in any modeling protocol is, therefore, to find a suitable template for the query.

As mentioned before, there are computational methods that perform similarity searches against
databases of known sequences. [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi){:target="_blank"} is the most popular
of such methods, and probably the most popular bioinformatics algorithm, with two of its versions
in the top 20 of the most cited papers in history
([source](https://www.nature.com/news/the-top-100-papers-1.16224){:target="_blank"}). It works by finding fragments of
the query that are similar to fragments of sequences in a database and then merging them into full
alignments ([source](https://www.ncbi.nlm.nih.gov/pubmed/23749753){:target="_blank"}). Another class of similarity
search methods uses the query sequence to seed a general _profile sequence_ that summarises
significant features in those sequences, such as the most conserved amino acids. This profile
sequence is then used to search the database for homologues.

<a class="prompt prompt-question">
  What is the advantage of searching sequence databases with a "profile" sequence?
</a>

Whichever the sequence search algorithm, the chances are that, after running through the database,
it returns a (hopefully) long list of results. Each entry in this list refers to a particular
sequence, the hit, which was deemed similar to the query. It will contain the sequence alignment
itself and also some quantitative statistics, namely the sequence similarity, the bit score of the
alignment, and its expectation (E) value. Sequence similarity is a quantitative measure of how
evolutionarily related two sequences are. It is essentially a comparison of every amino acid to its
aligned equivalent. There are three possible outcomes out of this comparison: the amino acids are
exactly the same, i.e. identical; they are different but share common physicochemical
characteristics, i.e. similar; they are neither. It is also possible that the alignment algorithm
introduced _gaps_ in either of the sequences, meaning that there was possibly an insertion or a
deletion event during evolution. While identity is straightforward, similarity depends on specific
criteria that group amino acids together, e.g. D/E, K/R/H, F/Y/W. The bit score is the likelihood
that the query sequence is _truly_ a homologue of the hit, as opposed to a random match. The
E-value represents the number of sequences that are expected to have a bit score higher than that
of this particular alignment just by chance, given the database size. In essence, a very high bit
score and a very small E-value is an assurance that the alignment is indeed significant and that
this hit is likely a true homologue of the query sequence.

Our goal is to search for homologues in a sequence database containing exclusively proteins of
known structure, such as [RCSB PDB](https://www.rcsb.org){:target="_blank"} and [PDBe](https://www.pdbe.org){:target="_blank"}. This database is available in text format
at the RCSB website and as a selection in most of the homology search web servers. Given the rather
small size of these databases (~100k sequences), for reasonably sized sequences, searches take only
a few seconds on a laptop.

[SWISS-MODEL](https://doi.org/10.1093/nar/gky427){:target="_blank"} is an online automated homology modelling tool available at [https://swissmodel.expasy.org](https://swissmodel.expasy.org){:target="_blank"}. On top of template search and homology modeling, the newest version of the software can now tackle the stoichiometry and the overall structure of a complex of multiple proteins based on the amino acid sequence of one or more interacting proteins. SWISS-MODEL has been available on the Internet since 1996 and uses ProMod3 as its modeling engine.


Working with SWISS-MODEL is very easy and straightforward. First you will need to visit [https://swissmodel.expasy.org](https://swissmodel.expasy.org){:target="_blank"} and click on **Start Modelling**.

### 1. Input data
On the first page you will see **Start a New Modelling Project** title. SWISS-MODEL can use multiple formats as input: protein sequence as plain text, FASTA, Clustal format or UniProtKB accession code. Clustal format is usually used for multiple sequence alignment with highlighting similarities and differences in sequences. Each aligned residue pair is marked with symbols:
`*` - perfect alignment, `:` - strong similarity, `.` - weak similarity.  Below, there is an example of an alignment of the full mouse MDM2 sequence aligned to the human MDM2 in Clustal format. This kind of alignment can be generated by UniProt, upon selecting organisms or isoforms you are interested it.


<pre style="background-color:#DAE4E7;padding:15px;margin:0px">
sp|P23804|MDM2_MOUSE      MCNTNMSVSTEGAASTSQIPASEQETLVRPKPLLLKLLKSVGAQNDTYTMKEIIFYIGQY  60
sp|Q00987|MDM2_HUMAN      MCNTNMSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQY  60
                          ******** *:**.:*****************************:*******::**:***

sp|P23804|MDM2_MOUSE      IMTKRLYDEKQQHIVYCSNDLLGDVFGVPSFSVKEHRKIYAMIYRNLVAVSQQ---DSGT  117
sp|Q00987|MDM2_HUMAN      IMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVKEHRKIYTMIYRNLVVVNQQESSDSGT  120
                          ************************:***************:*******.*.**   ****

sp|P23804|MDM2_MOUSE      SLSESRRQPEGGSDLKDPLQAPPEEKPSSSDLISRLSTSSRRRSISETEENTDELPGERH  177
sp|Q00987|MDM2_HUMAN      SVSENRCHLEGGSDQKDLVQELQEEKPSSSHLVSRPSTSSRRRAISETEENSDELSGERQ  180
                          *:**.* : ***** ** :*   *******.*:** *******:*******:*** ***:

sp|P23804|MDM2_MOUSE      RKRRR----SLSFDPSLGLCELREMCSGGSSSSSSSSSESTETPSHQDLDDGVSEHSGDC  233
sp|Q00987|MDM2_HUMAN      RKRHKSDSISLSFDESLALCVIREICCERSS-----SSESTGTPSNPDLDAGVSEHSGDW  235
                          ***::    ***** **.** :**:*.  **     ***** ***: *** ********

sp|P23804|MDM2_MOUSE      LDQDSVSDQFSVEFEVESLDSEDYSLSDEGHELSDEDDEVYRVTVYQTGESDTDSFEGDP  293
sp|Q00987|MDM2_HUMAN      LDQDSVSDQFSVEFEVESLDSEDYSLSEEGQELSDEDDEVYQVTVYQAGESDTDSFEEDP  295
                          ***************************:**:**********:*****:********* **

sp|P23804|MDM2_MOUSE      EISLADYWKCTSCNEMNPPLPSHCKRCWTLRENWLPDDKGKDKVEISEKAKLENSAQAEE  353
sp|Q00987|MDM2_HUMAN      EISLADYWKCTSCNEMNPPLPSHCNRCWALRENWLPEDKGKDKGEISEKAKLENSTQAEE  355
                          ************************:***:*******:****** ***********:****

sp|P23804|MDM2_MOUSE      GLDVPDGKKLTENDAKEPCAEEDSEEKAEQTPLSQESDDYSQPSTSSSIVYSSQESVKEL  413
sp|Q00987|MDM2_HUMAN      GFDVPDCKKTIVNDSRESCVEENDD-KITQASQSQESEDYSQPSTSSSIIYSSQEDVKEF  414
                          *:**** **   **::* *.**:.: *  *:  ****:***********:*****.***:

sp|P23804|MDM2_MOUSE      K-EETQDKDESVESSFSLNAIEPCVICQGRPKNGCIVHGKTGHLMSCFTCAKKLKKRNKP  472
sp|Q00987|MDM2_HUMAN      EREETQDKEESVESSLPLNAIEPCVICQGRPKNGCIVHGKTGHLMACFTCAKKLKKRNKP  474
                          : ******:******: ****************************:**************

sp|P23804|MDM2_MOUSE      CPVCRQPIQMIVLTYFN 489
sp|Q00987|MDM2_HUMAN      CPVCRQPIQMIVLTYFP 491
                          ****************
</pre>

<br>

<a class="prompt prompt-info">
 Copy the sequence of mouse MDM2 in to the input field or upload your fasta file. Select a project name. Let's call the project *'MDM2_MOUSE'*.
</a>

Below the project name there is an option to write down your e-mail and the result link will be sent to your e-mail address. This is very handy if you want to come back and inspect your results later, possibly using them for your future report.

SWISS-MODEL offers you the possibility to submit your own template too. This is not the scenario we will use in this course, however if you want to use a concrete template to build a model from, this option is useful.

### 2. Template search

After you inserted the amino acid sequence, which serves as query for template search, on the next page there will be all found templates listed.
SWISS-MODEL uses its own database [STML](https://www.ncbi.nlm.nih.gov/pubmed/24782522){:target="_blank"} to search against when looking for related protein structure for this query. STML [https://swissmodel.expasy.org/templates/](https://swissmodel.expasy.org/templates/){:target="_blank"} is a curated template library updated regularly with the new PDB release, containing templates for more than 120000 unique protein sequences.

SWISS-MODEL uses two databases to search through: fast and accurate [BLAST](https://www.ncbi.nlm.nih.gov/pubmed/9254694){:target="_blank"}, mostly used for closely related templates and more sensitive and time consuming [HHblits](https://www.ncbi.nlm.nih.gov/pubmed/22198341){:target="_blank"}, in cases of remote homology.

After you submitted your template search, you can see a log of individual steps and engines being used.

More about these steps and SWISS-MODEL publications are listed [here](https://swissmodel.expasy.org/docs/references){:target="_blank"}. For example two most recent and relevant ones:
* [SWISS-MODEL Repository](https://dx.doi.org/10.1093/nar/gkw1132){:target="_blank"}
* [SWISS-MODEL Workspace/ GMQE](https://doi.org/10.1093/nar/gky427){:target="_blank"}.


### 3. Template selection


Once the template search is finished, template quality is estimated by two methods.
These are [Global Model Quality Estimate (GMQE)](https://www.ncbi.nlm.nih.gov/pubmed/24782522){:target="_blank"} and [Quaternary Structure Quality Estimate (QSQE)](https://www.nature.com/articles/s41598-017-09654-8){:target="_blank"}. **GMQE** combines properties from the target–template alignment and the template structure and expresses the expected accuracy or reliability of the model. GMQE ranges between 0 and 1 with 1 being the highest accuracy and 0 the lowest. The **QSQE** score also ranges between 0 and 1, however it is only computed on the top ranked templates if there is a possibility to build an oligomer. A value above 0.7 is considered reliable.


<a class="prompt prompt-info">
Which oligomeric state is preferred for our future work? Be careful to select the right oligomeric state before building a model. Keep in mind that p53 binds to MDM2 in a 1:1 ratio.
</a>

#### Template Results

Except for GMQE and QSQE, sequence identity, experimental method, oligo states and ligands of these experimental structures are listed for all found templates in the **Templates** tab. It is possible to sort templates by all of these properties by toggling the symbols next to them. Moreover you can select a few to compare in the NGL molecular viewer on the right side.


<a class="prompt prompt-info">
Inspect the Template Results page. How many templates were found and what is the sequence coverage?
</a>


After clicking on the arrow `﹀` on the left a short preview of the template will appear. Here you see again the experimental method, with which was the template structure obtained, alignment method, sequence similarity and more information about the biounit. Below one can see the sequence alignment between the query sequence and the template.

The **oligomeric state** is predicted for each template and user can modify it manually under "target prediction". A warning sign appears if the oligomeric state of the model doesn't exactly match the one of the template (for example not all chains of the biounit included in the model).

As a rule of thumb, in homology modelling it is recommended to use X-ray crystal structures with a resolution higher than $$2.2Å$$ as templates. One has to often compromise between high sequence identity/similarity and **template resolution**. In general structures determined by X-ray crystallography are preferred over averaged NMR structures and structures determined with electron microscopy, as the latter determines the overall shape of the molecule not individual atoms locations.


 **Sequence similarity** between the sequence and the template is calculated from a normalized [BLOSUM62](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC50453/){:target="_blank"} substitution matrix and similarly as the QSQE score, it ranged between 0 and 1 with 1 as 100% sequence similarity and vice versa. Gaps are not taken into account while calculating the sequence similarity.


A cogwheel icon `⚙` on the left side of the sequence alignment or in the NGL viewer indicates additional options for sequence and structure coloring and format. One can select the type of secondary structure assignment algorithm: DSSP, PSIPRED, SSpro. Notice how the secondary structure changes between different algorithms. Another option one can choose between is color scheme based on the residue properties.

<a class="prompt prompt-info">
Have a look at found templates and their properties.
</a>


The NGL viewer offers an option to toggle between different protein representations as well as to create and save template figures. Notice how you can see residues names after you hover over them with your cursor.  One of the coloring options is by `bValue Range`. The B-value or the temperature factor refers to the displacement of atoms from their mean position in a crystal structure and reach the value between 0 and 1. It describes the local mobility of the macromolecule, with 0 being the most mobile parts, and in this case marked red.

<a class="prompt prompt-question">
How do the residues properties change depending on the position in the protein? For example polar, hydrophobic or aromatic residues. Which parts of the protein are more stable and which on the other hand more flexible?
</a>

<img src="/education/molmod_online/SM_colors.png">

Color scheme explanations taken from: [https://swissmodel.expasy.org/docs/help](https://swissmodel.expasy.org/docs/help#colour_schemes){:target="_blank"}

Except for a list of templates, one can find their **Quaternary structure, Sequence Similarity comparison and Alignment of Selected Templates** tabs on the top.

The **Quaternary Structure** view show clustered templates according to their oligomeric state, stoichiometry, topology and interface similarity.

*Protein–protein interaction (PPI) Fingerprint* shows how conserved residues are on the protein interfaces compared to the surface residues interacting with he solvent. This is naturally calculated only for templates in oligomeric states. A negative value of interface conservation (y-axis) indicates that interface residues are more conserved compared to surface residues. This estimate of conservation is derived from a multiple sequence alignment of homologous proteins using different identity cut-offs (x-axis). The interface conservation can be quite useful in defining how well template interfaces adapt to the target protein family. Thus, the closes homologues should reach the lowest interface conservation values in the highest possible identity cut-off.


In the **Sequence Similarity** plot templates are clustered by their sequence identity and are represented by circles.
Thus, templates with high sequence identity form clusters, further away from clusters of lower sequence identity.
The distance between templates is proportional to the sequence identity between them. You can see the name and the structure of each template by hovering over with your mouse.

<a class="prompt prompt-question">
Which templates show the evolutionary most conserved interface? Is this good?
</a>


If one selects multiple templates by checking the window in the **Templates** tab, their sequence alignment is shown in **Alignment of Selected Templates**. By clicking on the `More` button, one can see the complete list of templates not shown in this preview, download the Template Search Log or PDB structures of selected templates.


<a class="prompt prompt-info">
Select appropriate templates based on the properties described above. Visually inspect the selected structures. Which one is the most complete one or show the highest resolution, identity or GMQE score? Once you are satisfied with your selection, click on `Build Models`.
</a>

***Tip:*** Select templates of varying quality and coverage now and compare models made from them in the following step.

### 4. Model building


This step might take a bit longer than previous steps, since we are actually creating new models. To build a model from a selected template, first the identical atom coordinates are transferred, insertions and non-conserved amino acid sidechains are modelled in. This step is performed by the ProMod3 modelling engine which is based on the [OpenStructure computational structural biology framework](https://pubmed.ncbi.nlm.nih.gov/23633579/){:target="_blank"}. ProMod3 extracts structural information from an aligned template structure in Cartesian space and if no suitable fragments are found, Monte Carlo sampling is employed to perform a conformational space search.  The new sidechain conformations, which cannot be found in the template are modelled based on the backbone dependent [rotamer library](https://pubmed.ncbi.nlm.nih.gov/21645855/){:target="_blank"}. In the final stage, small structural distortions or steric clashes are resolved by a short energy minimization using the [CHARMM27](https://pubmed.ncbi.nlm.nih.gov/15185334/){:target="_blank"} forcefield.

### 5. Model estimation

Similarly as in Template selection, the list of built models is shown in **Model Results**.
After clicking on individual models, you can examine their quality in multiple ways and plots next to seeing their 3D structure in the NGL viewer on the right.


**GMQE** (Global Model Quality Estimation) is  is expressed as a number between 0 and 1, reflecting the expected accuracy of a model built with that alignment and template, normalized by the coverage of the target sequence. Higher numbers indicate higher reliability. GMQE takes contains also QMEAN to increase reliability of the quality estimation.

The Global Quality Estimate consists of four individual terms: Cβ atoms only, all atoms, the solvation potential and the torsion angle potential. Here again, the lower values indicate that the models scores lower than the experimental structure (red) and higher values indicate, that the model scores higher than the experimental structure (blue).

SWISS-MODEL uses another method **[QMEAN](https://pubmed.ncbi.nlm.nih.gov/21134891/){:target="_blank"}** to estimate the quality of freshly built models. QMEAN quantifies model accuracy as well as modelling errors per residues and globally - for the entire model. This is done using statistical potentials of mean force.


The QMEAN Z-score or the normalized QMEAN score shows the "degree of nativeness", which indicates how the model is comparable to an experimental structure of similar size. QMEAN Z-score around 0 indicates good agreement, while score below -4.0 are given to models of low quality. This is also turned into the "thumbs-up" or "thumbs-down" symbol next to the QMEAN value.


QMEAN score per residue is shown in the *Local Quality Estimate* plot. The **[QMEANDisCo](https://doi.org/10.1093/bioinformatics/btz828){:target="_blank"}** method is used in this step. QMEANDisCo compares interatomic distances in the model with ensemble information extracted from experimentally determined protein structures of target sequence homologues.  The score shows similarity of the residues to the experimental structure and if it drops below 0.6, modelled residues are in general of low quality.
Different chains are showed in different colours and the residue modelling-quality can be viewed in 3D by selecting QMEAN as the coloring method in the NGL viewer.

The comparison plot shows the QMEAN score of our model (red star) within all QMEAN scores of experimentally determined structures compared to their size (number of residues). Here the Z-score is equivalent to the standard deviation of the mean.

One can superimpose selected models by clicking on their 3D structure image and they appear in the NGL viewer. Very handy is the sequence coverage comparison which appears under the 3D structure view. Here the target sequence is in green, while the model sequences in blue.

<a class="prompt prompt-question">
Which models show the highest quality? It is worth to consider the sequence coverage too. Is the local quality estimate to specific residue properties, e.g. secondary structure of b-factor value?
</a>


For more detailed structure information, one can click on the `Structure Assessment` button. This feature can be used also as a separate interface [https://swissmodel.expasy.org/assess](https://swissmodel.expasy.org/assess){:target="_blank"} where one can upload their PDB structure and this will be assessed.

<a class="prompt prompt-info">
Investigate a selected model and its structure properties. What is the ratio of Ramachandran favoured residues?
</a>

A Ramachandran plot is a way to visualize backbone dihedral angles of amino acid residues in the model against energetically favored regions of dihedrals of amino acids in general. These favored regions were obtained from more than 12000 experimental structures from [PISCES](https://pubmed.ncbi.nlm.nih.gov/12912846/){:target="_blank"}. Moreover the model is validated by [Molprobity](https://molprobity.biochem.duke.edu){:target="_blank"} both locally and globally. The quality of the structure is then expressed in Molprobity score, which should be as low as possible and *Ramachandran Favoured* residues, ideally above 98%. Clash score, outliers and bad angles and bonds should be as well as low as possible. More about structure assessment can be found in its [documentation](https://swissmodel.expasy.org/assess/help){:target="_blank"}. Examples of Ramachadran plots for all residues below:

<img src="/education/molmod_online/ramachandran.png">

SWISS-MODEL offers a comprehensive overview of selected models, which can be open in a separate window.

 <a class="prompt prompt-info">
Select models that you wish to compare by checking the *Compare* box under **Structure Assessment** and compare them in a new window.
</a>


On this page we see the list of models, the *Consistency with Ensemble* plot, the *Ensemble Variance* plot and superposed 3D structures of the models. In this case the ensemble represents the ensemble of selected models, thus consistency doesn't indicate  local quality of the model, but how consistent the residue quality is within the ensemble of models. Red color in both the *Ensemble variance* plot and in the 3D overlay shows higher differences of this region between models. If one aims to see the local quality of the model calculated with QMEAN, choose the QMEAN coloring method as in the example below:

<img src="/education/molmod_online/model_comparison.png">


Notice how the selected residues are highlighted simultaneously in all plots, i.e. if you point at the *Consistency with Ensemble* plot, you will see where the given residue is in the sequence as well as in the 3D structure. The lower the consistency value, the more flexible the region is. This can be a good tool to quickly evaluate which model is the most stable one and which regions to take into account for further modelling. The default coloring scheme in the molecular viewer is consistency, or local deviations of a protein from the 'consensus' extracted from other selected models.

The *Ensemble variance* assesses the consistency of interatomic distances in the full ensemble. Only distances up to $$15Å$$ are considered to reduce the effect of domain movement events.

Note that all figures can be downloaded by clicking on the `Download` icon. More information about the comparison page can be found on [https://swissmodel.expasy.org/comparison/help](https://swissmodel.expasy.org/comparison/help){:target="_blank"}.



<a class="prompt prompt-question">
Which model would be the most fitting to choose for further docking studies? Is it worth to build a model involving the first ~20 amino acids considering local quality of this terminus?
</a>

When performing docking, we want to make sure that we work with all relevant parts of the protein, i.e. part necessary for interactions. In some cases unstructured termini that are not vital for the complex formation can quite on the contrary, hinder the protein contact.


<a class="prompt prompt-info">
Select the model that is in your opinion of highest quality, download it in the PDB Format and save it for docking later.
</a>

Except for downloading the model in the PDB Format one can download a report that summarizes results for all models, suggest relevant publications and lists all possible templates. This is very useful to keep, however plain copy-pasting to your end report is strongly discouraged. Rather inspect all obtained results and select the relevant information and figures.

<hr>
## Congratulations!
You started with a sequence of a protein and went all the way from finding possible templates, to
evaluating which to use, to building several models, assessing their quality, and finally selecting
one representative. This model can now be used to offer insights on the binding of MDM2 to p53, or
on the structure of the mouse MDM2 protein, or to seed new computational analysis such as docking.

You might want to continue with the  tutorial on
[molecular dynamics simulations](/education/molmod_online/simulation)!
