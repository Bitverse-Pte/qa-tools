import pandas as pds

class FHelper:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_all(self, file_path: str = "") -> str:

        if file_path == "":
            file_path = self.file_path
        
        with open(file_path, 'r') as file:
            res = file.read()

        return res

    def read_lins(self, file_path: str = "") -> list:

        if file_path == "":
            file_path = self.file_path
        
        with open(file_path, 'r') as file:
            fs = file.readlines()

        return fs

    def find_all(self, target: str) -> list:
        
        res = []
        fs = self.read_lins()
        for f in fs:
            if target in f:
                res.append(f)
        
        return res

    def write_csv(self, file_path: str, column: list, data: list):
        df = pds.DataFrame(data)
        df.columns = column
        df.to_csv(file_path)


if __name__ == "__main__":
    fHelp = FHelper("./logs/25-16-38.log")

    fs = fHelp.read_lins()
    
    res = fHelp.find_all(",tx sent: ")

    a = [r.split(",tx sent: ")[1].split(",")[0] for r in res]
    print(len(a))