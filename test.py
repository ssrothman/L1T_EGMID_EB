#our data is stored in .root files, a special high-energy physics data format
#we use the uproot library to read the data into python
#https://uproot.readthedocs.io/en/latest/index.html for documentation
import uproot

#we'll read in our data as jagged (non-rectangular) arrays
#we use the awkward library to handle these
#https://awkward-array.org/doc/main/ for documentation
import awkward 

#the data is on CERN EOS, a distributed filesystem
#to access it we tell uproot to use the xrootd protocol, with the specified redirector
prefix = 'root://eosuser.cern.ch//'  #points to CERN EOS

path = '/eos/cms/store/cmst3/group/exovv/precision/l1tr/' #path to data

fname = 'MinBias_TuneCP5_14TeV-pythia8_v2/output_100.root' #name of file
                                               #NB there are a bunch more files too

#open the file, and get the "TTree" that contains the data
#you probably need to make sure to activate your grid certificate before running this
f = uproot.open(prefix+path+fname)
tree = f['ntuple0/objects']

#the tree is basically a dictionary, with keys being the names of the variables
#for our purposes we are interested in the 'pup' and 'seedcone' branches
#the "pup" branch is the particles (PUPPI candidates) in the event
#the "seedcone" branch is the jets in the event, clustered with the seed cone algorithm
#NB every particle is in a jet (but it might be the only particle in the jet)

particles = tree['pup'].array() 
#we'll ignore the jets for the moment
#jets = tree['seedcone'].array() 

#this are read in as jagged arrays
#the shape is [event, index within event]

#the format here is a bit annoying, 
#   so I've writing a utility to make it easier to work with
import fileutil

particles, ecalDeposits, hcalDeposits = fileutil.reorganize_particles(particles)
#we'll ignore the jets for the moment
