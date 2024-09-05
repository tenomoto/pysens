#!/bin/sh
nmem=50
if [ $# -lt 2 ]; then
  echo "Usage:: $0 yyyymmddhh ft"
  exit
fi
yyyymmdd=$(echo $1 | cut -c 1-8)
hh=$(echo $1 | cut -c 9-10)
ft=$2

indir=/zdata/ECMWF/ens/${yyyymmdd}
ifname=${indir}/${yyyymmdd}${hh}0000-${ft}h-enfo-ef.grib2
outdir=pert/${yyyymmdd}${hh}/${ft}
withargs='shortName=u/v/t/q/sp,typeOfLevel=isobaricInhPa/surface'
if [ -d ${outdir} ]; then
  rm -rf ${outdir}
fi
mkdir ${outdir}
echo "i=0"
#grib_get -p shortName,level,min,avg,max -w ${withargs},number=0 ${ifname}
grib_copy -w ${withargs},number=0 -B shortName,level:i ${ifname} 00.grib2
for i in $(seq ${nmem}); do
  echo "i=${i}"
  ii=$(printf %02d ${i})
  tfname=${ii}.grib2
  ofname=${outdir}/${ii}.nc
#  grib_get -p shortName,level,min,avg,max -w ${withargs},number=${i} ${ifname}
  grib_copy -w ${withargs},number=${i} -B shortName,level:i ${ifname} ${tfname}
  cdo -f nc sub ${tfname} 00.grib2 ${ofname}
  rm -f ${tfname}
done
