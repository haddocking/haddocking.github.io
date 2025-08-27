#!/usr/bin/env python

"""
AIRviewer.py

Version	   : 2.0
Description: Interactive pymol plugin for the visiualisation, editing and 
 			 generation of HADDOCK Ambiguous Interaction Restraints.
Options	   : Once loaded their will be a button list at the right hand side
 			 of the pymol window. 
			 * The 'file' button allows you to choose a CNS style ".tbl" file 
			   from the directory where you launched pymol.
			 * The 'Load AIR file' button parses the selected file and colors
			   the residues as either active (red) or passive (green). If an
			   atom specific restraint is defined only those atoms will be 
			   displayed as either active or passive.
			 * The 'Show AIR net' button draws lines between the active and or
			   passive restraints to visiualize the connectivity. The lines are
			   grouped as objects according to the segid of the active residue 
			   they originated from. By deafult the full AIR net is shown but
			   if a selection is made only the AIR net for that given selection
			   is shown.
			 * The 'Set selection as active' button allows you to define the 
			   current selection as 'active. The selection can be on a residue 
			   or atom bases. The list of Ambiquous Interaction Restraints is
			   emediatly updated to clicking "Show AIR net" will display your
			   changes. 
			 * The 'Set selection as passive' button allows you to define the 
			   current selection as 'passive'. The selection can be on a residue 
			   or atom bases. The list of Ambiquous Interaction Restraints is
			   emediatly updated to clicking "Show AIR net" will display your
			   changes.
			 * The 'Deactivate selection' button removes the current selection
			   from the list of Ambiguous Interaction Restraints. The removal
			   works on a residue level. 
			 * With the 'Write AIR restraint file' button you can save your
			   Ambiguous Interaction Restraint network to file. The file
			   'ambig_pm.tbl' will be writen in the current directory. 
			   Backups are made if multiple files are saved.
			 * With 'Pairwise Select' button (toggle On/Off) you can switch 
			   between two modes of rstraint definition. When turned Off the 
			   restraints will be generated in the default way. This means that
			   all permutations between active and active/passive are made.
			   Depending on the complex under study (large interaction surface,
			   multiple domains e.d) the generated AIR network may contain to
			   much ambiguouty in the sense that their are restraints defined 
			   between parts of the complex of which you know they are not
			   possible. When you toggle the 'Pairwise Select' button On you
			   are able to define restraints based on two selections. Their
			   will only be AIR restraints defined between the residues in the
			   selection.
			 * The 'Quick atom select' menu allows you to quickly define certain
			   atom selections. So far they contain atom selections for the 
			   nucleic acid bases and nucleic acid sugar-phosphate backbone. 
Usage	   : Launch from within Pymol by typing "run AIRviewer" in the
			 pymol terminal. The program needs to be in the same directory as 
			 where you launched pymol or you append it to the pymol PYTHONPATH.
Disclamer  : Although the software is tested it can still contain bugs so please 
 			 verify the calculated results. If you run into bugs or would like to see
			 some additional options added to the program please contact me:
			 mvdijk@nmr.chem.uu.nl	

Created by Marc van Dijk on 29-03-2009.
Copyright (c) 2008-2009 Marc van Dijk. All rights reserved.

Updated to run on Python 3.9 by Anna Kravchenko 15-03-2025.
"""

from pymol import cmd, stored
from pymol.wizard import Wizard
import os
import sys
import re
import copy
import glob

MULTIPLE_OBJECTS = True

def ConstructSelector(dictionary):
	
	"""Construct a PyMol selector string from the segid, resid and atom definitions
	   in the supplied dictionary
	"""
	selection = []
	
	for chain in dictionary:
		for res in dictionary[chain]:
			if len(res) == 2: selstring = "(%s)" % " and ".join(res)
			else: selstring = "(%s and (%s))" % (" and ".join(res[0:2]),res[2])
			selection.append(selstring)	
	
	return selection		

