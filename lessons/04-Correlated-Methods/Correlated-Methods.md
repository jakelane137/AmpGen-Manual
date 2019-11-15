Correlated Methods in ``AmpGen``
================================

Quantum Correlated Amplitudes
-----------------------------

At experiments such as ``BESIII``, we collide $$ e^+ e^-$$ at "resonances" e.g. $$ e^+ e^- \to \psi(3770) $$ at $$\sqrt{s}=3.773 GeV$$. 
We then see the decay
$$
\psi(3770) \to D^0 \bar{D}^0
$$
with a branching fraction of 52%.

The two $$D$$ mesons are formed in a "correlated" state

$$
|\psi(3770)\rangle = \frac{1}{\sqrt{2}}(|D^0\rangle - |\bar{D}^0\rangle)
$$

the minus sign is due to the odd parity of the $$\psi(3770)$$ state.

Therefore the amplitude, $$\mathcal{A}(\psi(3770) \to D^0 \bar{D}^0)$$ will be of the form

$$
\mathcal{A}(\psi(3770) \to D^0 \bar{D}^0) = \frac{1}{\sqrt{2}} (\mathcal{A}(D^0 \to f_{1})\mathcal{A}(\bar{D}^0 \to f_{2}) - \mathcal{A}(\bar{D}^0 \to f_{1}) \mathcal{A}(D^0 \to f_{2}))
$$

where $$f_{1,2}$$ are two final states that the $$D^0 \bar{D}^0$$ decay into.

AmpGen
------


