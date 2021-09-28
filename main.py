import royaldataset.flist as flist
import royaldataset.fconv as fconv
import royaldataset.dgather as dgather
import royaldataset.dextract as dextract
import royaldataset.runner as runner


outdir = 'out/'
datadir = 'Data/'

flist.run(outdir, datadir)
fconv.run(outdir)
dextract.run(outdir)
dgather.run(outdir)
#runner.run(outdir)
