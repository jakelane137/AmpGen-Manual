import uproot
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnchoredText
from matplotlib.image import NonUniformImage

from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
viridis = plt.cm.get_cmap("viridis", 256)
newcolors = viridis(np.linspace(0, 1, 256))
newcolors2 = viridis(np.linspace(0, 1, 256))
white = np.array([256 / 256, 256 / 256, 256 / 256, 1])
newcolors[:1, :] = white
#newcolors2[128] = white
newcolors2[126] = white
#newcolors2[127] = white

newcmp = ListedColormap(newcolors)
newcmp2 = ListedColormap(newcolors2)
kppim=uproot.open("Kspipi_vs_Kppim.root")
uncorr=uproot.open("Kspipi.root")
plt.rcParams["figure.figsize"] = (16,9)
varnames = {
    "m12" : r"$m_{K_S^0 \pi^+}^2$",
    "m13" : r"$m_{K_S^0 \pi^-}^2$",
    "m23" : r"$m_{\pi^+ \pi^-}^2$"
    }

def P(f, name):
    KsE = f[name].array("_1_K0S0_E")
    KsPx = f[name].array("_1_K0S0_Px")
    KsPy = f[name].array("_1_K0S0_Py")
    KsPz = f[name].array("_1_K0S0_Pz")
    KsP = [KsE, KsPx, KsPy, KsPz]
    
    pipE = f[name].array("_3_pi#_E")
    pipPx = f[name].array("_3_pi#_Px")
    pipPy = f[name].array("_3_pi#_Py")
    pipPz = f[name].array("_3_pi#_Pz")
    pipP = [pipE, pipPx, pipPy, pipPz]
    
    pimE = f[name].array("_2_pi~_E")
    pimPx = f[name].array("_2_pi~_Px")
    pimPy = f[name].array("_2_pi~_Py")
    pimPz = f[name].array("_2_pi~_Pz")
    pimP = [pimE, pimPx, pimPy, pimPz]

    p12 = [KsP[i] + pipP[i] for i in range(4)]
    p13 = [KsP[i] + pimP[i] for i in range(4)]
    p23 = [pipP[i] + pimP[i] for i in range(4)]

    sq = lambda p : p[0]**2 - sum([x**2 for x in p[1:]])
    m12 = sq(p12)
    m13 = sq(p13)
    m23 = sq(p23)
    
    d = {
        "Ks" : KsP,
        "pip" : pipP,
        "pim" : pimP,
        "m12" : m12,
        "m13" : m13,
        "m23" : m23
        }
    return d

def plot(x):
    pU = P(uncorr, "DalitzEventList")
    pC = P(kppim, "Signal")
    fig, axes = plt.subplots(nrows=3, sharex=True)
    hist0, bins0 = np.histogram(pC[x], bins=100)
    hist1, bins1 = np.histogram(pU[x], bins=100)
    
        
    n = np.sum(hist0)
    
    center = (bins0[:-1] + bins0[1:])/2
    width = 0.7 * (bins0[1] - bins0[0])
    d = (hist1 - hist0)/np.sqrt(hist1 + hist0)
    axes[0].bar(center, hist0, align="center", width=width)
    axes[0].set_ylabel(r"$N_{corr}$")
    axes[1].bar(center, hist1, align="center", width=width)
    axes[1].set_ylabel(r"$N_{uncorr}$")
    axes[2].bar(center, d, align="center", width=width)
    axes[2].set_xlabel(rf"{varnames[x]}($GeV^2/c^4$)")
    axes[2].set_ylabel(r"$\frac{N_{corr} - N_{uncorr}}{\sqrt{N_{corr} + N_{uncorr}}}$")

    

    fig.suptitle(rf"""$K^+\pi^-$ v.s. $K^0_S \pi^+ \pi^-$
$N = {n}$""")
    
    return fig
    
def plot2D(x1, x2):
    pU = P(uncorr, "DalitzEventList")
    pC = P(kppim, "Signal")
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=True)

    hist0, X0, Y0, im0 = axes[0].hist2d(pC[x1], pC[x2], bins=100,cmap=newcmp)
    hist1, X1, Y1, im1 = axes[1].hist2d(pU[x1], pU[x2], bins=100,cmap=newcmp)
    n = np.sum(hist0)
    xc = (X1[:-1] + X1[1:])/2
    yc = (Y1[:-1] + Y1[1:])/2

    d = (hist1 - hist0)/np.sqrt(hist0 + hist1)
    xi,yi = np.meshgrid(xc,yc)
    im2 = axes[2].pcolormesh(xi,yi,d,cmap=newcmp2)
    bar0 = plt.colorbar(im0, ax=axes[0])
    bar0.set_label(r"$N_{corr}$")
    bar1 = plt.colorbar(im1, ax=axes[1])
    bar1.set_label(r"$N_{uncorr}$")
    bar2 = plt.colorbar(im2, ax=axes[2])
    bar2.set_label(r"$\frac{N_{corr} - N_{uncorr}}{\sqrt{N_{corr} + N_{uncorr}}}$")
    
    
    
    
    axes[2].set_xlabel(rf"{varnames[x1]}($GeV^2/c^4$)")
    axes[0].set_ylabel(rf"{varnames[x2]}($GeV^2/c^4$)")
    axes[1].set_ylabel(rf"{varnames[x2]}($GeV^2/c^4$)")
    axes[2].set_ylabel(rf"{varnames[x2]}($GeV^2/c^4$)")
    fig.suptitle(rf"""$K^+\pi^-$ v.s. $K^0_S \pi^+ \pi^-$
$N = {n}$""")
    #axes[1].set_title("Uncorrelated")
    
    
    return fig

figa = plot("m12")
figb = plot("m13")
figc =  plot("m23")

figa.savefig("s12.png")
figb.savefig("s13.png")
figc.savefig("s23.png")

ta = plot2D("m12", "m13")
tb = plot2D("m12", "m23")
tc = plot2D("m13", "m23")

ta.savefig("s12xs13.png")
tb.savefig("s12xs23.png")
tc.savefig("s13xs23.png")

plt.show()



