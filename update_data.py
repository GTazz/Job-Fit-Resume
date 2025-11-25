from scripts import *

if __name__ == "__main__":
    debug = True
    
    E_CSV = ExtractCSV(debug=debug)
    P_CSV = ParseCSV(data=E_CSV.data, debug=debug)
    
    BuildProfile(data=P_CSV.data, debug=debug)
    