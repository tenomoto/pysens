import numpy as np
import xarray as xr
import config

tfact = config.tfact
pfact = config.pfact
qfact = config.qfact

nmem = config.nmem
nlon, nlat, nlev = config.nlonv, config.nlatv, config.nlev
size2d = nlon * nlat
size3d = nlon * nlat * nlev
nstate = config.nstate
lon0, lon1 = config.lon0, config.lon1
lat0, lat1 = config.lat0, config.lat1 
lmoist = config.lmoist
psname = config.names["ps"]
uname, vname = config.names["u"], config.names["v"]
tname = config.names["T"]
surffname = config.surffname
plevfname = config.plevfname
if lmoist:
    qname = config.names["q"]
ft = config.ft
indir = config.indir
svdir = config.svdir
wlat = config.wlat
wlev = config.wlev
tv = config.tv

if __name__ == "__main__":
    zmat = np.zeros([nstate, nmem])
    for i in range(nmem):
        with xr.open_dataset(f"{indir}/{ft}/{surffname}{i+1:02}.nc") as ds:
            ps = ds[psname].loc[tv, lat0:lat1, lon0:lon1]
            ps *= pfact * wlat
            zmat[0:size2d, i] = ps.values.flatten()
        with xr.open_dataset(f"{indir}/{ft}/{plevfname}{i+1:02}.nc") as ds:
            u = ds[uname].loc[tv, :, lat0:lat1, lon0:lon1]
            u *= wlat * wlev
            zmat[size2d:size2d+size3d, i] = u.values.flatten()
            v = ds[vname].loc[tv, :, lat0:lat1, lon0:lon1]
            v *= wlat * wlev
            zmat[size2d+size3d:size2d+size3d*2, i] = v.values.flatten()
            T = ds[tname].loc[tv, :, lat0:lat1, lon0:lon1]
            T *= tfact * wlat * wlev
            zmat[size2d+size3d*2:size2d+size3d*3, i] = T.values.flatten()
            if lmoist:
                q = ds[tname].loc[tv, :, lat0:lat1, lon0:lon1]
                q *= qfact * wlat * wlev
                zmat[size2d+size3d*3:, i] = T.values.flatten()
    ss, vmat = np.linalg.eig(zmat.transpose() @ zmat)
    s = np.sqrt(ss)
    np.save(f"{svdir}/s.npy", np.sqrt(ss))
    np.save(f"{svdir}/vmat.npy", vmat)
    print(s)
    print(ss/ss.sum()*100)
