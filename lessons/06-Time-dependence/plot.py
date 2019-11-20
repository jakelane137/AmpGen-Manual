import uproot
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm
from matplotlib.offsetbox import AnchoredText
def getArray(file, name="DalitzEventList/D0_decayTime"):
    f = uproot.open(file)
    n = name.split("/")
    t = f[n[0]]
    a = t.array(n[1])
    
    return a




def plot(file = "Kspipi.root", name="DalitzEventList/D0_decayTime"):
    x = getArray(file, name)
    fig, ax = plt.subplots()
    nBins = 100
    n, bins = np.histogram(x, bins=nBins, density=True)
    N0 = sum(n) / 100
    n = n
    mean = np.mean(x)
    center = (bins[:-1] + bins[1:])/2
    center = center
    width = 0.7 * (bins[1] - bins[0])
    err = np.sqrt(n)
    n = n
    err = err
    par, cov =curve_fit(lambda t,a, b : np.exp(t * a) * b, center, n)
    center = center * 1e6
    X = np.linspace(np.min(center), np.max(center), nBins)
    print(par)
    det = cov[0][0] * cov[1][1] - cov[0][1] * cov[1][0]
    print(f"det = {det}")
    T = -1/par[0] * 1e6
    N = par[1]
    dN = np.sqrt(cov[1][1])
    dP0 = np.sqrt(cov[0][0])
    N = round(N, 3)
    dN = round(dN, 3)
    dT = dP0 * T / np.abs(par[0])
    T = round(T, 3)
    dT = round(dT, 3)
    print(f"N = {1}, NFit = {N}")
    string = r"$f(t) = N\exp(-t/\tau)$"
    string += "\n"
    string += rf"$\tau = {T}\pm{dT}$ fs"
    string += "\n"
    string += rf"$N = {N} \pm {dN}$"
    at = AnchoredText(string, loc="center right")
    ax.add_artist(at)
    Y = np.exp(-X/T) * N

    chi2 = (Y-n)**2/(Y+n)
    chi2 = sum(chi2)
    nParams = 2
    nDof = nBins - nParams - 1
    rchi2 = chi2/nDof
    print(f"rchi2 = {rchi2}")
    ax.errorbar(center, n, err, fmt="x", label="data")
    ax.plot(X, Y, label="fit")
    ax.set_title(r"$D^0$ decay time")
    ax.set_xlabel(r"Decay Time (fs)")
    ax.set_ylabel(r"Count")
    ax.legend(loc="upper right")
    return fig

fig = plot("Kspipi.root", "DalitzEventList/D0_decayTime")
fig.savefig("D0_decayTime.png")
plt.show()
