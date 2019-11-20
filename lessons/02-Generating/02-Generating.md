Generating Events with `AmpGen`
==

To generate events we use the command `Generator`, which takes the arguments

    ``--nEvents``, the number of events to generate (the default value is 1)

    ``--EventType``, the "type" of event in a string that describes the decay type, e.g. "D0 K0S0 pi- pi+" describes $`D^0 \to K_S^0 \pi^+ \pi^-`$

    ``--Output``, the ROOT file to output the tuple of generated events

    ``--Seed``, the seed for the random number generator in `AmpGen`, it is 0 by default but should be changed for pull studies.

We must also define our amplitude model (as seen in the [Amplitude Lesson](lessons/02-Amplitudes/02-Amplitudes.md))

In our example let's generate 10,000  $$D^0 \to K_S^0 \pi^+ \pi^-$$ events and save them as `Output.root` using the options file called `kspipi.opt`
```
Generator --Output Output.root --EventType "D0 K0S0 pi- pi+" --nEvents 10000 --Seed $RANDOM kspipi.opt
```
note that we have also used the `bash` variable `$RANDOM` to ensure the seed is different each time we run this command, otherwise every time we will generate identical sets of events.

The output from the above command should look like

![](Generator_Output.png)

We can examine the `ROOT` file with `TBrowser`, which should show the structure of the output file

![](TBrowser.png)

`Generator` will automatically produce histograms for the Dalitz variables (in 1D and 2D)

![](s01.png)


![](s02.png)


![](s12.png)

![](s01xs02.png)


![](s01xs12.png)


![](s02xs12.png)
