Submitting AmpGen jobs to the GRID
===

We've seen how to use the Batch system at CERN, but we may want to use the World Wide Computing Grid (WWCG) with CERN instead.

Initial Requirements
---

Let's make sure we have GRID credentials, 
```
dirac-proxy-init
```

That's about it for running jobs on the Grid!

Singularity Containers
---

Unfortunately, it seems that running jobs on the Grid is not as simple as just supplying a script like HTCondor - this is likely due to the larger number and variety of worker nodes you have on the Grid.

To make absolutely sure that the Worker Node (WN) will actually run our code, we will use a ``container''. This is a file that has everything the program we want to run needs, in our case we will make a file called `ampgen.sif` which will be about `500MB` in size and upload it to the grid. 

Building the container
---

Fortunately the work of building the container has already been done. You will need 

    - A computer that lets you run `sudo` commands (so not `lxplus`!)
    - `Singularity` - you can install this by `pip install singularity` or via your distribution.

```
git clone github.com/jakelane137:AmpGenImage.git
cd AmpGenImage
sudo ./makeImage.sh
```

this will take a few minutes to fully build the `ampgen.sif` image. You can now run any AmpGen program you want by running

```
./ampgen.sif ./my_script.sh
```

where `my_script.sh` must have 

```
#!/usr/bin/env bash
source /ampgen_setup.sh
```

to start, then we can have

```
Generator --Output events.root --EventType "D0 K0 pi- pi+" --nEvents 10000 kspipi_model.opt
```

Uploading the container to the grid
---

First we need to upload our `ampgen.sif` to `lxplus` using `rsync`, I would suggest using your `eos` or `workfs` space, since our file is about `500MB`.
(replace X with the first letter of your username and USERNAME with your username)
```
rsync --progress ampgen.sif lxplus.cern.ch:/eos/home-X/USERNAME/ampgen.sif
```
then `ssh` to `lxplus` and navigate to `/eos/home-X/USERNAME/ampgen.sif`

Making sure you have run `lhcb-proxy-init`, run `ganga` and run the following

```
df = DiracFile("ampgen.sif", lfn="/lhcb/user/X/USERNAME/ampgen.sif")
df.put(uploadSE="CERN-USER")
```
hopefully you won't see any errors (`ganga` might complain about `GUID`'s but that's fine). 
You can now run `AmpGen` on the `Grid`!

Running on the Grid
---

To submit to the grid we need a submission file, written in `python`. In our case we need the following

```
j = Job("my_AmpGen_Job")
imageFile = DiracFile("ampgen.sif", lfn="/lhcb/user/X/USERNAME/ampgen.sif")
scriptFile = LocalFile("my_script.sh")
BannedSites = ["LCG.CSCS.ch","LCG.CBPF.br","LCG.PIC.es", "VAC.Glasgow.uk", "LCG.IN2P3.fr", "DIRAC.HLTFarm.lhcb", "LCG.Lancaster.uk", "LCG.NIKHEF.nl"]
j.inputfiles = [imageFile, scriptFile]
j.application.platform="haswell-centos7"
j.backend = Dirac()
```
then you can submit your job or add other options to it (if your script needs additional arguements etc.)


Troubleshooting
---

Since we are running our program on a large number of possible systems that we have no practical way of accessing, its likely we might run into problems when using singularity images. Unfortunately the only solution (for now) is to "ban" sites that seem to have these problems and resubmit the failed jobs. 