class Restraints_wiz(Wizard):

	"""Initiates the AIR Restraint Inspection buttonlist in the right side menubar of pymol. Controls
	   all addition, modification and removal of AIR restraints. The menu allows for loadig existing 
	   CNS AIR restraint files and writting created or modified AIR restraints to file. 
	"""
	def __init__(self,_self=cmd):
		
		"""Initialize the wizard, set the initial display of the structure and initialize the 
		   AirRestraints class	
		"""
		Wizard.__init__(self)
		
		cmd.hide('all')
		cmd.show('cartoon','all')
		cmd.set('cartoon_nucleic_acid_mode','2')
		cmd.set('cartoon_tube_radius','0.3')
		cmd.set('cartoon_ring_mode','3')
		cmd.color('yellow','all')
		
		self.segments = self.getSegids()
		if not len(self.segments): print("--> PDB does not contain any segment identifier. This is required")
		
		self.atomselectors = ['Off','NA-sugar','NA-base','NA-minor','NA-major']
		self.atomselector = 'Off'
		
		self.pairSelect = {1:{},2:{}}
		self.pairwiseSelector = (['Off','To residue'] + [("To %s" % n) for n in self.segments])
		self.pairwiseSelect = 'Off'
		
		self.airNetObjects = []
		
		self.airstore = AirRestraints(segids=self.segments)
		self.initrestraints()

	def getSegids(self):
		
		"""Retrieve all segments from the loaded complex and return as list. If there are no segids defined
		   then query for chain id. If these are set then set the segid according to chain. If no chain Id
		   and no segid than raise and error
		"""
		
		stored.segids = []
		cmd.iterate('all','stored.segids.append(segi)')
		
		unique = []
		for n in stored.segids:
			if not n in unique and len(n): unique.append(n)
		
		if not unique:
			stored.chainids = []
			cmd.iterate('all','stored.chainids.append(chain)')
			for n in stored.chainids:	
				if not n in unique and len(n): unique.append(n)
			
			for chain in unique:
				cmd.alter('chain %s' % chain, 'segi = "%s"' % chain)
		
		if not unique:
			print("ERROR: no chain ID and no segid ID defined. Need one of these")	
		else:
			return unique	

	def initrestraints(self):
		
		"""Search for all .tbl files in the current directory. If not file found than display a 
		   warning message on the terminal and in the 'File' dropdown menu.
		"""
		self.restfiles = glob.glob('*.tbl')
		if not len(self.restfiles): 
			self.restfiles = ['No .tbl found']
			print("--> No .tbl restraint files found in current directory")
			
		self.rest_file = self.restfiles[0]
		self.rest_files = range(1,len(self.restfiles)+1)
		
		cmd.refresh_wizard()

	def get_panel(self):
		
		"""Construct the AIR restraint inspection buttonlist and the restraint file, Quick atom select and 
		   Pairwise Select dropdown menu
		"""
		self.menu['rest_file'] = [[1,self.restfiles[v-1],'cmd.get_wizard().set_rest_file(%i)' % v] for v in self.rest_files]
		self.menu['atomselector'] = [[1,self.atomselectors[v-1],'cmd.get_wizard().set_atomselector(%i)' % v] for v in range(1,len(self.atomselectors)+1)]
		self.menu['pairwiseSelect'] = [[1,self.pairwiseSelector[v-1],'cmd.get_wizard().set_pairwiseSelector(%i)' % v] for v in range(1,len(self.pairwiseSelector)+1)]
		
		return [
		[ 1, 'AIR restraint constructor', '' ],
		[ 3, 'File (%s)' % self.rest_file,'rest_file'],
		[ 2, 'Load AIR file', 'cmd.get_wizard().loadRestraint()' ],
		[ 2, 'Show AIR net', 'cmd.get_wizard().showDistance()'],
		[ 2, 'Set selection as active', 'cmd.get_wizard().setActive()' ],
		[ 2, 'Set selection as passive', 'cmd.get_wizard().setPassive()' ],
		[ 2, 'Deactivate selection', 'cmd.get_wizard().setToNone()'],
		[ 2, 'Write AIR restraint file', 'cmd.get_wizard().writeRestraints()'],
		[ 3, 'Pairwise Select: %s' % self.pairwiseSelect, 'pairwiseSelect'],
		[ 3, 'Quick atom select: %s' % self.atomselector, 'atomselector'],
		]

	def checkPairwiseResidueSelection(self):
		
		"""Check the pairwise residue selections to filter out mistakes made by the user. True is returned if no
		   problems were encountered and False if wrong defenition was encountered. A wrong defenition is two passive 
		   restraint sets or intramolecular restraints.
		"""	
		if self.pairSelect[1]['type'] == 'passive' and self.pairSelect[2]['type'] == 'passive': 
			print("--> No pairwise residue selection between two passive residues allowed")
			return False
		
		for one in self.pairSelect[1]['selection']:
			for two in self.pairSelect[2]['selection']:
				if one[0] == two[0]: 
					print ("--> No intra-molecular restraints allowed")
					return False
				
		return True		
	
	def checkPairwiseSegidSelection(self,selection=None,segid=None):
		
		"""Check the pairwise selection directed to a complete segment. Check for intramolecular restraints"""
		
		for n in selection:
			if n[0] == segid:
				print ("--> No intra-molecular restraints allowed")
				return False
			
		return True
		
	def setActive(self):
		
		"""Gathers the segments, residues and atoms from the selection and sets them as 'active'. This involves
		   appending them to the 'activedict', adding them to the 'airdict' and updating the view. For adding to the
		   'activedict' the defenition checks if the segid is in the dict (if not add it) and if the residue is 
		   allready defined (if not add it). For the 'airdict' the same checks are made but the residue is also
		   added to all active residues of the other segments. In case a conversion from active to passive is 
		   attempted the selection is also removed from the 'passive' and the 'air' dictionary before being re-added
		   as active.
		"""
		atom_selection = cmd.get_names("selections")
		if 'sele' in atom_selection:	
			if self.pairwiseSelect == 'To residue':
				if not len(self.pairSelect[1]):
					self.pairSelect[1]['selection'] = self.airstore.resolveSelection(quickselect=self.atomselector)
					self.pairSelect[1]['type'] = 'active'
					self.airstore.addToActive(self.pairSelect[1]['selection'])
					self.displayRestraints() 
					print("--> Pairwise residue store 1 filled with %i active residues" % len(self.pairSelect[1]['selection']))
				elif not len(self.pairSelect[2]):
					self.pairSelect[2]['selection'] = self.airstore.resolveSelection(quickselect=self.atomselector)
					self.pairSelect[2]['type'] = 'active'
					self.airstore.addToActive(self.pairSelect[2]['selection'])
					self.displayRestraints() 
					print("--> Pairwise residue store 2 filled with %i active residues" % len(self.pairSelect[2]['selection']))
					print("--> Set pairwise residue selection")
					if self.checkPairwiseResidueSelection(): self.airstore.setPairwiseResidueAir(self.pairSelect)
					else:
						for n in self.pairSelect:
							if self.pairSelect[n]['type'] == 'passive': self.airstore.removeFromPassive(self.pairSelect[n]['selection'])
							else: self.airstore.removeFromActive(self.pairSelect[n]['selection'])
						parent = cmd.get_names('objects')[0]
						cmd.color('yellow',parent)
						self.displayRestraints()
					self.pairSelect[1].clear(); self.pairSelect[2].clear()		 	
				else:
					pass
			elif not self.pairwiseSelect == 'Off':
				ActiveSelection = self.airstore.resolveSelection(quickselect=self.atomselector)
				segid = 'segid %s' % self.pairwiseSelect.split()[1]
				if self.checkPairwiseSegidSelection(selection=ActiveSelection,segid=segid):
					self.airstore.removeFromPassive(ActiveSelection)
					self.airstore.addToActive(ActiveSelection)
					self.airstore.setActiveAir(ActiveSelection,segid=segid)
					self.displayRestraints()
			else:
				ActiveSelection = self.airstore.resolveSelection(quickselect=self.atomselector)
				self.airstore.removeFromPassive(ActiveSelection)
				self.airstore.unsetAir(ActiveSelection)
				self.airstore.addToActive(ActiveSelection)
				self.airstore.setActiveAir(ActiveSelection)
			
				print("--> The following selection of residues is set as 'active':")
				for n in ActiveSelection: print("    %s" % " ".join(n))
					
				self.displayRestraints()
		else: print("--> No 'sele' selection found. Nothing to set")
		
	def setPassive(self):
		
		"""Gathers the segments, residues and atoms from the selection and sets them as 'passive'. This involves
		   appending them to the 'passivedict', adding them to the 'airdict' and updating the view. For adding to the
		   'passivedict' the defenition checks if the segid is in the dict (if not add it) and if the residue is 
		   allready defined (if not add it). For the 'airdict' the same checks are made but the residue is also
		   added to all active residues of the other segments. In case a conversion from passive to active is 
		   atempted the selection is also removed from the 'active' and the 'air' dictionary before being re-added
		   as passive. 
		"""
		atom_selection = cmd.get_names("selections")
		if 'sele' in atom_selection:
			if self.pairwiseSelect == 'To residue':
				if not len(self.pairSelect[1]):
					self.pairSelect[1]['selection'] = self.airstore.resolveSelection(quickselect=self.atomselector)
					self.pairSelect[1]['type'] = 'passive'
					self.airstore.addToPassive(self.pairSelect[1]['selection'])
					self.displayRestraints() 
					print("--> Pairwise residue store 1 filled with %i passive residues" % len(self.pairSelect[1]))
				elif not len(self.pairSelect[2]):
					self.pairSelect[2]['selection'] = self.airstore.resolveSelection(quickselect=self.atomselector)
					self.pairSelect[2]['type'] = 'passive'
					self.airstore.addToPassive(self.pairSelect[2]['selection'])
					self.displayRestraints() 
					print("--> Pairwise residue store 2 filled with %i passive residues" % len(self.pairSelect[2]))
					print("--> Set pairwise residue selection")
					if self.checkPairwiseResidueSelection(): self.airstore.setPairwiseResidueAir(self.pairSelect)
					else:
						for n in self.pairSelect:
							if self.pairSelect[n]['type'] == 'passive': self.airstore.removeFromPassive(self.pairSelect[n]['selection'])
							else: self.airstore.removeFromActive(self.pairSelect[n]['selection'])
						parent = cmd.get_names('objects')[0]
						cmd.color('yellow',parent)
						self.displayRestraints()
					self.pairSelect[1].clear(); self.pairSelect[2].clear()		
				else:
					pass
			elif not self.pairwiseSelect == 'Off':
				PassiveSelection = self.airstore.resolveSelection(quickselect=self.atomselector)
				segid = 'segid %s' % self.pairwiseSelect.split()[1]
				if self.checkPairwiseSegidSelection(selection=PassiveSelection,segid=segid):
					self.airstore.removeFromActive(PassiveSelection)
					self.airstore.unsetAir(PassiveSelection)
					self.airstore.addToPassive(PassiveSelection)
					self.airstore.setPassiveAir(PassiveSelection,segid=segid)
					self.displayRestraints()	
			else:		
				PassiveSelection = self.airstore.resolveSelection(quickselect=self.atomselector)
				self.airstore.removeFromActive(PassiveSelection)
				self.airstore.unsetAir(PassiveSelection)
				self.airstore.addToPassive(PassiveSelection)
				self.airstore.setPassiveAir(PassiveSelection)
			
				print("--> The following selection of residues is set as 'passive':")
				for n in PassiveSelection: print("    %s" % " ".join(n))
		
				self.displayRestraints()		
		else: print("--> No 'sele' selection found. Nothing to set")	
			
	def setToNone(self):
		
		"""Remove the selected residues from the 'active', 'passive' and 'air' dictionaries. It does a full remove of every 
		   entry in the above dictionaries that match segment and residue
		"""
		DeactivateSelection = []
		
		atom_selection = cmd.get_names("selections")
		if 'sele' in atom_selection:
			DeactivateSelection = self.airstore.resolveSelection()
			self.airstore.removeFromActive(DeactivateSelection,resremove=True)
			self.airstore.removeFromPassive(DeactivateSelection,resremove=True)
			self.airstore.unsetAir(DeactivateSelection,resremove=True)
			
			print("--> The following selection of residues are deactivated:")
			for n in DeactivateSelection: print("    %s" % " ".join(n))
		
			parent = cmd.get_names('objects')[0]
			cmd.color('yellow',parent)			
			
			self.displayRestraints()
		else: print("--> No 'sele' selection found. Nothing to set")
		
	def loadRestraint(self):
		
		"""Parse the selected restraintfile, display warning if no restraint file is present. Upon loading of another restraint 
		   file in the same pymol session all selections and objects (if MULTIPLE_OBJECTS = False) are removed and the airstore 
		   dictionary is re-initialized. 	
		"""
		
		if self.rest_file == 'No .tbl found': print("--> No .tbl file found. Nothing to load")
		else:
			for selection in cmd.get_names("selections"): cmd.delete(selection)
			objects = cmd.get_names("objects")
			if not MULTIPLE_OBJECTS:
				for obj in objects[1:len(objects)]: cmd.delete(obj)
			
			print("--> Load restraint file: %s" % self.rest_file)
			self.airstore.cleanup()
			self.airstore.readAirFile(self.rest_file)
			self.displayRestraints()
	
	def writeRestraints(self):
		
		"""Write the AIR restraints to a CNS restraint file. Previous generated restraintfiles are backed-up"""
		
		if os.path.isfile('ambig_pm.tbl'):
				i = 1; backup = False
				while backup == False:
					if os.path.isfile('ambig_pm%i.tbl' % i):
						i = i+1
					else:
						os.rename('ambig_pm.tbl', 'ambig_pm%i.tbl' % i)
						backup = True
		
		print("--> Write restraint file: ambig_pm.tbl")
		self.airstore.writeRestraints('ambig_pm.tbl')	
		self.initrestraints()	

	def showDistance(self):
		
		"""Show the way that an active residue is connected to a series of active or passive residues by calculating the distance 
		   between the CA or C1 atom of the given pair and display a dotted line between them (labels off). If the user has selected 
		   residue(s) than only the AIR net for the given selection is displayed.Group source active residues by segment and give 
		   the dotted lines a different color according to the segment. The group objects are stored in 'self.airNetObjects' and 
		   the objects are deleted in th view every time the 'Show AIR net' button is pressed.
		"""
		colors = ['red','orange','blue','cyan','magenta','yellow']; count = 0
		
		for obj in self.airNetObjects: cmd.delete(obj)
		self.airNetObjects = []
	
		if 'sele' in cmd.get_names("selections"):
			airNetSelection = self.airstore.resolveSelection()
			for chain in self.airstore.airdict:
				if len(self.airstore.airdict[chain]):
					chainID = (chain.split())[1]; actsel = False
					for res1 in self.airstore.airdict[chain]:
						if (res1[0],res1[1]) in airNetSelection:
							actsel = True
							for res2 in self.airstore.airdict[chain][res1]:
								r1 = "%s and %s and (name CA or name C1')" % (res1[0],res1[1])
								r2 = "%s and %s and (name CA or name C1')" % (res2[0],res2[1])
								cmd.distance("Partner-%s" % chainID,r1,r2)
						else:
							for res2 in self.airstore.airdict[chain][res1]:
								if (res2[0],res2[1]) in airNetSelection:
									actsel = True
									r1 = "%s and %s and (name CA or name C1')" % (res1[0],res1[1])
									r2 = "%s and %s and (name CA or name C1')" % (res2[0],res2[1])
									cmd.distance("Partner-%s" % chainID,r1,r2)		
					if actsel:
						cmd.color(colors[count],"Partner-%s" % chainID)
						self.airNetObjects.append("Partner-%s" % chainID)
						count += 1	
			cmd.delete('sele')			
		else:
			for chain in self.airstore.airdict:
				if len(self.airstore.airdict[chain]):
					chainID = (chain.split())[1]
					for res1 in self.airstore.airdict[chain]:
						for res2 in self.airstore.airdict[chain][res1]:
							r1 = "%s and %s and (name CA or name C1')" % (res1[0],res1[1])
							r2 = "%s and %s and (name CA or name C1')" % (res2[0],res2[1])
							cmd.distance("Partner-%s" % chainID,r1,r2)
					cmd.color(colors[count],"Partner-%s" % chainID)
					self.airNetObjects.append("Partner-%s" % chainID)
					count += 1
			
		cmd.set('dash_gap', 0.05)
		cmd.hide('labels')
			
	def displayRestraints(self):

		"""Color the active and pasive residues on the structure. Deselect selection emmediatly
		   so that the users can continue work without having to deselct themself.	
		"""
		active = ConstructSelector(self.airstore.activedict)
		if len(active):
			for act in range(len(active)):
				if act == 0: cmd.select('Active',active[act])
				else: cmd.select('Active','Active or %s' % active[act])
			cmd.color("red",'Active')
		
		passive = ConstructSelector(self.airstore.passivedict)
		if len(passive):
			for pas in range(len(passive)):
				if pas == 0: cmd.select('Passive',passive[pas])
				else: cmd.select('Passive','Passive or %s' % passive[pas])
				cmd.color("green",'Passive')

		cmd.deselect()
		cmd.delete('sele')

	def set_atomselector(self,name):
		
		"""Set the quick atom selector"""
		
		self.atomselector = self.atomselectors[name-1]
		print("--> Quick atom selector set to: %s" % self.atomselector)	
		cmd.refresh_wizard()

	def set_rest_file(self,name):
		
		"""Set the active restraint file as label on the file selector button"""
		
		self.rest_file = self.restfiles[name-1]
		cmd.refresh_wizard()
		
	def set_pairwiseSelector(self,name):
		
		"""Set pairwise restraint generation"""

		self.pairwiseSelect = self.pairwiseSelector[name-1]
		print("--> Pairwise residue restraint selection: %s" % self.pairwiseSelect)
		cmd.refresh_wizard()

