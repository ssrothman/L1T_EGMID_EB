import awkward as ak

def reorganize_particles(particles):
    '''
    The default way uproot reads in these particles is super annoying
    This is just a utility to transform them into objects that make sense
    '''
    particle_props = {
        #kinematic properties
        'pt': particles['pup.pt'],
        'eta': particles['pup.eta'],
        'phi': particles['pup.phi'],
        'mass': particles['pup.m'],
        'energy': particles['pup.e'],
        #particle ID & charge
        'pdgid': particles['pup.pdgId'],
        'charge': particles['pup.charge'],
        #pileup weight assigned by PUPPI algorithm
        'pupw': particles['pup.pupw'],
        #properties of any linked track. if no track, I bet these are zero [check!]
       'x0' : particles['pup.x0'], #xyz coordinates of extrapolated vertex
        'y0' : particles['pup.y0'],
        'z0' : particles['pup.z0'],
        'dxy': particles['pup.dxy'], #xy displacement of vertex from beamline
        'd0': particles['pup.d0'], #don't remember
        'tkmva1': particles['pup.tkmva1'], #not sure what these are tbh. should ask Phil
        'tkmva2': particles['pup.tkmva2'], 
        'tkmva3': particles['pup.tkmva3'],
        'tkCaloEta': particles['pup.tkCaloEta'], #eta of extrapolated track at ECAL
        'tkCaloPhi': particles['pup.tkCaloPhi'], #phi of extrapolated track at ECAL
        'tkchi2': particles['pup.chi2'], #chi2 of track fit
        'nstubs' : particles['pup.nstubs'], #number of stubs in track
        'npar' : particles['pup.npar'], #honestly not sure. Should ask Phil
        #calorimetery properties
        'hOverE' : particles['pup.hOverE'], #ratio of energy in ECAL/HCAL
        'CaloEt' : particles['pup.CaloEt'], #transverse energy in ECAL+HCAL
        #there are two MVAs that are only defined for hgcal and so we will ignore them
        #'egPiMVA' : particles['pup.egPiMVA'], 
        #'egPUMVA' : particles['pup.egGammaMVA'], 
    }

    ecalshape = particles['pup.ecalShapeInfo[45]']#energy deposits in 3x15 ECAL crystals
    #reshape ecalshape into 3x15 array
    ecalshape = ak.unflatten(ecalshape, 3, axis=-1)

    hcalshape = particles['pup.hcalShapeInfo[9]']#energy deposits in 3x3 HCAL crystals
    #reshape hcalshape into 3x3 array
    hcalshape = ak.unflatten(hcalshape, 3, axis=-1)

    return ak.zip(particle_props), ecalshape, hcalshape

def reorganize_jets(jets, sensibleparticles, ecalshape, hcalshape):
    '''
    The default way uproot reads in these jets is super annoying
    This is just a utility to transform them into objects that make sense
    '''
    jet_props = {
        'npart' : jets['seedcone.npart'], #number of particles in jet
        #kinematic properties
        'pt': jets['seedcone.pt'],
        'eta': jets['seedcone.eta'],
        'phi': jets['seedcone.phi'],
        'mass': jets['seedcone.m'],
        'energy': jets['seedcone.e'],
        #seed properties
        'seedpt': jets['seedcone.seedpt'],
        'seedeta': jets['seedcone.seedeta'],
        'seedphi': jets['seedcone.seedphi'],
    }
    raise NotImplementedError("Haven't yet setup indexing magic for jets")
    idxs = jets['seedcone.Parts'] #has shape [event, jet, particle]
    nparts = ak.to_numpy(ak.flatten(ak.num(idxs, axis=2)))
    flatidxs = ak.flatten(idxs, axis=-1) #flatten the indices to shape [event, particle]

    flatparts = sensibleparticles[flatidxs] #get the particles in the jet
    flatecal = ecalshape[flatidxs] #get the ecal deposits in the jet
    flathcal = hcalshape[flatidxs] #get the hcal deposits in the jet

    #unflatten to shape event, jet, particle
    parts = ak.unflatten(flatparts, nparts, axis=-1)
    necal = np.repeat(nparts, np.ones_like(nparts)*45)
    ecal = ak.unflatten(flatecal, nparts, axis=-1)
    hcal = ak.unflatten(flathcal, nparts, axis=-1)
