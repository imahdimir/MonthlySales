"""Use vpn for the first time to let the requests_html pkg to download chromium if it is not installed."""

##
import asyncio
import nest_asyncio
import glob
import os
import pandas as pd

# from aiohttp import ClientSession
# from requests_html import HTML
# from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
import warnings
from lxml.etree import XMLSyntaxError


try:
    from py import z_ns as ns
    from py import z_cf as cf
except ModuleNotFoundError:
    import z_ns as ns
    import z_cf as cf

warnings.filterwarnings("ignore")
nest_asyncio.apply()  # Run this line in cell mode to code work

asession = AsyncHTMLSession()
# session = HTMLSession()

lst_script_name = 'c'
script_name = 'd'

dirs = ns.ProjectDirectories()
rd = ns.RawDataColumns()

cur_prq_pn = dirs.raw / f'{script_name}{ns.parquet_suf}'
pre_prq_pn = dirs.raw / f'{lst_script_name}{ns.parquet_suf}'

# async def download_js_htmls(url):
#     async with ClientSession() as session:
#         async with session.get(url,
#                                verify_ssl=False) as resp:
#             content = await resp.text()
#             print(f"Finished downloading")
#             return content


async def write_to_file(content, file_pn):
    with open(file_pn, "w") as file:
        file.write(content)
    print(f'saved as {file_pn}')

async def web_scrape_task(url_in, file_pn):
    content = await get_render_js(url_in)
    await write_to_file(content, file_pn)

async def pages_reading_main(urls, all_file_pns):
    tasks = []
    for u, fpn in zip(urls, all_file_pns):
        tasks.append(web_scrape_task(u, fpn))
    await asyncio.wait(tasks)

# async def render_js_to_html(js_html):
#     html = HTML(html=js_html,
#                 async_=True)
#     await html.arender(reload=False)
#     return html.html


# def render_js(url):
#     r = session.get(url,
#                     verify=False)
#     r.html.render()
#     return r.html.html


async def get_render_js(url_in):
    r = await asession.get(url_in, verify = False)
    try:
        await r.html.arender()
        return r.html.html
    except XMLSyntaxError as e:
        print(e)
        return ""

def main():
    pass
    ##
    df = pd.read_parquet(pre_prq_pn)
    print(df)
    ##
    cond = df[rd.LetterCode].eq(ns.ReqParams().LetterCodeForMonthlySaleReorts)
    print(cond[cond])
    ##
    df[rd.jDate] = df[rd.Title].apply(cf.find_jdate)
    ##
    cond &= df[rd.HasHtml]
    print(cond[cond])
    ##
    df.loc[cond, rd.fullUrl] = ns.ReqParams().CodalBaseUrl + df[rd.Url]
    ##
    df.loc[cond, rd.htmlDownloaded] = df[rd.TracingNo].apply(lambda x: (
            dirs.htmls / f"{x}{ns.html_suf}").exists())
    ##
    cond &= df[rd.htmlDownloaded].eq(False)
    print(cond[cond])
    ##
    filtered_df = df[cond]
    # test1_url = filtered_df.iloc[0][rd.fullUrl]
    # test1_fpn = dirs.htmls / f'{filtered_df.iloc[0][rd.TracingNo]}{ns.html_suf}'
    # asyncio.run(pages_reading_main([test1_url], [test1_fpn]))
    ##
    clusters = cf.return_clusters_indices(filtered_df, 10)
    ##
    for i in range(len(clusters) - 1):
        start_index = clusters[i]
        end_index = clusters[i + 1]
        print(f'{start_index} to {end_index}')

        urls = filtered_df.iloc[start_index: end_index][rd.fullUrl]
        htmlfpns = str(dirs.htmls) + '/' + \
                   filtered_df.iloc[start_index: end_index][
                       rd.TracingNo].astype(str) + ns.html_suf

        asyncio.run(pages_reading_main(urls, htmlfpns))
        # break
    ##
    # remove timeout and corrupt htmls and download them again
    htmlpns = glob.glob(str(dirs.htmls / f'*{ns.html_suf}'))
    print(len(htmlpns))
    ##
    timeout_error = '"error": 504, "type": "GlobalTimeoutError"'
    ##
    timeouts = []
    for htpn in htmlpns:
        with open(htpn, 'r') as htmlf:
            htmlcont = htmlf.read()
        if timeout_error in htmlcont:
            print('TimeOut')
            timeouts.append(htpn)
            os.remove(htpn)
    ##
    for htpn in htmlpns:
        if os.path.exists(htpn):
            if os.path.getsize(htpn) < 10 * 10 ** 3:
                os.remove(htpn)
                print(htpn)
    ##
    df.loc[cond, rd.htmlDownloaded] = df[rd.TracingNo].apply(lambda x: (
            dirs.htmls / f"{x}{ns.html_suf}").exists())
    ##
    df.to_parquet(cur_prq_pn, index = False)

##
if __name__ == "__main__":
    main()
    print(f'{script_name}.py Done!')
else:
    pass
    ##
