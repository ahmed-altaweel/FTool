import glob
class PatternResolver:
    def resolve(self,path,recursive):
       return glob.glob(str(path),recursive=recursive)
