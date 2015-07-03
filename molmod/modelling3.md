---
layout: page
title: "Homology Modelling of the mouse MDM2 protein"
excerpt: "Homology Modelling module of the Molecular Modelling course"
tags: [sample post, images, test]
image:
  feature: pages/banner_education-thin.jpg
---

### Searching for a suitable template in the RCSB PDB database
The template is the name given to the structure that will be used to model your sequence. In some
course materials and web servers, your sequence is also referred to as 'query'. Our goal is to search
through a structure database, such as [RCSB PDB](http://www.rcsb.org), for structures whose sequence
is similar to ours. 

Before diving in the details, create a directory where we will keep all our data regarding the 
homology modelling of MDM2. To keep it easily accessible, create it directly under your $HOME 
directory.

<a class="prompt prompt-cmd">
	cd $HOME  
	mkdir homology_modelling  
	cd homology_modelling
</a> 

There are many algorithms available to search for sequence homologues. Given the rather small size
of structure databases (~100k sequences) these searches run in a few seconds or minutes, depending 
on the size of your query. [BLAST](http://blast.ncbi.nlm.nih.gov/Blast.cgi) was an early pioneer 
that remains in use even today, more than 20 years after its development. In short, it works by 
finding fragments of the query that are similar to fragments of sequences in the database, and then 
merging them into full alignments ([source](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3820096/)). 
Another class of similarity search algorithms uses the query sequence to seed a general 'profile'
sequence that summarises significant features in those sequences, such as the most conserved amino 
acids. This 'profile' is then used to search again the database for more homologues. This approach
is used in PSI-BLAST and also in [HMMER](hmmer.janelia.org), which is based, however, on an entirely
different mathematical framework and implementation ([source](http://www.nature.com/nbt/journal/v22/n10/abs/nbt1004-1315.html)).

<a class="prompt prompt-question">
	Can you think of an advantage of searching sequence databases with a 'profile' sequence?
</a>

Whichever search method you use, it will return you a (hopefully) long list of results. Each entry
on this list will refer to a particular sequence - also called a hit - that was deemed similar to 
your query and it will contain not only the sequence alignment itself but also some quantitative 
statistics, namely the sequence similarity, the bit score of the hit, and its E-value.

Sequence similarity is a quantitative measure of how evolutionarily related two sequences are. It is
essentially a comparison of every amino acid to its aligned equivalent. There are three possible 
outcomes out of this comparison: the amino acids are exactly the same - identical; the 
amino acids are different but share common physico-chemical characteristics - similar; they are 
different. It is also possible that the alignment algorithm introduced 'gaps' in either of the 
sequences, meaning that there was possibly an insertion or deletion event during evolution. While
identity is straightforward, similarity depends on specific criteria that group amino acids together,
e.g. D/E, K/R/H, F/Y/W, etc. The bit score is the likelihood that the query sequence is *truly* a 
homologue of the hit, as opposed a mere random match. The E-value represents the number of sequences
that are expected to have a bit score higher than that of this particular alignment just by chance, 
given the database size. In essence, a very high bit score and a very small E-value assures you that
the alignment is indeed significant and that you can therefore trust this hit to be a true homologue
of your query sequence. 

Let's put this into practice. Start by performing a search with HMMER on the RCSB database. Assuming
you saved your sequence file from Uniprot in Downloads/, copy it to the newly created folder and 
launch a phmmer search against the RCSB PDB sequence database.

<a class="prompt prompt-info">
	Run phmmer with your MDM2 sequence against the RCSB database to find possible templates.
</a> 
<a class="prompt prompt-cmd">
	cp $HOME/Downloads/MDM2_MOUSE.fasta .  
	phmmer -A msa.sto -o phmmer.out MDM2_MOUSE.fasta /opt/databases/pdb_seqres.txt
</a> 
<a class="prompt prompt-attention">
  Adapt the file names accordingly.
</a> 

Depending on which MDM2 sequence you took, you might get different alignments. Let's assume we took
the 1-100 region, as the Uniprot webpage indicated it to be the necessary minimum to bind p53. phmmer
produced two output files: ```msa.sto``` and ```phmmer.out```. The first contains the 
aligned sequences in Stockholm format, while the second contains all the information regarding the
alignments - the statistics - and about the HMMER run itself. Let's have a look at ```phmmer.out```.

<a class="prompt prompt-info">
	Open and inspect the phmmer output file.
</a>
<a class="prompt prompt-cmd">
	leafpad phmmer.out &
</a>

{% highlight bash %}
# phmmer :: search a protein sequence against a protein database
# HMMER 3.1b2 (February 2015); http://hmmer.org/
# Copyright (C) 2015 Howard Hughes Medical Institute.
# Freely distributed under the GNU General Public License (GPLv3).
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# query sequence file:             MDM2_MOUSE.fasta
# target sequence database:        /opt/databases/pdb_seqres.txt
# output directed to file:         phmmer.out
# MSA of hits saved to file:       msa.sto
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Query:       sp|P23804|1-110  [L=110]
Scores for complete sequences (score includes all domains):
   --- full sequence ---   --- best 1 domain ---    -#dom-
    E-value  score  bias    E-value  score  bias    exp  N  Sequence Description
    ------- ------ -----    ------- ------ -----   ---- --  -------- -----------
      1e-64  218.8   0.1    1.2e-64  218.6   0.1    1.0  1  1z1m_A    mol:protein length:119  Ubiquitin-protein ligase E3
    1.2e-64  218.5   0.1    1.4e-64  218.3   0.1    1.0  1  2lzg_A    mol:protein length:125  E3 ubiquitin-protein ligase
    2.2e-62  211.3   0.1    2.4e-62  211.2   0.1    1.0  1  2mps_A    mol:protein length:107  E3 ubiquitin-protein ligase
    1.8e-60  205.2   0.1      2e-60  205.0   0.1    1.0  1  4ode_A    mol:protein length:105  E3 ubiquitin-protein ligase
    1.8e-60  205.2   0.1      2e-60  205.0   0.1    1.0  1  4odf_A    mol:protein length:105  E3 ubiquitin-protein ligase

....
  ------ inclusion threshold ------
        3.1   11.9   0.0        3.3   11.8   0.0    1.2  1  1uhr_A    mol:protein length:93  SWI/SNF related, matrix asso


Domain annotation for each sequence (and alignments):
>> 1z1m_A  mol:protein length:119  Ubiquitin-protein ligase E3 Mdm2
   #    score  bias  c-Evalue  i-Evalue hmmfrom  hmm to    alifrom  ali to    envfrom  env to     acc
 ---   ------ ----- --------- --------- ------- -------    ------- -------    ------- -------    ----
   1 !  218.6   0.1   5.8e-68   1.2e-64       1     110 []       1     110 [.       1     110 [. 0.99

  Alignments for each domain:
  == domain 1  score: 218.6 bits;  conditional E-value: 5.8e-68
  sp|P23804|1-110   1 mcntnmsvstegaastsqipaseqetlvrpkplllkllksvgaqndtytmkeiifyigqyimtkrlydekqqhivycsndllgdvfgvpsfsvk 94 
                      mcntnmsv t+ga +tsqipaseqetlvrpkplllkllksvgaq dtytmke++fy+gqyimtkrlydekqqhivycsndllgd+fgvpsfsvk
           1z1m_A   1 MCNTNMSVPTDGAVTTSQIPASEQETLVRPKPLLLKLLKSVGAQKDTYTMKEVLFYLGQYIMTKRLYDEKQQHIVYCSNDLLGDLFGVPSFSVK 94 
                      8********************************************************************************************* PP

  sp|P23804|1-110  95 ehrkiyamiyrnlvav 110
                      ehrkiy miyrnlv v
           1z1m_A  95 EHRKIYTMIYRNLVVV 110
                      *************976 PP
....

Internal pipeline statistics summary:
-------------------------------------
Query model(s):                              1  (110 nodes)
Target sequences:                       323515  (78693430 residues searched)
Passed MSV filter:                      4547  (0.014055); expected 6470.3 (0.02)
Passed bias filter:                     4327  (0.013375); expected 6470.3 (0.02)
Passed Vit filter:                       250  (0.000772762); expected 323.5 (0.001)
Passed Fwd filter:                       162  (0.00050075); expected 3.2 (1e-05)
Initial search space (Z):             323515  [actual number of targets]
Domain search space  (domZ):             162  [number of targets reported over threshold]
# CPU time: 0.92u 1.21s 00:00:02.12 Elapsed: 00:00:02.18
# Mc/sec: 3952.64
//
# Alignment of 161 hits satisfying inclusion thresholds saved to: msa.sto
[ok]
{% endhighlight %}

This file contains pretty much all the information necessary to make an informed choice about which
hit, if any, we should take as a template. The header of the file specifies which were your input
options, as well as the version of HMMER you ran. Afterwards, there is a ranked list of all the hits
with the statistics, the PDB ID code and chain, and the description of the hit. For more information
on the HMMER output, refer to the [freely available manual](http://hmmer.janelia.org/documentation.html).

<a class="prompt prompt-question">
	How many sequences are there in the RCSB PDB database? How many of these were selected to match
	our MDM2 mouse sequence?
</a>

After this listing, there is another section that goes in more detail on the alignments. For each
hit, the file repeats the statistics - scores, e-values, but now also the boundaries of the 
alignment - and shows the explicit alignment between the query and the hit. Unlike BLAST or the 
HMMER web server, running HMMER locally will not give you the sequence identity or similarity 
values. It shows, though, in between the query and hit sequences, a line that contains the amino 
acid one-letter-code, a '+' symbol, or an empty space, depending if there is an identical, similar,
or no match at that position. Further, the line below the sequence shows you the posterior 
probabilities of each residue, a measure of the alignment confidence, ranging from 0 to * in 
increasing order. This last piece of information can be used to readily gauge which regions of the 
sequence are particularly 'floppy' in the alignment.

To help you make a decision, we included in the Virtual Image an utility script to calculate the
sequence identity and percentage of gaps in each hit of the alignment. 

<a class="prompt prompt-info">
  Use the utility script *calc_aln_ids.py* to get sequence identity values for 
	each hit in the alignment.
</a>
<a class="prompt prompt-cmd">
  python /opt/courses/homology/calc_aln_ids.py -s MDM2_MOUSE.fasta -a msa.sto -o msa.stats
</a>

The resulting file has four columns: the rank of the hit, the hit identifier, the sequence identity,
and the percentage of gaps in the hit sequence. 

{% highlight bash %}
# Alignment length = 110
#       Hit Id                  Seq Id (%)      Gaps (%)
1       1z1m_A/1-110            0.90            0.00
2       2lzg_A/1-110            0.90            0.00
3       2mps_A/1-106            0.87            0.04
4       4ode_A/1-105            0.85            0.05

....

156     2z5s_O/20-105           0.39            0.22
157     3dac_A/21-106           0.39            0.22
158     3dac_M/21-106           0.39            0.22
159     2z5t_M/20-105           0.39            0.22
160     2z5t_N/20-105           0.39            0.22
161     2z5t_O/20-105           0.39            0.22
{% endhighlight %}

In our case, it seems we were pretty lucky! There are at least 2 hits sharing 90% sequence identity
with our query, while the 'worst' hit has 39% and a 22% of gaps. Interestingly, it seems that the
overwhelming majority of the hits belong to the E3 ubiquitin-ligase family, and the lower ranking hits
all belong to the MDM4 protein, a relative of our MDM2. There is a consistent pattern, which is good!

Now, these results beg the question: how low can we go in terms of sequence identity (or similarity)
to the template and still trust our model? Fortunately for us, protein structures are quite robust.
If you mutate a third of the sequence, chances are that the fold will be maintained quite 
faithfully. Even if you mutate 60% of your sequence (identity ~40%), homology modelling is still
considered 'easy'. Of course, your mileage may vary depending on the case at hand.

<figure>
    <a href="/images/molmod/rcsb-statistics.png"><img src="/images/molmod/similarity-structures.png"></a>
    <figcaption>Structures of sequence homologues of the Ribosomal protein L5 (in red).</figcaption>
</figure>

As a rule of thumb, any sequence above 30-35% sequence similarity can be used to build a somewhat
reliable model ([source](http://peds.oxfordjournals.org/content/12/2/85.long)). Below these values, 
you enter what is called the twilight zone, and when you reach below 20%, you are in the danger zone.
All these percentages are of course relative to the sequence size. Further, if you have a 100 residue
protein with 90% sequence identity to a template but those 10% are all clumped together in the middle
of an alpha-helix, you probably should be extremely careful. Again: you mileage may vary depending on
the case at hand. The best piece of advice is to trust your knowledge of biology, not the numbers the
algorithms give you. Also, modelling a SH2 domain from another SH2 domain at 30% identity is different
than modelling it from luciferase at 50% identity. Biological function takes obvious precedent over
any number you might find. If you want a perfect example of how not to blindly trust sequence identity
have a look at this [publication](http://www.pnas.org/content/104/29/11963.full). 

When you are ready to proceed, [click here]({{site.url}}/molmod/modelling4.html).