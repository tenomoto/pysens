#!/bin/sh
nmem=26
#yyyymmddhh=2020122012
yyyymmddhh=2019100912
indir=grib
outdir=pert/${yyyymmddhh}
var3d=uvTq
if [ -d ${outdir} ]; then
  rm -rf ${outdir}
fi
mkdir ${outdir}
for var in ps ${var3d}; do
  ifname=${indir}/${var}${yyyymmddhh}.grib
  ifname00=${indir}/${var}${yyyymmddhh}c.grib
  for i in $(seq ${nmem}); do
    ii=$(printf %0.2d ${i})
    tfname=${var}${ii}.grib
    ofname=${outdir}/${var}${ii}.nc
    grib_get -p shortName,number,stepRange,min,max,avg -w number=${i} ${ifname}
    grib_copy -w number=${i} ${ifname} ${tfname}
    cdo -f nc sub ${tfname} ${ifname00} ${ofname}
    rm -f ${tfname}
  done
done