class AirRestraints(object):

	def __init__(self,segids=None):
		
		"""Initialize a empty AIR, Active and Passive dictionaries. Define quick atom selectors"""
		
		self.airdict = {}
		self.segids = segids
		
		for segid in self.segids:
			self.airdict['segid %s' % segid] = {}
		
		self.activedict = {}
		self.passivedict = {}
		
		self.currchain = None
		self.currresid = None
		self.currselect = []
	
		self.NAmajor = {'THY':'name H3 or name O4 or name C4 or name C5 or name C6 or name C7',
		   				'ADE':'name H61 or name H62 or name N1 or name N7 or name C5 or name C6 or name C8',
		   				'GUA':'name H1 or name H21 or name N7 or name O6 or name C5 or name C6 or name C8',
		   				'CYT':'name H41 or name H42 or name N3 or name C4 or name C5 or name C6'}
		
		self.NAminor = {'THY':'name H3 or name O2 or name C2',
		   				'ADE':'name N1 or name N3 or name C2 or name C4',
		   				'GUA':'name H1 or name H21 or name H22 or name N3 or name C2 or name C4',
		   				'CYT':'name N3 or name O2 or name C2'}
	
		self.NAbase = {'THY':'name H3 or name O2 or name O4 or name C2 or name C4 or name C5 or name C6 or name C7',
					   'ADE':'name H61 or name H62 or name N1 or name N3 or name N7 or name C2 or name C4 or name C5 or name C6 or name C8',
					   'CYT':'name H41 or name H42 or name N3 or name O2 or name C2 or name C4 or name C5 or name C6',
					   'GUA':'name H1 or name H21 or name H22 or name N3 or name N7 or name O6 or name C2 or name C4 or name C5 or name C6 or name C8'}
	
		self.NAsugar = "name C1' or name O4' or name C2' or name O3' or name O5' or name P or name O1P or name O2P"
	
	def __removeBlank(self,line):

		"""Strip whitespace from all string elements in the supplied list"""
		
		return [line[n].strip() for n in range(len(line)) if not len(line[n].strip()) == 0 ]
	
	def __formatAssignment(self,line):
		
		"""
		Extracts the segment, residue and possible atom specifiers from a line, sort them in the
		propper order and returns them as tuple.
		"""
		splitter2 = re.compile('and')
		
		newline = []
		for n in line: newline += self.__removeBlank(splitter2.split(n))
		
		sortline = []
		if len(newline) == 2: sortline.append(newline[1]); sortline.append(newline[0])
		else:sortline.append(newline[1]); sortline.append(newline[0]); sortline.append(newline[2])
		
		return tuple(sortline)	
	
	def __formatCutoff(self,line):
		
		"""Extract and format the air upper distance cutoff"""
		
		cutoff = None
		
		try: cutoff = [float(n) for n in line.split()]
		except: pass
		
		return cutoff		
	
	def __formatAtomString(self,atomlist):
		
		"""Format a list of atom names into a CNS style atom selector string"""
		
		if len(atomlist) == 1:
			atomstring = 'name %s' % atomlist[0]
			return atomstring
		elif len(atomlist) > 1:
			atomstring = 'name %s or name ' % atomlist[0]
			atomstring += " or name ".join(atomlist[1:len(atomlist)])
			return atomstring
		else: pass		
	
	def __resolveActivePassive(self):
		
		"""
		Takes the list of active and passive residues where the source active residue acts on from 
		the 'air' dictionary and copies the passive residues to the 'passive' dictionary.
		"""
		for chain in self.airdict:
			for resid in self.airdict[chain]:
				for n in self.airdict[chain][resid]:
					if n[0] not in self.passivedict: self.passivedict[n[0]] = []
					#if not self.passivedict.has_key(n[0]): self.passivedict[n[0]] = []
					if n[0] not in self.activedict and n not in self.passivedict: self.passivedict[n[0]].append(n)
					#if not self.activedict.has_key(n[0]) and not n in self.passivedict[n[0]]: self.passivedict[n[0]].append(n)
					elif not n in self.activedict[n[0]] and not n in self.passivedict[n[0]]: self.passivedict[n[0]].append(n)
	
	def removeFromActive(self,selection,resremove=False):

		"""Remove the given selection from the active residue dictionary"""

		if resremove == True:
			selection = [(n[0],n[1]) for n in selection]
			for chain in self.activedict:
				newlist = []
				for n in self.activedict[chain]: 
					if not (n[0],n[1]) in selection: newlist.append(n)
				self.activedict[chain] = copy.copy(newlist)	
		else:
			for n in selection:
				if n[0] in self.activedict:
					if n in self.activedict[n[0]]: self.activedict[n[0]].remove(n)
	
	def removeFromPassive(self,selection,resremove=False):
	
		"""Remove the given selection from the passive residue dictionary"""
		
		if resremove == True:
			selection = [(n[0],n[1]) for n in selection]
			for chain in self.passivedict:
				newlist = []
				for n in self.passivedict[chain]: 
					if not (n[0],n[1]) in selection: newlist.append(n)
				self.passivedict[chain] = copy.copy(newlist)	
		else:
			for n in selection:
				if n[0] in self.passivedict:
					if n in self.passivedict[n[0]]: self.passivedict[n[0]].remove(n)
			
	def addToPassive(self,selection):
		
		"""Add the given selection to the passive residue dictionary"""
		
		for n in selection:
			if n[0] not in self.passivedict: self.passivedict[n[0]] = []
			if not n in self.passivedict[n[0]]: self.passivedict[n[0]].append(n)

	def addToActive(self,selection):

		"""Add the given selection to the active residue dictionary"""

		for n in selection:
			if n[0] not in self.activedict: self.activedict[n[0]] = []
			if not n in self.activedict[n[0]]: self.activedict[n[0]].append(n)		
	
	def setPassiveAir(self,passivelist,segid=None):
		
		"""Change passive AIR defenitions in the AIR dictionary. Add the residue to all source active
		   residues of the other chains.
		"""
		if segid: segid = [segid]
		else: segid = self.airdict.keys()
		
		for s in segid:
			for resid in self.airdict[s]:
				for n in passivelist:
					if not resid[0] == n[0] and not n in self.airdict[s][resid]: 
						self.airdict[s][resid].append(n)
	
	def setActiveAir(self,activelist,segid=None):
		
		"""Change active AIR defenitions in the AIR dictionary. If the segid of the new active residue is not
		   yet in the 'air' dictionary than add it. Subsequently add all new active residues to the segment and
		   copy the active and passive residues of the other segments to the new source active residue.
		   For all other active residues not belonging to the same segid, check if they allready have the new
		   active residue and add if not.	
		"""

		sortedlist = {}
		for n in activelist:
			if n[0] in sortedlist: sortedlist[n[0]].append(n)
			else: 
				sortedlist[n[0]] = []
				sortedlist[n[0]].append(n)
				
		for chain in sortedlist:
			for resid in sortedlist[chain]:
				if not resid in self.airdict[chain]:
					self.airdict[chain][resid] = []
					if segid: chains = [segid]
					else: chains = self.activedict.keys()
					for active in chains:
						if not active == chain: self.airdict[chain][resid] += copy.copy(self.activedict[active])
					if segid: chains = [segid]
					else: chains = self.passivedict.keys()
					for passive in chains:
						if not passive == chain: self.airdict[chain][resid] += copy.copy(self.passivedict[passive])
		
		if segid: chains = [segid]
		else: chains = self.airdict.keys()
		for chain in sortedlist:
			for n in chains:
				for resid in self.airdict[n]:
					for sec in sortedlist[chain]:
						if not chain == n and not sec in self.airdict[n][resid]: self.airdict[n][resid].append(sec)  				
	
	def setPairwiseResidueAir(self,selection):
		
		"""Set a pairwise defined Amiguous Interaction Restraint. This means only set active and/or passive
		   restraints between the residues or atoms of two selections
		"""
		
		if selection[1]['type'] == 'active':
			for residue in selection[1]['selection']:
				if residue not in self.airdict[residue[0]]:
					self.airdict[residue[0]][residue] = []
				for partner in selection[2]['selection']:
					if not partner in self.airdict[residue[0]][residue]:
						self.airdict[residue[0]][residue].append(partner)
		else:
			for partner in selection[2]['selection']:
				if partner not in self.airdict[partner[0]]:
					self.airdict[partner[0]][partner] = []
				for n in selection[1]['selection']:
					if not n in self.airdict[partner[0]][partner]:
						self.airdict[partner[0]][partner].append(n)
		
		if selection[2]['type'] == 'active':
			for residue in selection[2]['selection']:
				if residue not in self.airdict[residue[0]]:
					self.airdict[residue[0]][residue] = []
				for partner in selection[1]['selection']:
					if not partner in self.airdict[residue[0]][residue]: 	
						self.airdict[residue[0]][residue].append(partner)
		else:
			for partner in selection[1]['selection']:
				if partner not in self.airdict[partner[0]]:
					self.airdict[partner[0]][partner] = []
				for n in selection[2]['selection']:
					if not n in self.airdict[partner[0]][partner]:
						self.airdict[partner[0]][partner].append(n)

	def unsetAir(self,DeactivateSelection,resremove=False):
		
		"""Remove given active and/or passive from the AIR dictionary. If the resremove argument equals True than
		   The definition only evaluates the segid and residue number. So even if their are active or passive
		   residues with specific atom selections they wil still be removed.
		"""
		newdict = {}
		if resremove == True: 
			DeactivateSelection = [(n[0],n[1]) for n in DeactivateSelection]
			for chain in self.airdict:
				newdict[chain] = {}
				for resid in self.airdict[chain]:
					if not (resid[0],resid[1]) in DeactivateSelection:
						newdict[chain][resid] = []
						for sec in self.airdict[chain][resid]:
							if not (sec[0],sec[1]) in DeactivateSelection: newdict[chain][resid].append(copy.copy(sec))
		else:
			for chain in self.airdict:
				newdict[chain] = {}
				for resid in self.airdict[chain]:
					if not resid in DeactivateSelection:
						newdict[chain][resid] = []
						for sec in self.airdict[chain][resid]:
							if not sec in DeactivateSelection: newdict[chain][resid].append(copy.copy(sec))
		
		self.airdict = newdict
	
	def resolveSelection(self,quickselect='Off'):
		
		"""Get all atoms in current pymol selection"""
		
		PartialSelector = {}
		
		model = cmd.get_model('sele')
		for m in model.atom:
			residue = ("segid %s" % m.chain,"resid %s" % m.resi,m.resn)
			if residue not in PartialSelector: 
				PartialSelector[residue] = []
				PartialSelector[residue].append(m.name)
			else: 
				PartialSelector[residue].append(m.name)	
		
		FullSelector = []
		for residue in PartialSelector:
			if quickselect == 'NA-sugar' and residue[2] in self.NAbase:
				FullSelector.append((residue[0],residue[1],self.NAsugar))
			elif quickselect == 'NA-base' and residue[2] in self.NAbase:
				FullSelector.append((residue[0],residue[1],self.NAbase[residue[2]]))
			elif quickselect == 'NA-major' and residue[2] in self.NAmajor:
				FullSelector.append((residue[0],residue[1],self.NAmajor[residue[2]]))
			elif quickselect == 'NA-minor' and residue[2] in self.NAminor:
				FullSelector.append((residue[0],residue[1],self.NAminor[residue[2]]))		
			else:		
				model = cmd.get_model(" and ".join(residue[0:2]))
				all_atoms = len([m for m in model.atom])
				if len(PartialSelector[residue]) == all_atoms: FullSelector.append((residue[0:2]))
				else: FullSelector.append((residue[0],residue[1],self.__formatAtomString(PartialSelector[residue])))

		return FullSelector	
			
	def cleanup(self):
		
		"""Re-initialize the dictionaries"""
		
		self.airdict.clear(); self.activedict.clear(); self.passivedict.clear()
		
		for segid in self.segids:
			self.airdict['segid %s' % segid] = {}
		
	def readAirFile(self,tbl):
		
		"""
		Read through the AIR file line by line. When encountering an active residue append it to
		the 'active' and 'air' dictionaries. Then start to extract the active and passive residues
		beloging to that source active residue and append them to the 'air' dictionary. The procedure
		also extracts atom selections if defined. Finish the procedure by extracting passive 
		restraints from the 'air' dictionary and appending them to the 'passive' dictionary.  
		"""
		
		splitter1 = re.compile('\(|\)'); startassign = False
		
		airfile = open(tbl,'r')
		for line in airfile.readlines():
			pairs = self.__removeBlank(splitter1.split(line.strip()))
			if len(pairs):
				if pairs[0] == 'assign': 
					startassign = True
					format = self.__formatAssignment(pairs[1:len(pairs)])
					
					if format[0] not in self.activedict: self.activedict[format[0]] = []
					self.activedict[format[0]].append(format)
				
					if format[0] not in self.airdict: self.airdict[format[0]] = {}
					self.currchain = copy.copy(format[0])
					self.currresid = format
				
				elif self.__formatCutoff(pairs[0]):
					base = [n for n in self.currresid]
					#base.append(self.__formatCutoff(pairs[0])[0]) Let's not add cutoff for the moment
					
					self.airdict[self.currchain][tuple(base)] = copy.copy(self.currselect)
					self.currselect = []
					startassign = False
					
				elif startassign == True and not pairs[0] == 'or':
					self.currselect.append(self.__formatAssignment(pairs))
				else:
					pass		
		
		airfile.close()
		self.__resolveActivePassive()
	
	def writeRestraints(self,filename):
		
		"""Write a propper formatted HADDOCK Ambiguous Interaction Restraint file to disk"""
		
		ambig = open(filename, 'w')
		#ambig = file(filename,'w')
		
		for segid in self.airdict:
			ambig.write("! HADDOCK Ambiguous Interaction Restraints for %s\n" % segid)
			ambig.write("!\n")
			for active in self.airdict[segid]:
				if len(active) == 2: ambig.write("assign ( %s and %s)\n" % (active[1],active[0]))
				else: ambig.write("assign ( %s and %s and (%s))\n" % (active[1],active[0],active[2]))
				ambig.write("       (\n")
				for sec in self.airdict[segid][active]:
					if not self.airdict[segid][active].index(sec) == 0: ambig.write("        or\n")
					if len(sec) == 2: ambig.write("       ( %s and %s)\n" % (sec[1],sec[0]))
					else: ambig.write("       ( %s and %s and (%s))\n" % (sec[1],sec[0],sec[2]))
				ambig.write("       ) 2.0 2.0 0.0\n")
				ambig.write("!\n")			
					
		ambig.close()
	
# Initiate the file menu in Pymol
cmd.set_wizard( Restraints_wiz() )