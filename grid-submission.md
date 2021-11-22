# Grid Submission

We've seen how to use the Batch system at CERN, but we may want to use the World Wide Computing Grid \(WWCG\) with CERN instead.

## Initial Requirements

Let's make sure we have GRID credentials,

```text
dirac-proxy-init
```

That's about it for running jobs on the Grid!

##Gaudi Package Hack
AmpGen is a part of Gauss, however we will probably want to run a custom version of AmpGen, e.g. if we want to fit correlated data or we modify a program.
Fortunately we can `hack' the Gauss version of AmpGen and swap our AmpGen code instead of the stuff given by Gauss. 

In lxplus

```text 
lb-dev --name GaussDev Gauss/latest
cd GaussDev
git lb-use Gauss
git lb-checkout Gauss/master Gen/AmpGen
```

Now we have Gauss's version of AmpGen. All we need to do is replace all the files in Gen/AmpGen/(AmpGen,src,options). 
Here's a script you can modifiy to replace the Gauss version of AmpGen with one you've built on lxplus, note that there are some custom programs (e.g. MI.cpp, BESIIILHCbKspipi.cpp)

```text
#!/bin/bash
SOURCE=/afs/cern.ch/user/j/jolane/sw/AmpGen
TARGET=/afs/cern.ch/user/j/jolane/sw/AmpGenGauss/GaussDev/Gen/AmpGen

rm $TARGET/AmpGen/*.h
rm $TARGET/src/*.cpp
rm $TARGET/src/Lineshapes/*.cpp

rm $TARGET/apps/*.cpp

cp $SOURCE/AmpGen/*.h $TARGET/AmpGen/
cp $SOURCE/src/*.cpp $TARGET/src
cp $SOURCE/options/* $TARGET/options/
cp $SOURCE/doc/* $TARGET/doc/
cp $SOURCE/src/Lineshapes/*.cpp $TARGET/src/Lineshapes
cp $SOURCE/examples/{MI,gammaGen,QcGen2,gamCombFit,BESIIILHCbKspipi,SignalOnlyFitter}.cpp $TARGET/apps
cp $SOURCE/apps/Generator.cpp $TARGET/apps

```
just replace the SOURCE and TARGET variables to point to your local build of AmpGen on lxplus and the location of AmpGen inside the GaussDev directory


## Singularity Containers (Slow option)

Unfortunately, it seems that running jobs on the Grid is not as simple as just supplying a script like HTCondor - this is likely due to the larger number and variety of worker nodes you have on the Grid.

To make absolutely sure that the Worker Node \(WN\) will actually run our code, we will use a container. This is a file that has everything the program we want to run needs, in our case we will make a file called `ampgen.sif` which will be about `500MB` in size and upload it to the grid.

## Building the container

Fortunately the work of building the container has already been done. You will need

* A computer that lets you run `sudo` commands \(so not `lxplus`!\)
* `Singularity` - you can install this by `pip install singularity` or via your distribution.

```text
git clone github.com/jakelane137:AmpGenImage.git
cd AmpGenImage
sudo ./makeImage.sh
```

this will take a few minutes to fully build the `ampgen.sif` image. You can now run any AmpGen program you want by running

```text
./ampgen.sif ./my_script.sh
```

where `my_script.sh` must have

```text
#!/usr/bin/env bash
source /ampgen_setup.sh
```

to start, then we can have

```text
Generator --Output events.root --EventType "D0 K0 pi- pi+" --nEvents 10000 kspipi_model.opt
```

## Uploading the container to the grid

First we need to upload our `ampgen.sif` to `lxplus` using `rsync`, I would suggest using your `eos` or `workfs` space, since our file is about `500MB`. \(replace X with the first letter of your username and USERNAME with your username\)

```text
rsync --progress ampgen.sif lxplus.cern.ch:/eos/home-X/USERNAME/ampgen.sif
```

then `ssh` to `lxplus` and navigate to `/eos/home-X/USERNAME/ampgen.sif`

Making sure you have run `lhcb-proxy-init`, run `ganga` and run the following

```text
df = DiracFile("ampgen.sif", lfn="/lhcb/user/X/USERNAME/ampgen.sif")
df.put(uploadSE="CERN-USER")
```

hopefully you won't see any errors \(`ganga` might complain about `GUID`'s but that's fine\). You can now run `AmpGen` on the `Grid`!

## Running on the Grid

To submit to the grid we need a submission file, written in `python`. In our case we need the following

```text
j = Job("my_AmpGen_Job")
imageFile = DiracFile("ampgen.sif", lfn="/lhcb/user/X/USERNAME/ampgen.sif")
scriptFile = LocalFile("my_script.sh")
BannedSites = ["LCG.CSCS.ch","LCG.CBPF.br","LCG.PIC.es", "VAC.Glasgow.uk", "LCG.IN2P3.fr", "DIRAC.HLTFarm.lhcb", "LCG.Lancaster.uk", "LCG.NIKHEF.nl"]
j.inputfiles = [imageFile, scriptFile]
j.application.exe = "singularity"
j.application.args = "run ampgen.sif ./my_script.sh".split()
j.application.platform="haswell-centos7"
j.backend = Dirac()

```





then you can submit your job or add other options to it \(if your script needs additional arguements etc.\)

## Troubleshooting

Since we are running our program on a large number of possible systems that we have no practical way of accessing, its likely we might run into problems when using singularity images. Unfortunately the only solution \(for now\) is to "ban" sites that seem to have these problems and resubmit the failed jobs.

