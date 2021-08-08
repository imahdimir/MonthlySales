##
from glob import glob
import json
import os

import pandas as pd


try:
    from py import z_ns as ns
    from py import z_cf as cf
except ModuleNotFoundError:
    import z_ns as ns
    import z_cf as cf

lst_script_name = 'b'
script_name = 'c'

dirs = ns.ProjectDirectories()
ct = ns.CodalTableColumns()

cur_scrp_prq_pn = dirs.raw / f'{script_name}{ns.parquet_suf}'

def extract_data_from_json(jspn):
    with open(jspn, 'r') as jsfile:
        json_dict = json.load(jsfile)

    letters = json_dict['Letters']

    outdf = pd.DataFrame(columns = ct.cols_list)
    for row in letters:
        new_entry = {}
        for key, val in row.items():
            new_entry[key] = val
        outdf = outdf.append(new_entry, ignore_index = True)
    return outdf

def main():
    pass
    ##
    json_pns = glob(str(dirs.jsons / '*.json'))
    print(str(dirs.jsons / '*.json'))
    print(len(json_pns))
    ##
    new = pd.DataFrame(columns = ct.cols_list)

    for jspn in json_pns:
        print(jspn)
        jsondf = extract_data_from_json(jspn)
        new = new.append(jsondf)
    print(new)
    ##
    new.to_parquet(dirs.raw / f'NewData{ns.parquet_suf}', index = False)
    ##
    new[ct.PublishDateTime] = new[
        ct.PublishDateTime].apply(cf.convert_pubdatetime_to_int)
    print(new)
    ##
    new = new.drop(columns = ct.SuperVision)
    print(new)
    ##
    if cur_scrp_prq_pn.exists():
        pre_data = pd.read_parquet(cur_scrp_prq_pn)
        new = new.append(pre_data)
    print(new)
    ##
    new = new.drop_duplicates()
    print(new)
    ##
    assert len(new[ct.TracingNo].unique()) == len(new), 'Not_Unique_TracingNo'
    ##
    new = new.sort_values(by = [ct.PublishDateTime], ascending = False)
    print(new)
    ##
    new.to_parquet(cur_scrp_prq_pn, index = False)
    ##
    for jpn in json_pns:
        os.remove(jpn)
        print(f'Deleted : {jpn}')

##
if __name__ == '__main__':
    main()
    print(f'{script_name}.py done!')
else:
    pass
    ##
    df = pd.read_parquet(cur_scrp_prq_pn)

##
