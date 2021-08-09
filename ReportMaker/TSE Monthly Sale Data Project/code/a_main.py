""" python v. == 3.6.13 only
    install pkgs in requirements.txt
    This Script only updates the sale data to the latest data available on Codal.ir
    set the Code folder as Current Working Direcoty(cwd)
    """
##
try:
    from py import b_pagesJsons as b
    from py import c_tablesFromJsons as c
    from py import d_getRenderedHTMLs as d
    from py import e_extractSaleDataFromHtmlTables as e
    from py import f_applySaleModifications as f
    from py import g_cleanDataMakeOutputs as g
except ModuleNotFoundError:
    import b_pagesJsons as b
    import c_tablesFromJsons as c
    import d_getRenderedHTMLs as d
    import e_extractSaleDataFromHtmlTables as e
    import f_applySaleModifications as f
    import g_cleanDataMakeOutputs as g

def main():
    for module in [b, c, d, e, f, g]:
        module.main()

##
if __name__ == "__main__":
    main()
    print(f'All Done! \n The Monthly Sale Data is Updated. The associated Excel file is in the output folder.')
else:
    pass
    ##
