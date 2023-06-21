Here is a repo for use in L1T E/gamma ID studies for upgrade L1T. 

`test.py` contains some code to read in a data file into python. What we end up with are three important python objects:

 - `particles` is a jagged array of particles reconstructed in the L1 trigger, with shape [event, particle]. running `particles.fields` will show a list of all the contained variables, and there's some documentation of what each field means in `fileutil.py`.
 - `ecalDeposits` is a jagged array of deposits in the ECAL corresponding to each particle. It has shape [event, particle, 15, 3], corresponding to a 15x3 slice of ECAL crystals centered on the reconstructed particle. The short direction is the phi direction, and the long direction is the eta direction, which is the bending direction in the CMS magnetic field (hence needing larger clusters in that direction). Most particles will be reconstructed with only the central 5x3 slice, but electrons can have an additional 5x3 slice on each side to recover radiation emitted while the electron was passing through the tracker. For the moment lets just consider the entire 15x3 block
 - `hcalDeposits` is a jagged array of deposits in the HCAL corresponding to each particle. It has have [event, particle, 3, 3], corresponding to a 3x3 block of HCAL towers centered on the reconstructed particle. Note that each HCAL tower is about the size of a 3x3 block of ECAL crystals, so the physical size of this is equivalent to a ~9x9 block of ECAL crystals.
