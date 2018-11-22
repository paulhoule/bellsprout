from bellsprout.clients.threedbooru import find_files,read3d
import datetime
import dask.bag as db

files = find_files()[0:10]
files = db.from_sequence(files)

start = datetime.datetime.now()
all = files.map(read3d)
out =  all.compute()
print(out)
end = datetime.datetime.now()

print(f"Duration is {end-start}")