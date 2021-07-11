import numpy as np
import xarray as xr
import config
from datetime import datetime

tfact = config.tfact
pfact = config.pfact

nmem = config.nmem
nmode = config.nmode
nlon, nlat, nlev, nt = config.nlon, config.nlat, config.nlev, config.nt
size2d = nlon * nlat
size3d = nlon * nlat * nlev
lmoist = config.lmoist
psname = config.names["ps"]
uname, vname = config.names["u"], config.names["v"]
tname = config.names["T"]
surffname = config.surffname
plevfname = config.plevfname
if lmoist:
    qfact = config.qfact
    qname = config.names["q"]
indir = config.indir
svdir = config.svdir
modedir = config.modedir
init = config.init
lon = config.lon
lat = config.lat
plev = config.plev
time = config.time
wlev = config.wlev


if __name__ == "__main__":
    vmat = np.load(f"{svdir}/vmat.npy")
    zmat = np.zeros([nt, size2d, nmem])
    zmatu = np.zeros([nt, size3d, nmem])
    zmatv = np.zeros([nt, size3d, nmem])
    zmatT = np.zeros([nt, size3d, nmem])
    ps = np.zeros([nt, nlat, nlon])
    u = np.zeros([nt, nlev, nlat, nlon])
    v = np.zeros([nt, nlev, nlat, nlon])
    T = np.zeros([nt, nlev, nlat, nlon])
    if lmoist:
        zmatq = np.zeros([nt, size3d, nmem])
        q = np.zeros([nt, nlev, nlat, nlon])

    for i in range(nmem):
        with xr.open_dataset(f"{indir}/{surffname}{i+1:02}.nc") as ds:
            for j in range(nt):
                zmat[j,:,i] = ds[psname][j,:,:].values.flatten()
        with xr.open_dataset(f"{indir}/{plevfname}{i+1:02}.nc") as ds:
            for j in range(nt):
                zmatu[j,:,i] = ds[uname][j,:,:,:].values.flatten()
                zmatv[j,:,i] = ds[vname][j,:,:,:].values.flatten()
                zmatT[j,:,i] = ds[tname][j,:,:,:].values.flatten()
                if lmoist:
                    zmatq[j,:,i] = ds[qname][j,:,:,:].values.flatten()

    for i in range(nmode):
        for j in range(nt):
            ps[j,:,:] = (zmat[j,:,:] @ vmat[:,i]).reshape([nlat, nlon])
            u[j,:,:,:] = (zmatu[j,:,:] @ vmat[:,i]).reshape([nlev, nlat, nlon])
            v[j,:,:,:] = (zmatv[j,:,:] @ vmat[:,i]).reshape([nlev, nlat, nlon])
            T[j,:,:,:] = (zmatT[j,:,:] @ vmat[:,i]).reshape([nlev, nlat, nlon])
            if lmoist:
                q[j,:,:,:] = (zmatq[j,:,:] @ vmat[:,i]).reshape([nlev, nlat, nlon])
        ke = 0.5 * (u**2 + v**2)
        te = ke + 0.5 * (tfact * T)**2
        ke0 = np.zeros([nt, nlat, nlon])
        te0 = 0.5 * (pfact * ps)**2
        for k in range(nlev):
            ke0 += ke[:,k,:,:] * wlev.data[k]
            te0 += te[:,k,:,:] * wlev.data[k]
        if lmoist:
            me = te + 0.5 * (qfact * q)**2
            me0 = np.zeros([nt, nlat, nlon])
            for k in range(nlev):
                me0 += me[:,k,:,:] * wlev.data[k]

        ds = xr.Dataset({
            "u": (["time", "lev", "lat", "lon"], u, {"units":"m/s"}),
            "v": (["time", "lev", "lat", "lon"], v, {"units":"m/s"}),
            "T": (["time", "lev", "lat", "lon"], T, {"units":"K"}),
            "ps": (["time", "lat", "lon"], ps, {"units":"Pa"}),
            "ke": (["time", "lev", "lat", "lon"], ke, {"units":"m2/s2"}),
            "te": (["time", "lev", "lat", "lon"], te, {"units":"m2/s2"}),
            "ke0": (["time", "lat", "lon"], ke0, {"units":"m2/s2"}),
            "te0": (["time", "lat", "lon"], te0, {"units":"m2/s2"}),
            },
            coords = {
                "time": ("time", time),
                "lev": ("lev", plev),
                "lat": ("lat", lat),
                "lon": ("lon", lon),},)
        if lmoist:
            ds["q"] = (["time", "lev", "lat", "lon"], q, {"units":"kg/kg"})
            ds["me"] = (["time", "lev", "lat", "lon"], me, {"units":"m2/s2"})
            ds["me0"] = (["time", "lat", "lon"], me0, {"units":"m2/s2"})
        ds.to_netcdf(f"{modedir}/{init}/reg{i+1:02}.nc")
